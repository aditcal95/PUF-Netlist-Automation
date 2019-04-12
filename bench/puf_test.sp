** Generated for: hspiceD
** Generated on: Nov 30 16:56:14 2017
** Design library name: myLib
** Design cell name: puf4s_test
** Design view name: schematic
.INCLUDE "../hw/netlist/finFET/DGPMOS.sp"
.INCLUDE "../hw/netlist/finFET/DGNMOS.sp"
.INCLUDE "../hw/netlist/subckt/inv.sp"
.INCLUDE "../hw/netlist/subckt/nand2.sp"
.INCLUDE "../hw/netlist/subckt/mux2x1.sp"
.INCLUDE "../hw/netlist/subckt/puf_stage.sp"
.INCLUDE "../hw/netlist/subckt/sr_latch.sp"
.INCLUDE "../hw/netlist/puf.sp"
.VEC "puf_test.vec"


.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 4.8e-9 START=0.0


** Library name: myLib
** Cell name: puf4s_test
** View name: schematic
xi0 ch[0] ch[1] ch[2] 0 in_sig q net4 puf
v0 net4 0 DC=1.2

.END
