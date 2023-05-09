all: SDF MOVE
	@echo "Done"


SDFS = CCSPELL.SDF CC_FORTH.SDF DS_DF_CC.SDF STYCOCO.SDF cscfl_s1.SDF cscfl_s2.SDF fhl_color_utilities.SDF fhl_ed.SDF fhl_extended_basic.SDF

SDF: $(SDFS)

MOVE: $(SDFS)
	mv $^ ../sdf

%.SDF: %.DMK
	dmk2sdf $< -o $@
	
clean:
	rm -vf *.DMK *.SDF
