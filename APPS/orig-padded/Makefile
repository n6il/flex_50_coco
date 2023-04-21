all: DMK MOVE
	@echo "Done"


DMKS = CCSPELL.DMK

DMK: $(DMKS)

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: $(DMKS)

%.DMK: %.DSK
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSDD_35T_padding_removed.xml -finput:$< -conv:TRS80_DMK -foutput:$@
	
clean:
	rm -vf *.DMK
