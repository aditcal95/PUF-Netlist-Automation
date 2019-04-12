** Generated for: hspiceD
** Generated on: Dec  3 13:46:34 2017
** Design library name: myLib
** Design cell name: xor2_test
** Design view name: schematic
.INCLUDE "../finFET/DGPMOS.sp"
.INCLUDE "../finFET/DGNMOS.sp"
.INCLUDE "../subckt/inv.sp"
.INCLUDE "../subckt/xor2.sp"

.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 4.8e-9 START=0.0

** Library name: myLib
** Cell name: xor2_test
** View name: schematic
xi0 in_a in_b 0 out vdd xor2
v0 vdd 0 DC=1.2
v2 in_b 0 PULSE 0 1.2 0 30e-12 30e-12 2.4e-9 4.8e-9
v1 in_a 0 PULSE 0 1.2 0 30e-12 30e-12 1.2e-9 2.4e-9
.END
