** Generated for: hspiceD
** Generated on: Nov 29 21:11:56 2017
** Design library name: myLib
** Design cell name: nand2_test
** Design view name: schematic
.INCLUDE "../hw/netlist/finFET/DGPMOS.sp"
.INCLUDE "../hw/netlist/finFET/DGNMOS.sp"
.INCLUDE "../hw/netlist/subckt/nand2.sp"


.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 4.8e-9 START=0.0

** Library name: myLib
** Cell name: nand2_test
** View name: schematic
xi1 0 net6 net7 out net5 nand2 ppvth_lt=-0.25 ppvth_rt=-0.25 npvth_up=0.29 npvth_dn=0.29
v0 net5 0 DC=1.2
v2 net7 0 PULSE 0 1.2 0 30e-12 30e-12 600e-12 1.2e-9
v1 net6 0 PULSE 0 1.2 0 30e-12 30e-12 1.2e-9 2.4e-9
.END
