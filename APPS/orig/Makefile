all: DMK MOVE
	@echo "Done"



DMKS = CC_FORTH.DMK DS_DF_CC.DMK STYCOCO.DMK cscfl_s1.DMK cscfl_s2.DMK

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: $(DMKS)

CC_FORTH.DMK: CC_FORTH.DSK
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:$< -conv:TRS80_DMK -foutput:$@

DS_DF_CC.DMK: DS_DF_CC.DSK
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:$< -conv:TRS80_DMK -foutput:$@

STYCOCO.DMK: STYCOCO.DSK
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:$< -conv:TRS80_DMK -foutput:$@


cscfl_s1.DMK: cscfl_s1.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_40T.xml -finput:$< -conv:TRS80_DMK -foutput:$@

cscfl_s2.DMK: cscfl_s2.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_40T.xml -finput:$< -conv:TRS80_DMK -foutput:$@


clean:
	rm -vf *.DMK
