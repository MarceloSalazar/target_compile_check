# Simple script to compile an app with multiple targets/toolchains

# Workflow
# 1. Read from targets.json
# 2. Compile app for all targets, for a given toolchain
# 3. Generate report

import requests
import os
import glob
import pathlib
import urllib, json
import datetime
import time
import subprocess
from datetime import datetime
from argparse import ArgumentParser
from prettytable import PrettyTable


def get_targets():
    # Read targets from targets.json and returns list

    file_name = "./mbed-os/targets/targets.json"

    with open(file_name) as json_file:
        data = json.load(json_file)

    targets = []
    for i in data:
        if 'public' in data[i] and data[i]['public'] == False:
            continue
        targets.append(i)

    return(targets)

def compile_app(toolchain, target):

    compile_options = " -v"
    command = "mbed compile -t " + str(toolchain) + \
                " -m " + str(target) + str(compile_options)
                
    print("command: " + command)

    # Save current path        
    #top_path = os.getcwd()
    #print("path: " + top_path)
    # Change to library folder before compiling
    #temp = top_path + '/' + dft_temp_dir + self.apps[app_n]["local_dir"] + '/'
    #os.chdir(temp)


    try:
        output = subprocess.check_call(command , shell=True, stderr=subprocess.STDOUT)
        return "PASS" # compile successful

    except Exception:
        print("mbed compile error\n")
        print(subprocess.STDOUT)
        return "FAIL" # compile failed

def print_table(test_result, toolchains):

    table_header = ["Target"] + toolchains
    table = PrettyTable(table_header)

    table.align['Target'] = 'l'

    for m in test_result:
        table.add_row([str(m)] + [test_result[m][a] for a in toolchains])

    print(table)

def save_results(test_result, toolchains):

    yr = datetime.now().year
    mo = datetime.now().month
    day = datetime.now().day
    hr = datetime.now().hour
    minu = datetime.now().minute
    
    filename = "results_" + str(yr) + str(mo) + str(day) + str(hr) + str(minu) + ".txt"
    filew = open(filename,"w") 

    line = "Target " + str(' '.join(toolchains)) + "\n"
    filew.writelines(line)

    for m in test_result:
        line = str(m) + " " + str(' '.join([test_result[m][a] for a in toolchains])) + "\n"
        filew.writelines(line)

    filew.close() 

def main():
    global args

    # Parser handling
    parser = ArgumentParser(description="Automation script to compile apps for targets/toolchain")

    parser.add_argument(
        '-m', '--target', dest='target',
        help='Target name', required=False)

    parser.add_argument(
        '-t', '--toolchain', dest='toolchain',
        help='Toolchain name (ARM, GCC_ARM)', required=False)

    args = parser.parse_args()

    # Optional target
    if args.target:
        targets = str(args.target).split(",") #  compile only for a target, otherwise all targets
    else:
        # Read from targets.json
        targets = get_targets()

    # Optional toolchain:
    if args.toolchain:
        toolchains = str(args.toolchain).split(",")
    else:
        toolchains = ["ARM", "GCC_ARM"]
        
    test_result = {}

    # Compile app for all targets, for a given toolchain
    for m in targets:
        temp = dict()
        for t in toolchains:
            result = compile_app(t, m)
            temp[t] = result
        test_result[m] = temp

    # Generate report
    # Default format PrettyTable, TODO Github markdown
    save_results(test_result, toolchains)
    print_table(test_result, toolchains)

    exit(0)

if __name__ == "__main__":
    main()