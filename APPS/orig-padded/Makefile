all: DMK MOVE
	@echo "Done"


DMKS = CCSPELL.DMK

DMK: $(DMKS)

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: 1sec.dd $(DMKS)

1sec.dd:
	dd if=/dev/zero of=$@ bs=256 count=1	


%.DMK: %.DSK 1sec.dd
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSDD_35T_padding_removed.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk
	
clean:
	rm -vf 1sec.dd tmp.dsk  *.DMK
