#!/usr/local/bin/python
from __future__ import print_function
from datetime import datetime
import numpy as np
import os
import csv
import time
import math
import shutil
import argparse
import subprocess


OVERWRITE_SIM_DIR = True

# A list with all the netlists/files need to be included
INCLUDE_NETLISTS = ["finFET/DGPMOS.sp", "finFET/DGNMOS.sp", "subckt/inv.sp", "subckt/nand2.sp", "subckt/mux2x1.sp",
                    "subckt/puf_stage.sp", "subckt/sr_latch.sp", "subckt/xor2.sp"]

TEST_VECTOR_FILE = "../../bench/puf_test.vec"  # Test vector file name and path
TEMPERATURE_BASE = 25.0
VDD_NOMINAL = 1.2
VDD_STEP = 0.1
NUM_TRANSISTOR_STAGE = 28  # Number of transistors in each stage
PROCESS_VARIATION_MODEL = {"pmos_mean": -0.25, "pmos_sigma": 0.350, "nmos_mean": 0.29, "nmos_sigma": 0.325}


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


# A class for generating the PUF netlist and testbench
class PUFGenerator(object):
    def __init__(self, testbench_name, pufckt_name, num_stages, sim_stop, vdd_min, vdd_max, tmin, tmax, num_pufs,
                 num_challenges):
        self._testbench_name = testbench_name
        self._pufckt_name = pufckt_name
        self._num_stages = num_stages
        self._sim_stop = sim_stop
        self._sim_dir_path = ""
        self._vdd_min = vdd_min
        self._vdd_max = vdd_max
        self._tmin = tmin
        self._tmax = tmax
        self._num_pufs = num_pufs
        self._vt_values = []
        self._puf_stage_idx = 0
        self._num_challenges = num_challenges

    def create_sim_directory(self):
        if OVERWRITE_SIM_DIR:
            self._sim_dir_path = "../../hspice/sim_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "/"
        else:
            self._sim_dir_path = "../../hspice/sim_/"

        print("\n>PUFPy: Creating simulation directory: %s" % self._sim_dir_path)

        # If the directory already exists delete it
        if os.path.exists(self._sim_dir_path) and os.path.isdir(self._sim_dir_path):
            shutil.rmtree(self._sim_dir_path)

        # Create simulation directory
        os.mkdir(self._sim_dir_path)

    # A method for generating the requested netlist
    def generate_netlist(self):
        # Check if we have to generate several testbenches varying temperature and Vdd voltage
        if self._vdd_min == self._vdd_max and self._tmin == self._tmax:
            self._generate_test_subckt(self._testbench_name, self._sim_stop, self._vdd_min, self._tmin)
        else:
            # Else go through all the Vdd and temperature variations
            vdd = self._vdd_min
            while vdd < (self._vdd_max + VDD_STEP):
                for temperature in range(self._tmin, (self._tmax + TEMPERATURE_BASE), TEMPERATURE_BASE):
                    self._generate_test_subckt(("vdd" + str(vdd) + "v_t" + str(temperature) + "c_" +
                                                self._testbench_name), self._sim_stop,  vdd, temperature)
                vdd += VDD_STEP

        # Generate the requested number of PUF circuits
        for i in range(self._num_pufs):
            self._generate_puf_subckt(self._pufckt_name + "_" + str(i))

    # A method for generating testbench subcircuit netlist
    def _generate_test_subckt(self, testbench_name, sim_stop, vdd, temperature):
        print("\n>PUFPy: Generating PUF testbench %s.sp, Vdd: %.3fV, Temp.: %dC" % (testbench_name, vdd, temperature))

        # Write testbench's netlist header
        testbench_circuit = self._get_netlist_header(testbench_name)

        # Write testbench's include statements
        for netlist_name in INCLUDE_NETLISTS:
            testbench_circuit += ".INCLUDE \"" + os.getcwd() + "/../../hw/netlist/" + netlist_name + "\"\n"

        # Write PUF circuits include statements
        for i in range(self._num_pufs):
            testbench_circuit += ".INCLUDE \"" + self._pufckt_name + "_" + str(i) + ".sp" + "\"\n"

        # If we have more than one PUF circuits (cascaded mode) include and implement n-input XOR's gate circuit as well
        if self._num_pufs > 1:
            testbench_circuit += ".INCLUDE \"xor.sp\"\n"
            self._generate_xortree()

        # # Write test vector include statement
        # testbench_circuit += ".VEC \"puf_test.vec\"\n\n"

        # Write simulation options
        testbench_circuit += self._get_sim_options(str(temperature), sim_stop)

        # Write subcircuit's header
        testbench_circuit += self._get_subckt_header(testbench_name)

        # Write challenges input ports
        ch_ports = ""
        # for i in range(self._num_stages):
        #     ch_ports += " ch[" + str(i) + "]"
        # If number of challenges = 1 use the default pattern: 0x55.., otherwise test the all zeroes pattern
        for i in range(self._num_stages):
            if self._num_challenges == 1:
                if i % 2:
                    ch_ports += " vdd"
                else:
                    ch_ports += " 0"
            else:
                ch_ports += " 0"

        # Instantiate PUF circuit(s) and XOR tree gate if needed (cascaded mode)
        if self._num_pufs > 1:
            # Write PUFs' instantiation statements
            for i in range(self._num_pufs):
                testbench_circuit += "xi" + str(i) + ch_ports + " 0 vdd net" + str(i) + " vdd puf_" + str(i) + "\n"

            # Instantiate the n-input XOR tree subcircuit
            testbench_circuit += "xxor"

            # Connect PUFs' outputs to the XOR tree
            for i in range(self._num_pufs):
                testbench_circuit += " net" + str(i)

            # Connect the remaining input ports of the XOR tree to ground
            for i in range(self._calc_xor_inputs(self._num_pufs) - self._num_pufs):
                testbench_circuit += " 0"

            # Connect XOR's ground, output and Vdd voltage
            testbench_circuit += " 0 q vdd2 xor\n"
        else:
            testbench_circuit += "xi0" + ch_ports + " 0 vdd q" + " vdd puf_0\n"

        # Write voltage source's instantiation statement
        testbench_circuit += "v0 vdd 0 DC=" + str(vdd) + "\n\n"

        # Power the XOR tree subcircuit with the nominal Vdd
        if self._num_pufs > 1:
            testbench_circuit += "v1 vdd2 0 DC=" + str(VDD_NOMINAL) + "\n\n"

        # Use alter HSPICE feature to examine the requested number of challenges
        if self._num_challenges > 1:
            # Also write challenges in the output file
            with open(self._sim_dir_path + "challenges.txt", "w") as challenges_file:
                for i in range(self._num_challenges-1):
                    testbench_circuit += ".alter case " + str(i+1) + ":\n"
                    ch_ports = '%0*d' % (self._num_stages, int(bin(i+1)[2:]))
                    ch_ports = " ".join(ch_ports)

                    # Write challenges into the challenges.txt
                    challenges_file.write(ch_ports + "\n")

                    # Replace ones with vdd
                    ch_ports = ch_ports.replace("1", "vdd")
                    testbench_circuit += "xi0 " + ch_ports + " 0 vdd q" + " vdd puf_0\n"

        # Finish the description of the netlist
        testbench_circuit += "\n.end\n\n"

        # Write the testbench description into the netlist file
        with open(self._sim_dir_path + testbench_name + ".sp", "w") as netlist_file:
            netlist_file.write(testbench_circuit)

    # A method for generating PUF subcircuit netlist
    def _generate_puf_subckt(self, pufckt_name):
        print("\n>PUFPy: Generating PUF subcircuit %s.sp, number of stages %d" % (pufckt_name, self._num_stages))

        # Write PUF's netlist header
        puf_subckt = self._get_netlist_header(pufckt_name)

        # Write the header of the PUF subcircuit
        puf_subckt += self._get_subckt_header(pufckt_name)
        puf_subckt += ".subckt " + pufckt_name
        for i in range(self._num_stages):
            puf_subckt += " ch_" + str(i)
        puf_subckt += " gnd in_sig q vdd\n"

        # PUF stage connection indexes
        connections = [0, 1, 2, 3]

        # Create PUF stages
        for i in range(self._num_stages):
            puf_subckt += "** " + str(i+1) + " PUF stage\n"
            # If it is the first stage connect in_sig signal with the input ports of the first PUF stage
            if i == 0:
                puf_subckt += "xi" + str(i) + " gnd in_sig in_sig ch_" + str(i) + " net" + str(connections[2]) + " net"\
                              + str(connections[3]) + " vdd puf_stage\n"
            else:
                puf_subckt += "xi" + str(i) + " gnd net" + str(connections[0]) + " net" + str(connections[1]) + " ch_"\
                              + str(i) + " net" + str(connections[2]) + " net" + str(connections[3]) \
                              + " vdd puf_stage\n"

            # Write PUF's Vt parameters considering all stages and PUF slices
            puf_subckt += self._get_vt_parameters()

            # Increase by two all the connection indexes
            for j in range(4):
                connections[j] += 2

            puf_subckt += "**\n\n"

        # Write the SR latch
        puf_subckt += "** SR latch\n" \
                      "xi" + str(self._num_stages) + " gnd q net" + str(connections[1]+1) + " net" \
                      + str(connections[0]) + " net" + str(connections[1]) + " vdd sr_latch\n"

        puf_subckt += ".ends " + pufckt_name + "\n"
        puf_subckt += "** End of subcircuit definition\n\n"

        # Finish the description of the netlist
        puf_subckt += ".end\n\n"

        # Write the PUF's circuit description into the netlist file
        with open(self._sim_dir_path + pufckt_name + ".sp", "w") as netlist_file:
            netlist_file.write(puf_subckt)

    # A method for generating XOR tree subcircuit
    def _generate_xortree(self):
        # Calculate the number of inputs based on the number of PUF circuits
        num_inputs = self._calc_xor_inputs(self._num_pufs)

        # Calculate the height of the XOR tree
        tree_height = int(math.log(num_inputs, 2))

        print("\n>PUFPy: Generating XOR tree subcircuit, inputs ports: %d, tree height: %d" % (num_inputs, tree_height))

        # Write the header of the XOR tree netlist
        xortree_subckt = self._get_netlist_header("xor")

        # Write the header of the XOR tree subcircuit
        xortree_subckt += self._get_subckt_header("xor")
        xortree_subckt += ".subckt xor"
        for i in range(num_inputs):
            xortree_subckt += " in_" + str(i)
        xortree_subckt += " gnd out vdd\n"

        # Number of nodes in each tree-level
        level_nodes = num_inputs / 2
        for i in range(tree_height):
            for j in range(level_nodes):
                if i == 0:
                    xortree_subckt += "xi" + str(i) + str(j) + " in_" + str(j * 2) + " in_" + str((j * 2) + 1) \
                                      + " gnd net" + str(i) + str(j) + " vdd xor2\n"
                elif i == (tree_height - 1):
                    xortree_subckt += "xi" + str(i) + str(j) + " net" + str(i - 1) + str(j * 2) + " net" + str(i - 1) \
                                      + str((j * 2) + 1) + " gnd out vdd xor2\n"
                else:
                    xortree_subckt += "xi" + str(i) + str(j) + " net" + str(i - 1) + str(j * 2) + " net" + str(i - 1) \
                                      + str((j * 2) + 1) + " gnd net" + str(i) + str(j) + " vdd xor2\n"

            level_nodes /= 2

        xortree_subckt += ".ends xor\n"
        xortree_subckt += "** End of subcircuit definition\n\n"

        # Finish the description of the netlist
        xortree_subckt += ".end\n\n"

        # Write the circuit description of the XOR tree into the netlist file
        with open(self._sim_dir_path + "xor.sp", "w") as netlist_file:
            netlist_file.write(xortree_subckt)

    # A method for calculating the number of XOR's input ports
    def _calc_xor_inputs(self, requested_inputs):
        if requested_inputs < 2:
            return 2
        else:
            nearest_power = math.ceil(math.log(requested_inputs, 2))
            return int(2**nearest_power)

    # A method for writing PUF's parameters (threshold voltage)
    def _get_vt_parameters(self):
        # Read voltage threshold values from vt_values.csv file
        if not self._vt_values:
            with open("vt_values.csv", "rb") as vt_value_file:
                reader = csv.reader(vt_value_file)
                self._vt_values = list(reader)

        # Get the Vt values of the requested PUF stage
        puf_stage_vt = []
        try:
            puf_stage_vt = self._vt_values[self._puf_stage_idx]
            self._puf_stage_idx += 1
        except IndexError:
            print(Style.RED + "\n>[ERROR]" + Style.END + " Not enough vt values, run PUFPy with -Vt switch to generate "
                  "a new vt_values.csv file to reflect the latest PUF design")
            quit()

        # Write the Vt values of the requested PUF stage
        vt_parameters = \
            "** Vt parameters of the upper MUX2x1\n" \
            "+mup_inv_ppvth=%s mup_inv_npvth=%s\n" \
            "+mup_na_ppvth_lt=%s mup_na_ppvth_rt=%s mup_na_npvth_up=%s mup_na_npvth_dn=%s\n" \
            "+mup_nb_ppvth_lt=%s mup_nb_ppvth_rt=%s mup_nb_npvth_up=%s mup_nb_npvth_dn=%s\n" \
            "+mup_no_ppvth_lt=%s mup_no_ppvth_rt=%s mup_no_npvth_up=%s mup_no_npvth_dn=%s\n\n" \
            "** Vt parameters of the lower MUX2x1\n" \
            "+mdn_inv_ppvth=%s mdn_inv_npvth=%s\n" \
            "+mdn_na_ppvth_lt=%s mdn_na_ppvth_rt=%s mdn_na_npvth_up=%s mdn_na_npvth_dn=%s\n" \
            "+mdn_nb_ppvth_lt=%s mdn_nb_ppvth_rt=%s mdn_nb_npvth_up=%s mdn_nb_npvth_dn=%s\n" \
            "+mdn_no_ppvth_lt=%s mdn_no_ppvth_rt=%s mdn_no_npvth_up=%s mdn_no_npvth_dn=%s\n" %\
            (puf_stage_vt[0],  puf_stage_vt[14],
             puf_stage_vt[1],  puf_stage_vt[2],  puf_stage_vt[15], puf_stage_vt[16],
             puf_stage_vt[3],  puf_stage_vt[4],  puf_stage_vt[17], puf_stage_vt[18],
             puf_stage_vt[5],  puf_stage_vt[6],  puf_stage_vt[19], puf_stage_vt[20],
             puf_stage_vt[7],  puf_stage_vt[21],
             puf_stage_vt[8],  puf_stage_vt[9],  puf_stage_vt[22], puf_stage_vt[23],
             puf_stage_vt[10], puf_stage_vt[11], puf_stage_vt[24], puf_stage_vt[25],
             puf_stage_vt[12], puf_stage_vt[13], puf_stage_vt[26], puf_stage_vt[27])

        return vt_parameters

    # A method for writing netlist's header
    def _get_netlist_header(self, name):
        netlist_header = \
            "** Generated by pufgen.py for: hspiceD\n" \
            "** Generated on: %s\n" % time.strftime("%c") +\
            "** Design library name: pufLib\n" \
            "** Design cell name: %s\n" % name +\
            "** Design view name: schematic\n\n"
        return netlist_header

    # A method for writing subcircuits header
    def _get_subckt_header(self, name):
        subckt_header = \
            "** Library name: pufLib\n" \
            "** Cell name: %s\n" % name + \
            "** View name: schematic\n"
        return subckt_header

    # A method for writing general options of the simulation
    def _get_sim_options(self, temperature="25.0", sim_stop_time="2.4e-9", sim_start_time="0.0", sim_step_time="10e-12"):
        sim_options = \
            ".TEMP %s\n" % temperature + \
            ".OPTION\n" \
            "+    ARTIST=2\n" \
            "+    INGOLD=2\n" \
            "+    PARHIER=LOCAL\n" \
            "+    PSF=2\n" \
            "+    POST\n" \
            ".TRAN %s %s START=%s\n\n" % (sim_step_time, sim_stop_time, sim_start_time)
        return sim_options

    # Get simulation directory path
    def get_sim_directory_path(self):
        return self._sim_dir_path


# Helper functions

# A function for copying files
def copy_file(src, dst):
    print("\n>PUFPy: Copying %s file to %s" % (src, dst))
    try:
        shutil.copy2(src, dst)
    except IOError:
        print(Style.RED + "\n[ERROR]" + Style.END + " File %s not found" % TEST_VECTOR_FILE)
        quit()


# A function for running hspice simulations
def run_simulation(sim_directory_path, mthreaded):
    print(Style.GREEN + "\n>PUFPy: " + Style.END +
          "Invoking pufsim.py in directory %s to start simulating the generated PUF" % sim_directory_path)
    try:
        # Invoke pufsim.py to simulate the circuit
        process = subprocess.Popen([sim_directory_path + "pufsim.py", "-mt", str(mthreaded)], stdin=subprocess.PIPE,
                                   cwd=sim_directory_path)
        process.communicate("\r")
    except:
        print(Style.RED + "\n[ERROR]" + Style.END + " subprocess.py raised an exception while attempting to invoke"
              " pufsim.py")


# A function for generating threshold voltages variations
def generate_vt_values(num_puf_stages=1):
    print("\n>PUFPy: Creating threshold voltage values for %d PUF stages" % num_puf_stages)
    print(">PUFPy: Using normal distribution, PMOS: Mean=%.3fV and Sigma=%.3fV, NMOS:Mean=%.3fV and Sigma=%.3fV" %
          (PROCESS_VARIATION_MODEL["pmos_mean"], PROCESS_VARIATION_MODEL["pmos_sigma"],
           PROCESS_VARIATION_MODEL["nmos_mean"], PROCESS_VARIATION_MODEL["nmos_sigma"]))

    vt_values_stage = []
    for i in range(num_puf_stages):
        # Following normal distribution get a voltage threshold value for every transistor of a PUF stage, consider
        # different mean values and standard deviations for PMOS and NMOS
        pmos_vt = np.random.normal(PROCESS_VARIATION_MODEL["pmos_mean"], PROCESS_VARIATION_MODEL["pmos_sigma"],
                                   NUM_TRANSISTOR_STAGE / 2)
        nmos_vt = np.random.normal(PROCESS_VARIATION_MODEL["nmos_mean"], PROCESS_VARIATION_MODEL["nmos_sigma"],
                                   NUM_TRANSISTOR_STAGE / 2)

        # Concatenate the two lists and ensure Vt<0 for PMOS and Vt>0 for NMOS, not sure if we want this behaviours...
        vt_values_stage.append(list(-abs(pmos_vt)) + list(abs(nmos_vt)))

        # Round all values to 3 decimal places
        vt_values_stage[i] = ["%.3f" % x for x in vt_values_stage[i]]

    # Write voltage threshold values to CSV file vt_values.csv
    with open("vt_values.csv", "w") as vt_values_file:
        writer = csv.writer(vt_values_file)
        writer.writerows(vt_values_stage)


# ==============================
# Main program
# ==============================
def main():
    # Instantiate the command line parser
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument("num_puf_stages", type=int,
                        help="Required the number of PUF stages")
    parser.add_argument("-s", "--simulate", action="store_true",
                        help="Invoke pufsim.py to simulate the circuit")
    parser.add_argument("-sstop", "--sim_stop", type=float, default=2.4e-9,
                        help="Define the duration of the transient analysis")
    parser.add_argument("-mt", "--mthreaded", type=int, default=8,
                        help="Enable multi-threaded simulation and define number of available processors")
    parser.add_argument("-vmin", "--vdd_min", type=float, default=VDD_NOMINAL,
                        help="Define minimum/maximum Temperature range to simulate the circuit")
    parser.add_argument("-vmax", "--vdd_max", type=float, default=VDD_NOMINAL,
                        help="Define minimum/maximum Temperature range to simulate the circuit")
    parser.add_argument("-tmin", "--temp_min", type=int, default=TEMPERATURE_BASE,
                        help="Define minimum/maximum Vdd range to simulate the circuit")
    parser.add_argument("-tmax", "--temp_max", type=int, default=TEMPERATURE_BASE,
                        help="Define minimum/maximum Vdd range to simulate the circuit")
    parser.add_argument("-c", "--cascade", type=int, default=1,
                        help="Define the number of cascade PUFs")
    parser.add_argument("-vt", "--vthreshold", action="store_true",
                        help="Generate new threshold voltage values for all the PUF stages including cascaded layers")
    parser.add_argument("-ch", "--challenges", type=int, default=1,
                        help="Define the number of challenges to be tested")

    # Parse command line options
    args = parser.parse_args()

    print(Style.BOLD + "\n>PUFPy: a tool for generating arbiter based PUFs" + Style.END)

    # Instantiate PUF generator
    puf_generator = PUFGenerator("puf_test", "puf", args.num_puf_stages, args.sim_stop, args.vdd_min, args.vdd_max,
                                 args.temp_min, args.temp_max, args.cascade, args.challenges)
    # puf_generator = PUFGenerator("puf_test", "puf", args.num_puf_stages, 0.1, 1.4, args.temp_min, args.temp_max)
    # puf_generator = PUFGenerator("puf_test", "puf", args.num_puf_stages, args.vdd_min, args.vdd_max, -25, 100)
    # puf_generator = PUFGenerator("puf_test", "puf", args.num_puf_stages, 0.1, 1.4, -25, 100)

    # Create PUF's simulation directory
    puf_generator.create_sim_directory()

    # Generate threshold voltage values for all the PUF stages including cascaded layers
    if args.vthreshold:
        generate_vt_values(args.cascade * args.num_puf_stages)

    # Generate PUF netlists
    puf_generator.generate_netlist()

    # # Copy test vector file into the simulation directory
    # copy_file(TEST_VECTOR_FILE, puf_generator.get_sim_directory_path())

    # Copy pufsim.py script into the simulation directory
    copy_file("pufsim.py", puf_generator.get_sim_directory_path())

    # If simulation switch is define call run_simulation() method to simulate the PUF circuit
    if args.simulate:
        run_simulation(puf_generator.get_sim_directory_path(), args.mthreaded)


if __name__ == "__main__":
    main()
