import sys
import signal
import argparse
import xml.etree.ElementTree as et
import csv

def KeyboardInterruptHandler(sig, frame):
	print("Script interrupted by user.")
	sys.exit(0)

signal.signal(signal.SIGINT, KeyboardInterruptHandler)

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description = 
        "Take a Modbus map file from Connected Components Workbench and " +
        "translate it to a Kepware tag CSV file.\r\n" + 
        "See https://github.com/Dureddo for details.")
parser.add_argument("-m", "--mapfile", required=True,
	help="Modbus mapping file from Connected Components Workbench")
parser.add_argument("-o", "--outfile", required=True,
	help="Kepware tag CSV file")
parser.add_argument("-p", "--prefix", default='',
	help="Tag prefix")
parser.add_argument("-r", "--readonly", action="store_true",
	help="Default all tags to read-only (read-write if not specified)")
parser.add_argument("-s", "--scanrate", type=int,default=100,
	help="Specify scan rate in ms (100 ms by default)")
parser.add_argument("--noprog", action="store_true",
        help="Remove the '@<program>' suffix from variable names")
parser.add_argument("-v", "--verbose", action="store_true",
        help="Verbose output")
args = parser.parse_args()

try:
    tree = et.parse(args.mapfile).getroot()
    assert(tree.tag == "modbusServer")
except IOError as e:
    print("ERROR - Unable to open file: {}".format(args.mapfile))
    sys.exit(0)
except (AssertionError, et.ParseError) as e:
    print("ERROR - Malformed XML file")
    sys.exit(0)

fileHeader = ["Tag Name",
              "Address",
              "Data Type",
              "Respect Data Type",
              "Client Access",
              "Scan Rate",
              "Scaling",
              "Raw Low",
              "Raw High",
              "Scaled Low",
              "Scaled High",
              "Scaled Data Type",
              "Clamp Low",
              "Clamp High",
              "Eng Units",
              "Description",
              "Negate Value"
             ]
typeMap = {"Bool":"Boolean",
           "Word":"Word",
           "UInt":"Word",
           "DInt":"Long",
           "DWord":"Dword",
           "UDInt":"Dword",
           "Real":"Float",
           "AnyArray":"String"
          }

try:
    with open(args.outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fileHeader)
        for child in tree:
            if(child.tag == "modbusRegister"):
                for addr in child:
                    if(addr.tag == "mapping"):
                        name = addr.attrib["variable"]
                        if args.noprog:
                            name = name.split('@')[0]
                        name = args.prefix + name
                        csvRow = [name,
                                  addr.attrib["address"],
                                  typeMap[addr.attrib["dataType"]],
                                  '1',
                                  "R/W" if not args.readonly else "RO",
                                  args.scanrate,
                                 ] + [''] * 11 # Set scaling parameters null
                        writer.writerow(csvRow)
except IOError as e:
    print("Unable to write to file: {}".format(args.outfile))
    
