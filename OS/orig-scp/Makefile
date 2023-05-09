all: DMK MVDMK MVIMA
	@echo "Done"

DMKS = fhl_flex_5_0_4_master.DMK
IMAS = fhl_flex_5_0_4_master.IMA

DMK: $(DMKS)

MVDMK: $(DMKS)
	mv $^ ../dmk

MVIMA: $(IMAS)
	mv $^ ../ima

%.DMK: %.IMA
	../../tools/dmk.py --flex --template ../../templates/BLANK_FLEX_SSDD35T.DMK --import $< --output $@

%.IMA: %.scp
	hxcfe -finput:$< -conv:RAW_LOADER -foutput:$@
	
clean:
	rm -vf *.DMK *.IMA
