import os
from pathlib import Path
from src.testsolar_python_unittest.executor import parse_test_report

testdata_dir: str = str(Path(__file__).parent.absolute().joinpath("testdata"))


def test_parse_test_report():
    results = parse_test_report(
        proj_path=testdata_dir, xml_file=os.path.join(testdata_dir, "xml_results.xml")
    )
    assert len(results) == 30


def test_parse_failed_report():
    results = parse_test_report(
        proj_path=testdata_dir,
        xml_file=os.path.join(testdata_dir, "failed_results.xml"),
    )
    assert len(results) == 1
    assert (
        results[0].Test.Name
        == "setUpClass (example.order_process.test_ct_cn_order_approval.TestExample)"
    )
