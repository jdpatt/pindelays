# Pin Delays

Takes an excel file and looks for the two columns "Pin Name" and "Delay". Then reads the rest of the sheet
and produces a correctly formatting pin package length file for either Mentor (icdb flows) or Allergo.

You need to do any math in excel prior to running the script to convert the Delay column to the right unit.

Mentor must take mils and cadence can take either mils or ns.