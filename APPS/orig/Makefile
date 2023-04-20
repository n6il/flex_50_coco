all: DMK MOVE
	@echo "Done"



DMKS = CC_FORTH.DMK DS_DF_CC.DMK STYCOCO.DMK cscfl_s1.DMK cscfl_s2.DMK

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: 1sec.dd $(DMKS)

1sec.dd:
	dd if=/dev/zero of=$@ bs=256 count=1	


CC_FORTH.DMK: CC_FORTH.DSK
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk

DS_DF_CC.DMK: DS_DF_CC.DSK
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk

STYCOCO.DMK: STYCOCO.DSK
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_35T.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk


cscfl_s1.DMK: cscfl_s1.dsk
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_40T.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk

cscfl_s2.DMK: cscfl_s2.dsk
	cat $< 1sec.dd > tmp.dsk
	hxcfe -uselayout:../../HxCFloppyEmulator/DiskLayout_FLEX_SSSD_40T.xml -finput:tmp.dsk -conv:TRS80_DMK -foutput:$@
	rm tmp.dsk


clean:
	rm -vf 1sec.dd tmp.dsk  *.DMK
