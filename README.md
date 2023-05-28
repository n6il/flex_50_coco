# FHL FLEX 5.0 For the Tandy/TRS-80 Color Computer

## Contents

This package has the following directories:

    OS
    OS/ima
    OS/sdf
    OS/dmk
    OS/orig-padded
    OS/orig-scp
    APPS
    APPS/ima
    APPS/sdf
    APPS/dmk
    APPS/orig-padded
    APPS/orig-scp
    APPS/orig
    SRC
    SRC/sdf
    SRC/dmk
    SRC/orig-padded

* `OS` -- Contains the FLEX OS Disks
* `APPS` -- Contains Applications
* `SRC` -- Contains FLEX Source Code

Each of these directores has the following:

* `orig` -- Original DSK iamges
* `orig-padded` -- Original "Padded" DSK Images (additional padding sectors in track 0)
* `orig-scp` -- Original SCP Images (images of physical floppies)

The following ready-to-use binaries are available:

* `dmk` -- DMK images of the disks.  These can be used for writing to physical disks or in emulators such as XRoar or David Keil's CoCo 2 emulator.
* `sdf` -- SDF images for CoCo SDC
* `ima` -- IMA images for SWTPCemu

## Building Requirements

Both tools must be in the current PATH

* `hxcfe` -- HxCFloppyEmulator command line tool - NOTE: Must be Version 2.14.6.4 or later
* `dmk2sdf` -- DMK to SDF conversion utility

## Building

    cd flex_50_coco
    make

## History

The FLEX operating system was originally released in May 1978 for MC6800 based systems.  The MC6809 CPU was released in 1978 but systems contining the new CPU weren't widely available until SWTPC and GIMIX and the TRS-80 Color Computer were all released in 1980.  Microware's OS-9 also came about around 1980.  This means that FLEX pre-dates OS-9 by 2-3 years.  Ultimately FLEX started to slowly die off after the release of the Color Computer OS-9 in 1983.  Despite this OS-9 survived and continued on into the late 1990's.

The Frank Hogg version of FLEX 5.0 for the Color Computer came out around March 1982.  FHL placed very aggressive ads in 68 Micro Journal and Rainbow Magazine setting up for a battle between FLEX and OS-9.

## Provenance

The origin of the disks used in this project are unknown.  the FLEX OS and Application disks are all backup copies of the master disks.  There aren't any images of the original master disks known to exist.   The images were all obtained from the FuFu (FLEX/UniFLEX User Group) archives.  A package of similar disk images is also on the Color Computer Archive.

## FLEX Disk Formats -- Technical Details

FLEX on the Color Computer uses the traditional FLEX Disk Formats:

A Single-Density disk has the formatting:

       Track 0-n: Single Density -- 10 Sectors of 256 Bytes
    
A Double-Density disk has the formatting:

       Track 0: Single Density -- 10 Sectors of 256 Bytes
    Tracks 1-n: Double Density -- 18 Sectors of 256 Bytes

Both formats can be up to 40 tracks and single- or double-sided.  On Double-sided disks sectors are numbered continuously across both sides:

Density | Head 0 | Head 1
---|---|---
Single | Sectors 1-10 | Sectors 11-20
Double | Sectors 1-18 | Sectors 19-36

CoCo FLEX will refuse to read any disk which does not have Single-Density formatting on Track 0

## Disk Image Conversion Process

The disk images are of various formats.  The Operating System disks are what is called a sector "padded" disk image.  These padded disk images remove the original formatting of the original disks:

    Tracks 0-n: Double Density -- 18 Sectors of 256 Bytes

Unfortunately it's impossible to fit 18-sectors in a Single-density track.  This project utilizes a few hacks to remove the 8 extra sectors from track 0 and to restore the single density formatting:

1. Custom XML layout files for the HxCFloppyEmulator tools were generated which skip over the padding sectors and restore single-density formatting on track 0
2. `hxcfe` tool converts the original sector images to DMK format images.  The DMK iamges can be used to create physical floppies or can also be used in XRoar or David Keil's Coco emulator.
3. `dmk2sdf` tool is used to convert the DMK images to SDF format used on the CoCo SDC.
