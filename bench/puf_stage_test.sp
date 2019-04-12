** Generated for: hspiceD
** Generated on: Nov 30 17:45:20 2017
** Design library name: myLib
** Design cell name: puf_stage_test
** Design view name: schematic
.INCLUDE "../hw/netlist/finFET/DGPMOS.sp"
.INCLUDE "../hw/netlist/finFET/DGNMOS.sp"
.INCLUDE "../hw/netlist/subckt/inv.sp"
.INCLUDE "../hw/netlist/subckt/nand2.sp"
.INCLUDE "../hw/netlist/subckt/mux2x1.sp"
.INCLUDE "../hw/netlist/subckt/puf_stage.sp"


.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 4.8e-9 START=0.0


** Library name: myLib
** Cell name: puf_stage_test
** View name: schematic
xi0 0 net7 net7 net7 out_dn out_up vdd puf_stage
* ** Parameters of the upper MUX2x1
* +mup_inv_ppvth=0 mup_inv_npvth=0
* +mup_na_ppvth_lt=0 mup_na_ppvth_rt=0 mup_na_npvth_up=0 mup_na_npvth_dn=0
* +mup_nb_ppvth_lt=0 mup_nb_ppvth_rt=0 mup_nb_npvth_up=0 mup_nb_npvth_dn=0
* +mup_no_ppvth_lt=0 mup_no_ppvth_rt=0 mup_no_npvth_up=0 mup_no_npvth_dn=0

* ** Parameters of the lower MUX2x1
* +mdn_inv_ppvth=0 mdn_inv_npvth=0
* +mdn_na_ppvth_lt=0 mdn_na_ppvth_rt=0 mdn_na_npvth_up=0 mdn_na_npvth_dn=0
* +mdn_nb_ppvth_lt=0 mdn_nb_ppvth_rt=0 mdn_nb_npvth_up=0 mdn_nb_npvth_dn=0
* +mdn_no_ppvth_lt=0 mdn_no_ppvth_rt=0 mdn_no_npvth_up=0 mdn_no_npvth_dn=0

** Parameters of the upper MUX2x1
+mup_inv_ppvth=-0.25 mup_inv_npvth=0.29
+mup_na_ppvth_lt=-0.25 mup_na_ppvth_rt=-0.25 mup_na_npvth_up=0.29 mup_na_npvth_dn=0.29
+mup_nb_ppvth_lt=-0.25 mup_nb_ppvth_rt=-0.25 mup_nb_npvth_up=0.29 mup_nb_npvth_dn=0.29
+mup_no_ppvth_lt=-0.25 mup_no_ppvth_rt=-0.25 mup_no_npvth_up=0.29 mup_no_npvth_dn=0.29

** Parameters of the lower MUX2x1
+mdn_inv_ppvth=-0.25 mdn_inv_npvth=0.29
+mdn_na_ppvth_lt=-0.25 mdn_na_ppvth_rt=-0.25 mdn_na_npvth_up=0.29 mdn_na_npvth_dn=0.29
+mdn_nb_ppvth_lt=-0.25 mdn_nb_ppvth_rt=-0.25 mdn_nb_npvth_up=0.29 mdn_nb_npvth_dn=0.29
+mdn_no_ppvth_lt=-0.25 mdn_no_ppvth_rt=-0.25 mdn_no_npvth_up=0.29 mdn_no_npvth_dn=0.29

v0 vdd 0 DC=1.2
v1 net7 0 PULSE 0 1.2 0 30e-12 30e-12 1.2e-9 2.4e-9
.END
