# Pin Delays

Takes an excel file and looks for the two columns "Pin Name" and "Delay". Then reads the rest of the sheet
and produces a correctly formatting pin package length file for either Mentor (icdb flows) or Allergo.

You need to do any math in excel prior to running the script to convert the Delay column to the right unit.

Mentor must take mils and cadence can take either mils or ns.

## Install
* Clone this repo to your machine
* Run `pip install .` from that folder

## Usage
```
pindelays --help
usage: pindelays [-h] [--cadence] [--mentor] [--partnumber PARTNUMBER]
                 [--package PACKAGE] [--refdes REFDES] [--units UNITS]
                 excel_file [excel_file ...]

For high speed PCB designs, one must take into account the internal length of a pin.  Because
the difference between pins in a diff pair could be so much that the signal would not work well.
This is also very common for DDR buses. This python program takes an excel file and produces a pin
delay file that is correctly formatted for your EDA tool set.

positional arguments:
  excel_file            The excel file to read in

optional arguments:
  -h, --help            show this help message and exit
  --cadence, -c         Generate Cadence File
  --mentor, -m          Generate Mentor File
  --partnumber PARTNUMBER, -p PARTNUMBER
                        Part number [Only used in mentor]
  --package PACKAGE, -d PACKAGE
                        Device Package [Only used in cadence]
  --refdes REFDES, -r REFDES
                        RefDes [Only used in cadence]
  --units UNITS, -u UNITS
                        RefDes [Only used in cadence] Mentor needs mils
```
