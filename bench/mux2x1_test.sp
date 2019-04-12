** Generated for: hspiceD
** Generated on: Nov 29 16:20:05 2017
** Design library name: myLib
** Design cell name: mux2x1_test
** Design view name: schematic
.INCLUDE "../hw/netlist/finFET/DGPMOS.sp"
.INCLUDE "../hw/netlist/finFET/DGNMOS.sp"
.INCLUDE "../hw/netlist/subckt/inv.sp"
.INCLUDE "../hw/netlist/subckt/nand2.sp"
.INCLUDE "../hw/netlist/subckt/mux2x1.sp"


.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 9.6e-9 START=0.0


** Library name: myLib
** Cell name: mux2x1_test
** View name: schematic
* xi68 0 in_a in_b in_s out vdd mux2x1 inv_ppvth=0 inv_npvth=0
* +na_ppvth_lt=0 na_ppvth_rt=0 na_npvth_up=0 na_npvth_dn=0
* +nb_ppvth_lt=0 nb_ppvth_rt=0 nb_npvth_up=0 nb_npvth_dn=0
* +no_ppvth_lt=0 no_ppvth_rt=0 no_npvth_up=0 no_npvth_dn=0
xi68 0 in_a in_b in_s out vdd mux2x1 inv_ppvth=-0.25 inv_npvth=0.29
+na_ppvth_lt=-0.25 na_ppvth_rt=-0.25 na_npvth_up=0.29 na_npvth_dn=0.29
+nb_ppvth_lt=-0.25 nb_ppvth_rt=-0.25 nb_npvth_up=0.29 nb_npvth_dn=0.29
+no_ppvth_lt=-0.25 no_ppvth_rt=-0.25 no_npvth_up=0.29 no_npvth_dn=0.29
v0 vdd 0 DC=1.2
v3 in_s 0 PULSE 0 1.2 0 30e-12 30e-12 4.8e-9 9.6e-9
v2 in_b 0 PULSE 0 1.2 0 30e-12 30e-12 2.4e-9 4.8e-9
v1 in_a 0 PULSE 0 1.2 0 30e-12 30e-12 1.2e-9 2.4e-9
c0 out 0 7e-15

.END
