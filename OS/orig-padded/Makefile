all: DMK MOVE
	@echo "Done"


DMKS =  F502MSA.DMK F502MSD.DMK F502MSDP.DMK F502MSE.DMK F502MSEA.DMK F502MSFO.DMK F503MSA.DMK F503MSD.DMK F503MSDA.DMK F503MSDE.DMK F503MSE.DMK F503MSEA.DMK F503MSFO.DMK MASTR503.DMK

DMK: $(DMKS)

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: 1sec.dd $(DMKS)

1sec.dd:
	dd if=/dev/zero of=$@ bs=256 count=1	


%.DMK: %.DSK 1sec.dd
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSDD_34T_padding_removed.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk
	
clean:
	rm -vf 1sec.dd tmp.dsk  *.DMK
