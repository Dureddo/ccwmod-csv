# CCWMOD to CSV File Conversion

This utility converts the Modbus mapping exported from Connected Components Workbench to a CSV file. This can be useful when setting up something like a Kepware OPC server with tags associated with these mappings.

## Usage

```
python ccwmod-csv.py -h
```

The command-line help will explain the options and general usage. A typical example is:

```
python ccwmod-csv.py -m file.ccwmod -o file.csv -p Tag_Prefix_ -r
```

The above command will:

* Take `file.ccwmod` as the input map file.
* Output to `file.csv`.
* Prefix all tags with the string "Tag_Prefix_".
* Make all tags read only.
