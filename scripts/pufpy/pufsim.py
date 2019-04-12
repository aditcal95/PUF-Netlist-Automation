#!/usr/local/bin/python
from __future__ import print_function
import os
import glob
import shutil
import argparse
import subprocess

PUF_OUTPUTS = []  # Use a list to store the outputs of the PUF being tested


# A class for changing font style
class Style:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

# Helper functions


# Search current directory and find testbench netlists
def get_testbenches():
    testbenches = []
    os.chdir("./")
    for testbench in glob.glob("*_test.sp"):
        # Remove file extension and store the name of the testbench into the testbench list
        testbenches.append(os.path.splitext(os.path.basename(testbench))[0])
    return testbenches


# Read .lis HSPICE output file and write simulation results into output.txt output file
def read_results():
    # Create the output file
    output_file = open("output.txt", "w+")

    # Read .lis HSPICE output file
    unused_outputs = 0
    with open("puf_test/puf_test.lis", "r") as hspice_lis_file:
        for lis_line in hspice_lis_file:
            if ":q" in lis_line:
                if unused_outputs not in range(1, 7):
                    # Read the output voltage of the PUF
                    puf_output = float(lis_line[lis_line.index("q")+9:lis_line.index("q")+19])
                    # Store the output of the PUF
                    PUF_OUTPUTS.append(puf_output)
                    # Store in the output file 0/1 based on the output voltage of the PUF
                    if puf_output > 1:
                        output_file.write("1\n")
                    else:
                        output_file.write("0\n")

                if unused_outputs < 7:
                    unused_outputs += 1


# ==============================
# Main program
# ==============================
def main():
    # Instantiate the command line parser
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument("-mt", "--mthreaded", type=int, default=8,
                        help="Enable multi-threaded simulation and define number of available processors")

    # Parse command line options
    args = parser.parse_args()

    print(Style.BOLD + "\n>PUFSim: " + Style.END + "searching for testbenches in %s/\n..." % os.getcwd())

    # Search current directory and find testbench netlists
    testbenches = get_testbenches()

    # Go through the testbench list and simulate them one by one
    for testbench in testbenches:
        print("\n>PUFSim: creating subdirectory for simulating testbench: " + Style.BOLD + testbench + ".sp"
              + Style.END)

        # If the current simulation directory already exists delete it
        if os.path.exists(testbench) and os.path.isdir(testbench):
            shutil.rmtree(testbench)

        # Create simulation directory
        os.mkdir(testbench)

        print(">PUFSim: invoking HSPICE (-mt %d) to simulate testbench...\n" % args.mthreaded)
        try:
            # Invoke hspice to simulate the circuit. Enable multi-threaded simulation, use 8 processors if available
            process = subprocess.Popen(["hspice", "-i", (testbench + ".sp"), "-mt", str(args.mthreaded), "-o",
                                        testbench], stdin=subprocess.PIPE)
            process.communicate("\r")
        except:
            print("\n[ERROR] subprocess.py raised an exception while attempting to invoke hspice simulator")

        print(Style.BOLD + "\n>PUFSim: " + Style.END + "simulation of %s.sp is completed" % testbench)

    # Read .lis HSPICE output file and write simulation results into output.txt output file
    read_results()


if __name__ == "__main__":
    main()
