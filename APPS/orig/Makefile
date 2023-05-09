all: DMK MOVE
	@echo "Done"



DMKS = CC_FORTH.DMK DS_DF_CC.DMK STYCOCO.DMK cscfl_s1.DMK cscfl_s2.DMK

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: $(DMKS)

CC_FORTH.DMK: CC_FORTH.DSK
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD35T.DMK --import $< --output $@

DS_DF_CC.DMK: DS_DF_CC.DSK
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD35T.DMK --import $< --output $@

STYCOCO.DMK: STYCOCO.DSK
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD35T.DMK --import $< --output $@


cscfl_s1.DMK: cscfl_s1.dsk
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD40T.DMK --import $< --output $@

cscfl_s2.DMK: cscfl_s2.dsk
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD40T.DMK --import $< --output $@


clean:
	rm -vf *.DMK
