all: DMK MOVE
	@echo "Done"

DMKS = F502MSA.DMK F502MSD.DMK F502MSDP.DMK F502MSE.DMK F502MSEA.DMK F502MSFO.DMK F503MSA.DMK F503MSD.DMK F503MSDA.DMK F503MSDE.DMK F503MSE.DMK F503MSEA.DMK F503MSFO.DMK MASTR503.DMK

DMK: $(DMKS)

MOVE: $(DMKS)
	mv $^ ../dmk

%.DMK: %.DSK
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSDD_34T_padding_removed.xml -finput:$< -conv:TRS80_DMK -foutput:$@
	
clean:
	rm -vf *.DMK
