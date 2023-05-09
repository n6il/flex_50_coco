all: DMK MOVE
	@echo "Done"


DMKS = CCSPELL.DMK

DMK: $(DMKS)

MOVE: $(DMKS)
	mv $^ ../dmk

DMK: $(DMKS)

%.DMK: %.DSK
	../../tools/dmk.py --flex --padding 18 --template ../../templates/BLANK_FLEX_SSDD35T.DMK --import $< --output $@
	
clean:
	rm -vf *.DMK
