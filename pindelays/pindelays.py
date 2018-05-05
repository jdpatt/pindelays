''' Take an excel file in and produce a pin delay file for a device '''
from argparse import ArgumentParser
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string


def getColIndexOfHeader(name, columns):
    ''' If the cell exists return the position otherwise return None '''
    for col in columns:
        if col[0].value == name:  # Only look at the first row
            return column_index_from_string(col[0].column)
    return None


def parseExcelFile(excel_file):
    '''  Read in excel and get the pin number, function, and color '''
    workbook = load_workbook(excel_file, data_only=True)
    sheet = workbook.active
    delay_dict = dict()
    try:
        pin_col = getColIndexOfHeader('Pin Name', sheet.iter_cols(max_row=1))
        delay_col = getColIndexOfHeader('Delay', sheet.iter_cols(max_row=1))
        for excel_row in range(2, sheet.max_row + 1):
            pin = sheet.cell(row=excel_row, column=pin_col).value
            delay = sheet.cell(row=excel_row, column=delay_col).value
            if not all([pin, delay]):
                raise ValueError
            else:
                delay_dict.update({pin: delay})
    except (TypeError, ValueError, KeyError, UnboundLocalError) as error:
        print(error)
        raise
    return delay_dict


def generateMentorDelay(partnumber, delays):
    ''' Ouput for Mentor Graphics should be in the following format:
        UNITS <value> th
        PART_NUMBER <part_number>
        <pin_number> <value>
    '''
    with open('PinPkgLengths.txt', 'w') as output:
        output.write('UNITS th\n')
        output.write(f'PART_NUMBER {partnumber}\n')
        for key, value in delays.items():
            output.write(f'{key} {value}\n')


def generateCadenceDelay(ref, package, unit, delays):
    ''' [PIN DELAY]
        [RefDes    <refdes>]in
        [DEVICE    <package name>]
        [UNITS     <mks units>]    Has to be either MIL or NS
        <Pin number>    <delay value> <...>
    '''
    with open(f'{package}.csv', 'w') as output:
        output.write('PIN DELAY\n')
        output.write(f'REFDES\t{ref}\n')
        output.write(f'DEVICE\t{package}\n')
        output.write('\n')
        for key, value in delays.items():
            output.write(f'{key}\t{value}\t{unit}\n')


def parseCommandLine():
    ''' handle all the command line inputs. '''
    parser = ArgumentParser()
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
                        help='Partnumber [Only used in mentor]')
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


if __name__ == '__main__':
    ARGS = parseCommandLine()
    for file_to_parse in ARGS.excel_file:
        part_delays = parseExcelFile(file_to_parse)
        if ARGS.cadence:
            generateCadenceDelay(ARGS.refdes, ARGS.package, ARGS.units, part_delays)
        if ARGS.mentor:
            generateMentorDelay(ARGS.partnumber, part_delays)
