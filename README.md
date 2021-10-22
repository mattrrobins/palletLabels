README for Project: palletLabels

This program features a tkinter-built GUI which creates scannable barcoded label for inventory management based on the user's input.  The program previews the label, and if the printer settings have been configured to the user's Zebra printer, the program will print the label to that printer.

Configure Zebra Printer:
Go to views.pr_id and enter the printer network address as a string.  I.e., a numerical grouping of the form: 'xxx.xxx.xxx.xxx'

The resultant label will contain:
- Item number (barcode scannable)
- Total quantity (barcode scannable)
- Auto generated date
- The requisite math for easily checking a count on a pallet
