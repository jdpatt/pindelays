import pytest
from openpyxl import Workbook
from pathlib import Path

from pindelays.pindelays import (
    get_column,
    parse_excel_file,
    generate_mentor,
    generate_cadence,
)


@pytest.fixture(scope="session")
def workbook():
    wb = Workbook()
    ws = wb.active
    ws["A1"] = "Pin Name"
    ws["B1"] = "Delay"
    ws["A2"] = "A1"
    ws["B2"] = "10"
    ws["A3"] = "A2"
    ws["B3"] = "12"
    return wb


@pytest.mark.usefixtures("workbook")
class TestPinDelays(object):
    def test_get_column(self, workbook):
        """ If the cell exists return the position otherwise return None """
        worksheet = workbook.active
        assert get_column("Delay", worksheet) == 2
        assert get_column("foo", worksheet) == 0

    def test_parse_excel_file(self, workbook):
        assert parse_excel_file(workbook) == {"A1": "10", "A2": "12"}

    def test_parse_excel_file_value_error(self, workbook):
        workbook.active["B2"] = ""  # Missing delay for pin A1
        with pytest.raises(ValueError):
            parse_excel_file(workbook)

    def test_generate_cadence(self, workbook):
        delays = {"A1": "10", "A2": "12"}
        generate_cadence("U1", "test_package", "MIL", delays)
        with open(Path().cwd().joinpath("test_package.csv")) as cadence:
            assert cadence.read() == (
                "PIN DELAY\n"
                "REFDES\tU1\n"
                "DEVICE\ttest_package\n\n"
                "A1\t10\tMIL\n"
                "A2\t12\tMIL\n"
            )

    def test_generate_mentor(self, workbook):
        delays = {"A1": "10", "A2": "12"}
        generate_mentor("test_partnumber", delays)
        with open(Path().cwd().joinpath("PinPkgLengths.txt")) as mentor:
            assert mentor.read() == (
                "UNITS th\n" "PART_NUMBER test_partnumber\n" "A1 10\n" "A2 12\n"
            )
