# Pin Delays

Takes an excel file and looks for the two columns "Pin Name" and "Delay". Then reads the rest of the sheet
and produces a correctly formatting pin package length file for either Mentor (icdb flows) or Allergo.

You need to do any math in excel prior to running the script to convert the Delay column to the right unit.

## Install

* Clone this repo to your machine
* Run `pip install .` from that folder

## Usage

```shell
pindelay --help
Usage: pindelay [OPTIONS] [EXCEL_FILE]... [[cadence|mentor]]

  For today's high speed designs, one must take into account the internal
  length or delay of a pin. This python program takes an excel file and
  produces a pin delay file that is correctly formatted for your EDA tool
  set.

Options:
  -p, --partnumber TEXT    Part number [Only used in mentor]
  -d, --package TEXT       Device Package [Only used in cadence]
  -r, --refdes TEXT        RefDes [Only used in cadence]
  -u, --units [ns|ps|mil]  Units
  --version                Show the version and exit.
  -h, --help               Show this message and exit.
```
