# Recreation of FHL Color Flex 5.0

This directory constains a recreation of Frank Hogg Labs 5.0

Two different versions of this recreation are contained in this package:

* `fhl_flex_5_0_recreation_fhlcolor_only.DMK`
* `fhl_flex_5_0_recreation.DMK`

This package also contains the source materials used to create
both disks:

* `Fhlcolor.DMK` -- Contains source and binaries of FHL CC FLEX 5.0
* `F502MSDP.DMK` -- Contains a FHL CC FLEX 5.0:2 System

## Booting up FHL Color Flex 5.0

To try out these disks use the XRoar emulator.

** IMPORTANT NOTE **
Please note that XRoar versions 1.3.1 or prior have a bug which will
corrupt DMK images.  At the time of writing this bug has been fixed
pushed to the XRoar `dev` branch but has not been released yet. 
Either use the latest version or make copies of the disks before using
them.  You have been warned.

1. Set your machine type to any CoCo
2. Insert `fhl_flex_5_0_recreation.DMK` into Drive 0
3. Start FLEX by typing `RUN "FLEX"`

## `fhl_flex_5_0_recreation_fhlcolor_only.DMK`

This disk contains only the contents found on `Fhlcolor.DMK`.  This disk was
not bootable but contained enough code to create a bootable disk from scratch.

The procedure was:

1. Boot up a FHL CC FLEX 5.0:4 system
2. Run `NEWDISK.BIN` from `Fhcolor` to create a blank disk
3. Run `PUTLDR.BIN <D>` from `Fhcolor`
4. Copy `FLEX.SYS` from `Fhcolor` to the new disk
5. Copy the remaining `.BIN` files to the new disk, renamed as `.CMD`
6. Place the new disk in Drive 0
7. Run `LINK FLEX.SYS`

The result of this procedure is a bootable FHL FLEX 5.0 disk created using
and containing the contents of the `Fhlcolor` disk.

NOTE:  This disk is mainly interesting for historical and/or research 
purposes.  The normal suite of FLEX utilities are NOT on this disk, so it
may be somewhat difficult to actually use this disk for anything other than
creating new boot disks.

## `fhl_flex_5_0_recreation.DMK`

This disk contains a minimum usable FLEX system.  Please remember that this
is a _recreation_ of what an original FHL CC FLEX 5.0 disk may have looked
like.  This disk starts with the
`fhl_flex_5_0_recreation_fhlcolor_only.DMK` disk and adds to it many of the
basic standard FLEX utilities from a later version of FLEX, 5.0:2.  Since
they are standard flex utilties it is probably unlikely that FHL had made
many changes to them in between releases.
