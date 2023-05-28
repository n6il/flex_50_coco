import xml.etree.ElementTree as ET
from collections import OrderedDict

def appendMultiple(obj, nodes):
    for tag, text in nodes:
        e = ET.SubElement(obj, tag)
        e.text = text

def getTrack(obj, tn, sn, fmt, offset, ell=None):
    attribs = OrderedDict( {'track_number':'%02d'%tn, 'side_number':'%s'%sn} )
    e = ET.SubElement(obj, 'track', attrib=attribs)
    el = (('data_offset', '0x%06x'%offset), ('format', fmt))
    if ell:
        el += ell
    appendMultiple(e, el)
    return e

def getSector(obj, si, ss, offset, ell=None):
    attribs=OrderedDict({'sector_id':'%02d'%si, 'sector_size':'%s'%ss})
    e = ET.SubElement(obj, 'sector', attrib=attribs)
    el = (('data_fill', '0x00'), ('datamark', '0xFB'), ('data_offset', '0x%06x'%offset))
    if ell:
        el += ell
    appendMultiple(e, el)
    return e


tracks = 34
spt = 18
sides = 1
interleave = True
if interleave:
    sectors_track_0 = (1,4,7,10,3,6,9,2,5,8)
    sectors_track = (1,11,4,14,7,10,3,13,6,9,2,12,5,15,8)
else:
    sectors_track_0 = range(1,11)
    sectors_track = range(1,spt+1)
sector_len = 256
padded = False
flex = True

if padded:
    # padded
    file_size = sides * (len(sectors_track) * (tracks) * sector_len)
else:
    # not padded
    file_size =  sides * (len(sectors_track_0) * sector_len  + len(sectors_track) * (tracks - 1) * sector_len)

# disk_layout
dl = ET.Element('disk_layout')

sideStr = "DS" if sides==2 else "SS"
densStr = "DD" if spt==18 else "SD"
kStr = "%s" % (file_size // 1024)
padStr = "_padding_removed" if padded else ""
layout_name = 'FLEX_%s%s_%sT_%sKB%s' % (sideStr, densStr, tracks, kStr, padStr)
dl_nodes = (
        ('disk_layout_name', layout_name),
        ('disk_layout_description', layout_name),
        ('prefered_file_extension', 'dsk'),
        ('interface_mode', 'GENERIC_SHUGART_DD_FLOPPYMODE'),
        ('file_size', "%d" % file_size),
    )
appendMultiple(dl, dl_nodes)

la = ET.SubElement(dl,'layout')

la_nodes = (
        ('number_of_track', "%s" % tracks),
        ('number_of_side', "%s" % sides),
        ('format', 'IBM_FM'),
        ('start_sector_id', '1'),
        ('sector_per_track', '10'),
        ('sector_size', "%s" % sector_len),
        ('formatvalue', '0'),
        ('gap3', '255'),
        ('bitrate', '250000')
    )
appendMultiple(la, la_nodes)
_ = ET.Comment('FM tracks : <interleave>4</interleave>')
la.append(_)
_ = ET.Comment('MFM tracks : <interleave>6</interleave>')
la.append(_)
la_nodes = (
        ('pregap', '0'),
        ('rpm', '300')
        )
appendMultiple(la, la_nodes)

tl = ET.SubElement(la,'track_list')
#la.append(tl)

# track 0
track = 0
offset = 0

skip = 0
for side in range(sides):
    t = getTrack(tl, track, side, 'IBM_FM', offset)
    #ell = (('pregap', '20'), ('gap3', '11'))
    #t = getTrack(tl, track, side, 'IBM_FM', offset, ell)

    sl = ET.SubElement(t, 'sector_list')

    for sector in sectors_track_0:
        if flex:
            phys_sector = sector + side * len(sectors_track_0)
        else:
            phys_sector = sector
        soffset = offset + ((track * len(sectors_track_0)) + (sector - 1)) * sector_len
        s = getSector(sl, phys_sector, sector_len, soffset)

    offset += len(sectors_track_0) * sector_len
    if padded:
        # hack to skipp padding
        padding_len = len(sectors_track) - len(sectors_track_0)
        if flex:
            # Accumulate 8 sectors which will need to be skipped
            # later - See note below
            skip += padding_len * sector_len
        else:
            # Non-Flex
            # Sectors on both sides of the disk are numbered the same, 1-n
            # The padding sectors n+1, n+2, etc. appear at the end of each side
            offset += padding_len * sector_len

if flex:
    # For FLEX -
    # On double sided FLEX disks, the sectors are numbered
    # 1-m on side 0
    # and m+1 - n on side 1
    # The padding sectors to be skipped are n+1, n+2, etc. so they
    # are at the end of side 1 of the track.
    # Skip is the total number of bytes which need to be skipped.
    offset += skip


for side in range(sides):
    for track in range(1,tracks):
        t = getTrack(tl, track, side, 'IBM_MFM', offset)
        sl = ET.SubElement(t, 'sector_list')

        for sector in sectors_track:
            phys_sector = sector + side * len(sectors_track)
            soffset = offset + ((sector - 1) * sector_len)
            s = getSector(sl, phys_sector, sector_len, soffset)
        offset += len(sectors_track) * sector_len


ET.indent(dl)
f=open('test-%s.xml'%layout_name, 'w')
f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
f.write('<!-- HxC Floppy Emulator Disk Layout -->\n')
f.write(ET.tostring(dl, encoding='unicode'))
