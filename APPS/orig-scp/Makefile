all: DMK MVDMK MVIMA
	@echo "Done"

DMKS = fhl_color_utilities.DMK fhl_ed.DMK fhl_extended_basic.DMK
IMAS = fhl_color_utilities.IMA fhl_ed.IMA fhl_extended_basic.IMA

DMK: $(DMKS)

IMA: $(IMAS)

MVDMK: $(DMKS)
	mv $^ ../dmk

MVIMA: $(IMAS)
	mv $^ ../ima

fhl_color_utilities.DMK: fhl_color_utilities.IMA
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD6T.DMK --import $< --output $@

fhl_ed.DMK: fhl_ed.IMA
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD12T.DMK --import $< --output $@

fhl_extended_basic.DMK: fhl_extended_basic.IMA
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSSD35T.DMK --import $< --output $@

%.IMA: %.scp
	hxcfe -finput:$< -conv:RAW_LOADER -foutput:$@
	
clean:
	rm -vf *.DMK *.IMA
