** Generated by pufgen.py for: hspiceD
** Generated on: 07/24/18 12:39:51
** Design library name: pufLib
** Design cell name: puf_test
** Design view name: schematic

.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/finFET/DGPMOS.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/finFET/DGNMOS.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/inv.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/nand2.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/mux2x1.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/puf_stage.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/sr_latch.sp"
.INCLUDE "C:\Users\Aditya\Desktop\PUF Research\PUFPy\scripts\pufpy/../../hw/netlist/subckt/xor2.sp"
.INCLUDE "puf_0.sp"
.TEMP 25.0
.OPTION
+    ARTIST=2
+    INGOLD=2
+    PARHIER=LOCAL
+    PSF=2
+    POST
.TRAN 10e-12 2.4e-09 START=0.0

** Library name: pufLib
** Cell name: puf_test
** View name: schematic
xi0 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd 0 vdd q vdd puf_0
v0 vdd 0 DC=1.2


.end

