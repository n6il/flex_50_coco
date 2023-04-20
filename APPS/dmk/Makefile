all: SDF MOVE
	@echo "Done"


SDFS = CCSPELL.SDF CC_FORTH.SDF DS_DF_CC.SDF STYCOCO.SDF cscfl_s1.SDF cscfl_s2.SDF

SDF: $(SDFS)

MOVE: $(SDFS)
	mv $^ ../sdf

%.SDF: %.DMK
	dmk2sdf $< -o $@
	
clean:
	rm -vf *.DMK *.SDF
