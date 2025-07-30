from datetime import datetime, timedelta
from typing import List
import os
from loguru import logger
from testsolar_testtool_sdk.model.param import EntryParam
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.model.testresult import (
    TestResult,
    ResultType,
    TestCaseStep,
    TestCaseLog,
    LogLevel,
)
from testsolar_testtool_sdk.reporter import FileReporter
import xml.etree.ElementTree as ET
import unittest
import xmlrunner  # type: ignore
import coverage
from urllib.parse import urlparse, parse_qs
import sys
from pathlib import Path
import hashlib

REPORT_FILE_NAME = "test_results.xml"


def run_tests(report_file_path: str, test_cases: List[str]) -> None:
    with open(report_file_path, "wb") as output:
        suite = unittest.TestSuite()
        for test_case in test_cases:
            try:
                suite.addTests(unittest.defaultTestLoader.loadTestsFromName(test_case))
            except Exception as e:
                logger.error(f"load testcases {test_case} failed, err: {str(e)}")

        runner = xmlrunner.XMLTestRunner(output=output)
        runner.run(suite)


def parse_test_report(proj_path: str, xml_file: str) -> list[TestResult]:
    with open(xml_file, "r") as f:
        logger.info(f"xml file:\n{f.read()}")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    test_results: list[TestResult] = []
    for testcase in root.iter("testcase"):
        classname = testcase.attrib.get("classname") or ""
        if classname:
            classname = classname.split(".")[-1]
        name = testcase.attrib.get("name") or ""
        raw_file_path = testcase.attrib.get("file")
        file_name = (
            os.path.relpath(raw_file_path, proj_path)
            if raw_file_path and os.path.isabs(raw_file_path)
            else raw_file_path
        )
        start_time_str = testcase.attrib.get("timestamp")
        start_time = datetime.now()
        if start_time_str and start_time_str != "0001-01-01T00:00:00":
            start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
        run_time = testcase.attrib.get("time")
        elapsed_time = timedelta(0)
        if run_time:
            elapsed_time = timedelta(seconds=float(run_time))
        end_time = start_time + elapsed_time
        case = TestCase(
            Name=((file_name + "?") if file_name else "")
            + (
                "/".join([classname, name])
                if classname and name
                else (classname or name)
            )
        )
        tr_result: ResultType = ResultType.SUCCEED
        tr = TestResult(
            Test=case,
            StartTime=start_time,
            EndTime=end_time,
            ResultType=tr_result,
            Message="",
        )
        step_logs: List[TestCaseLog] = []
        tr.Steps.append(
            TestCaseStep(
                Title="STEP",
                StartTime=start_time,
                ResultType=tr_result,
                EndTime=end_time,
                Logs=step_logs,
            )
        )
        for child in testcase:
            content = child.text if child.text else ""
            if child.tag == "failure" or child.tag == "error":
                tr.ResultType = ResultType.FAILED
                step_logs.append(
                    TestCaseLog(Time=start_time, Level=LogLevel.ERROR, Content=content)
                )
            elif child.tag == "skipped":
                tr.ResultType = ResultType.IGNORED
                step_logs.append(
                    TestCaseLog(Time=start_time, Level=LogLevel.INFO, Content=content)
                )
            elif child.tag == "system-out":
                step_logs.append(
                    TestCaseLog(Time=start_time, Level=LogLevel.INFO, Content=content)
                )
        test_results.append(tr)
    return test_results


def get_executable_selectors(proj_path: str, test_selectors: list[str]) -> list[str]:
    parsed_selectors: list[str] = []
    for selector in test_selectors:
        url = urlparse(selector)
        abs_path = os.path.join(
            proj_path, url.path if (url.path != "." and url.path != "/") else ""
        )
        if not os.path.exists(abs_path):
            logger.error(f"can't find {abs_path}")
            continue
        if os.path.isdir(abs_path):
            if url.query:
                logger.error(
                    f"selector format: [{selector}] is illegal, please explicitly declare the file where the use case is located "
                )
                continue
            for root, dirs, files in os.walk(abs_path):
                for f in files:
                    if f.endswith(".py") and f != "__ini__.py":
                        parsed_selectors.append(
                            os.path.relpath(os.path.join(root, f), proj_path)
                        )
        elif os.path.isfile(abs_path):
            parsed_selectors.append(selector)
        else:
            logger.error(f"{url.path} if not file or dir")
    return parsed_selectors


def format_selector_to_unittest(selectors: list[str]) -> list[str]:
    testcases: list[str] = []
    for selector in selectors:
        url = urlparse(selector)
        unittest_path = url.path.removesuffix(".py").replace("/", ".")
        if url.query:
            if "=" in url.query:
                name = parse_qs(url.query).get("name")
                if name:
                    unittest_path = ".".join([unittest_path, name[0].replace("/", ".")])
            else:
                unittest_path = ".".join([unittest_path, url.query.replace("/", ".")])
        testcases.append(unittest_path)
    return testcases


def calculate_md5_hash(input_string: str) -> str:
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode("utf-8"))
    return md5_hash.hexdigest()


def run_testcases(entry: EntryParam) -> None:
    logger.info(
        f"running testcase {entry.TestSelectors} in workdir [{entry.ProjectPath}]"
    )
    executable_selectors = get_executable_selectors(
        proj_path=entry.ProjectPath, test_selectors=entry.TestSelectors
    )
    logger.info(f"get excutalbe selectors: {executable_selectors}")
    testcases = format_selector_to_unittest(executable_selectors)
    logger.info(f"format testcases: {testcases}")
    sys.path.insert(0, entry.ProjectPath)
    enable = os.environ.get("TESTSOLAR_TTP_ENABLECOVERAGE", "")
    report_file_path = os.path.join(entry.ProjectPath, REPORT_FILE_NAME)
    if enable and enable in ["1", "true", "True"]:
        cov = coverage.Coverage(source=[entry.ProjectPath])
        cov.start()
        run_tests(report_file_path=report_file_path, test_cases=testcases)
        cov.stop()
        cov.save()
        md5_str = calculate_md5_hash(input_string=" ".join(entry.TestSelectors))[:10]
        cov.xml_report(
            outfile=os.path.join(
                entry.ProjectPath, "testsolar_coverage", f"{md5_str}.xml"
            )
        )
    else:
        run_tests(report_file_path=report_file_path, test_cases=testcases)
    if not Path(report_file_path).exists():
        raise Exception(
            f"can't find test report file {report_file_path}, please check if testcases run successfully"
        )
    test_results = parse_test_report(
        proj_path=entry.ProjectPath, xml_file=report_file_path
    )
    reporter = FileReporter(report_path=Path(entry.FileReportPath))
    for result in test_results:
        reporter.report_case_result(result)
