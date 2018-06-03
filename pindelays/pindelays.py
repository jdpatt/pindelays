"""For high speed PCB designs, one must take into account the internal length of a pin.  Because
the difference between pins in a diff pair could be so much that the signal would not work well.
This is also very common for DDR buses. This python program takes an excel file and produces a pin
delay file that is correctly formatted for your EDA tool set. """
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Dict, Any
from openpyxl import load_workbook, Workbook
from openpyxl.utils import column_index_from_string


def get_column(name: str, columns: list) -> int:
    """Search a row of cells for the string.

    Args:
        name: The text to search for
        columns: The list or generator of columns in the excel sheet

    Returns:
        Either returns the column number or returns 0 if no column matched the name

    """
    for col in columns:
        if col[0].value == name:  # Only look at the first row
            return int(column_index_from_string(col[0].column))
    return 0


def parse_excel_file(workbook: Workbook) -> Dict[str, Any]:
    """  Read in excel and get the pin number and internal length

    The excel file must have a header row with the cells "Pin Name" and "Delay".  It does not
    matter which column they are in.

    Args:
        excel_file: The excel file to open and read from

    """
    sheet = workbook.active
    delay_dict = dict()
    columns = list(sheet.iter_cols(max_row=1))
    try:
        pin_col = get_column('Pin Name', columns)
        delay_col = get_column('Delay', columns)
        for excel_row in range(2, sheet.max_row + 1):
            pin = str(sheet.cell(row=excel_row, column=pin_col).value)
            delay = str(sheet.cell(row=excel_row, column=delay_col).value)
            if not all([pin, delay]):
                raise ValueError
            else:
                delay_dict.update({pin: delay})
    except (ValueError, KeyError, UnboundLocalError) as error:
        print(error)
        raise
    return delay_dict


def generate_mentor(partnumber: str, delays: Dict) -> None:
    """ This function generates a text file that can be imported in the Constraint Manager tool.

    Example:
        UNITS <value> th
        PART_NUMBER <part_number>
        <pin_number> <value>

    Args:
        partnumber: The part number to apply these delays
        delays: The data read in from the excel file

    """
    with open('PinPkgLengths.txt', 'w') as output:
        output.write('UNITS th\n')
        output.write(f'PART_NUMBER {partnumber}\n')
        for key, value in delays.items():
            output.write(f'{key} {value}\n')


def generate_cadence(ref: str, package: str, unit: str, delays: Dict) -> None:
    """ This function generates a text file that can be imported into Allergo if you are using the
    high speed license. Allergo applies delays individual vs against all part numbers that match
    like mentor.  UNITS MIL can be a header row that applies to everything or you can list unit for
    every row.  This does the later.

    Example:
        [PIN DELAY]
        [RefDes    <refdes>]
        [DEVICE    <package name>]
        [UNITS     <mks units>]
        <Pin number>    <delay value> <...>

    Args:
        ref:  The reference designator to apply the delays
        package: The cadence source package
        unit: The unit of the delays in either MIL or NS
        delays: The data read in from the excel file

    """
    with open(f'{package}.csv', 'w') as output:
        output.write('PIN DELAY\n')
        output.write(f'REFDES\t{ref}\n')
        output.write(f'DEVICE\t{package}\n')
        output.write('\n')
        for key, value in delays.items():
            output.write(f'{key}\t{value}\t{unit}\n')


def parse_cmd_line():
    """handle all the command line inputs. """
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    parser.add_argument('excel_file',
                        nargs='+',
                        help='The excel file to read in')
    parser.add_argument('--cadence', '-c',
                        action='store_true',
                        default=True,
                        help='Generate Cadence File')
    parser.add_argument('--mentor', '-m',
                        action='store_true',
                        default=False,
                        help='Generate Mentor File')
    parser.add_argument('--partnumber', '-p',
                        default='dummy_part',
                        help='Part number [Only used in mentor]')
    parser.add_argument('--package', '-d',
                        default='dummy_package',
                        help='Device Package [Only used in cadence]')
    parser.add_argument('--refdes', '-r',
                        default='U1',
                        help='RefDes [Only used in cadence]')
    parser.add_argument('--units', '-u',
                        default='NS',
                        help='RefDes [Only used in cadence] Mentor needs mils')
    return parser.parse_args()


def main():
    """Main Application Entry """
    args = parse_cmd_line()
    for file_to_parse in args.excel_file:
        print(f'Reading in Excel File: {Path(file_to_parse)}')
        part_delays = parse_excel_file(load_workbook(file_to_parse, data_only=True))
        if args.cadence:
            generate_cadence(args.refdes, args.package, args.units, part_delays)
            print(f'Cadence File Generated')
        if args.mentor:
            generate_mentor(args.partnumber, part_delays)
            print(f'Mentor File Generated')


if __name__ == '__main__':
    main()
