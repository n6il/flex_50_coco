#!/usr/bin/python3

import sys
from struct import *
import pprint
from binascii import crc_hqx
import argparse
import shutil
import os

def strDdup(s):
        r = []
        for i in range(len(s)):
            if not i&1:
                r.append(s[i])
        return bytes(r)

def strDup(s):
    r=[]
    for c in s:
        r += [c,c]
    return bytes(r)


class DMK:
    def __init__(self, fn):
        self.f = open(fn, 'rb+')
        self.parse()

    def tracks(self):
        return(self.dmk['track_data'].keys())

    def sides(self, track):
        return(self.dmk['track_data'][track].keys())

    def numSectors(self, track, sides):
        return(self.dmk['track_data'][track][sides]['num_sectors'])

    def sectors(self, track, sides):
        return(self.dmk['track_data'][track][sides]['sectors'].keys())

    def getSector(self, track, side, sector):
        trk = self.dmk['track_data'][track][side]
        sector = trk['sectors'][sector]
        return(sector)

    def readSector(self, track, side, sector):
        sectorData = self.getSector(track, side, sector)

        #  FM: SYNC($00x3) + DAM($FB) + DATA(sectorlen) + CRC(uint16)
        #      CRC: DAM + DATA
        #      Reminder: in DMK FM Single Density Bytes are doubled
        # MFM: SYNC($A1x3) + DAM($FB)  + DATA(sectorlen) + CRC(uint16)
        #      CRC: SYNC + DAM + DATA

        # Density Multiplier
        if sectorData['density']:
            # Double Density
            mult=1
        else:
            # Single Density - bytes are doubled
            mult=2

        # Seek to DAM-3 - points to the 3 sync bytes
        self.f.seek(sectorData['dam_foffset']-(3*mult),0)
        # Read in: SYNC + DAM + DATA + CRC
        rlen = 3 + 1 + 256 + 2
        sdata = self.f.read(rlen * mult)
        if not sectorData['density']:
            # Single Density - Dedupe the data
            sdata = strDdup(sdata)
        
        # CRC calculation
        if sectorData['density']:
            #print(sdata[:3+1+256])
            nc = crc_hqx(sdata[:3+1+256], 0xffff)
        else:
            #print(sdata[3:3+1+256])
            nc = crc_hqx(sdata[3:3+1+256], 0xffff)

        # Unpack
        sync, dam, data, crc = unpack(">3sB256sH",sdata)

        assert(dam == 0xfb)
        #print(crc,nc)
        assert(crc == nc)
        print("Reading %d bytes from T:%d H:%d S:%d CRC:0x%04x" % (len(data), track, side, sector, crc))
        return data

    def writeSector(self, track, side, sector, data):
        sectorData = self.getSector(track, side, sector)

        #  FM: SYNC($00x3) + DAM($FB) + DATA(sectorlen) + CRC(uint16)
        #      CRC: DAM + DATA
        #      Reminder: in DMK FM Single Density Bytes are doubled
        # MFM: SYNC($A1x3) + DAM($FB)  + DATA(sectorlen) + CRC(uint16)
        #      CRC: SYNC + DAM + DATA

        # Prepare the data for CRC Calculation
        cdata = b''
        if sectorData['density']:
            # Double Density - include sync bytes
            cdata += b'\xa1\xa1\xa1'
        # DAM
        cdata += b'\xfb'
        # Data
        cdata += data
        # Calculate CRC
        crc = crc_hqx(cdata, 0xffff)

        # Prepare sector data - DAM + DATA + CRC
        sdata = pack(">B256sH", 0xfb, data, crc)
        
        print("Writing %d bytes to   T:%d H:%d S:%d CRC:0x%04x" % (len(data), track, side, sector, crc))
        self.f.seek(sectorData['dam_foffset'],0)
        # Duplicate the data for single density
        if not sectorData['density']:
            sdata = strDup(sdata)
        self.f.write(sdata)

    def parse(self):

        self.dmk = {}
        self.f.seek(0,0)
        st = os.stat(self.f.name)
        flen = st.st_size
        data = self.f.read(16)
        #self.dmk['header'] = data
        self.dmk['wp'], self.dmk['tracks'], self.dmk['trklen'], self.dmk['flags'], _, self.dmk['vd'] = unpack("<BBHB7sI", data)
        self.dmk['sides'] = 1 if self.dmk['flags']&0x10 else 2
        self.dmk['density'] = self.dmk['flags']&0x40
        self.dmk['ignoreDensity'] = self.dmk['flags']&0x80
        self.dmk['track_data'] = {}
        for t in range(self.dmk['tracks']):
            for s in range(self.dmk['sides']):
                trk = {'track': t, 'side': s, 'length': self.dmk['trklen'] , 'foffset':self.f.tell()}
                data = self.f.read(self.dmk['trklen'])
                #trk['hdr'] = data
                #trk['idams'] = unpack("<64H", data)
                trk['idams'] = []
                trk['sectors'] = {}
                ptrs = unpack("<64H", data[:128])
                # print(ptrs)
                for p in ptrs:
                    if p==0:
                        continue
                    idam = {}
                    idam['density'] = True if p&0x8000 else False
                    idam['offset'] = p&0x3fff
                    idam['foffset'] = idam['offset'] + trk['foffset']
                    idams =  idam['offset']
                    idame = idams+7
                    ddup = False
                    if idam['density'] is False:
                        idame += 7
                        ddup = True
                    idamd = data[idams:idame]
                    if ddup:
                        idamd = strDdup(idamd)
                    _, track, side, sector, size, crc = unpack(">BBBBBH", idamd)
                    #print(p, idam, _, track, side, sector, size, crc)
                    assert(sector!=0)
                    dam_offset = data[idame:].index(b'\xfb') + idame
                    dam_foffset = dam_offset + trk['foffset']
                    if idam['density'] is False:
                        crc_offset = dam_offset + 2 + 512
                        data_crc = unpack(">H", strDdup(data[crc_offset:crc_offset+4]))[0]
                    else:
                        crc_offset = dam_offset + 1 + 256
                        data_crc = unpack(">H", data[crc_offset:crc_offset+2])[0]
                    sectord = {'track': track, 'sector': sector, 'side': side, 'size': size, 'crc': crc, 'dam_offset':dam_offset, 'dam_foffset': dam_foffset, 'density':idam['density'], 'data_crc': data_crc}
                    trk['idams'].append(idam) 
                    trk['sectors'][sector] = sectord
                trk['num_sectors'] = len(trk['idams'])
                if not track in self.dmk['track_data']:
                    self.dmk['track_data'][track] = {}
                if not side in self.dmk['track_data'][track]:
                    self.dmk['track_data'][track][side] = {}
                self.dmk['track_data'][track][side] = trk
                #_ = self.f.seek(self.dmk['trklen']-128, 1)
        #return dmk

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='DMK Library',
        description='Library for DMK format virtual disk images',
        epilog='Text at the bottom of help')

    parser.add_argument('-T', '--test')
    parser.add_argument('-i', '--import', dest='input')
    parser.add_argument('-e', '--export')
    parser.add_argument('-t', '--template')
    parser.add_argument('-o', '--output')
    parser.add_argument('-p', '--padding', type=int, default=0)
    parser.add_argument('--flex', action='store_true')
    args = parser.parse_args()


    if not args:
        parser.print_help()

    if args.test:
        dmk = DMK(args.test)
        pprint.pprint(dmk.dmk)
        for track in sorted(dmk.tracks()):
            for side in sorted(dmk.sides(track)):
                sectors = sorted(dmk.sectors(track, side))
                for sector in sectors:
                    data = dmk.readSector(track, side, sector)
                    dmk.writeSector(track, side, sector, data)

    elif args.input and args.template and args.output:
        tf = os.path.expanduser(args.template)
        of = os.path.expanduser(args.output)
        shutil.copyfile(tf, of)
        dmk = DMK(of)
        fn = os.path.expanduser(args.input)
        f = open(fn, 'rb')
        for track in sorted(dmk.tracks()):
            remain = 0
            for side in sorted(dmk.sides(track)):
                sectors = sorted(dmk.sectors(track, side))
                if not args.flex:
                    remain = 0
                for sector in sectors:
                    data = f.read(256)
                    if data == '':
                        print("E: T:%d H:%d S:%d: No data available for sector" % (track, side, sector))
                        continue
                    # print(track,side,sector)
                    dmk.writeSector(track, side, sector, data)
                remain += args.padding - len(sectors)
                if not args.flex and args.padding > 0 and remain > 0:
                    # Non-FLEX - Remove Padding at the end of each side 
                    print("P: T:%d Skipping padding for %d sector(s): Src:%d Dest:%d Sides:%d" % (track, remain, args.padding, len(sectors), len(dmk.sides(track))))
                    for i in range(remain):
                        _ = f.read(256)
            if args.flex and args.padding > 0 and remain > 0:
                # FLEX: Remove the padding after both sides of the track are read
                print("P: T:%d Skipping padding for %d sector(s): Src:%d Dest:%d Sides:%d" % (track, remain, args.padding, len(sectors), len(dmk.sides(track))))
                for i in range(remain):
                    _ = f.read(256)

    elif args.export and args.output:
        ef = os.path.expanduser(args.export)
        of = os.path.expanduser(args.output)
        dmk = DMK(ef)
        f = open(of, 'wb')
        for track in sorted(dmk.tracks()):
            remain = 0
            for side in sorted(dmk.sides(track)):
                sectors = sorted(dmk.sectors(track, side))
                if not args.flex:
                    remain = 0
                for sector in sectors:
                    f.write(dmk.readSector(track, side, sector))
                remain += args.padding - len(sectors)
                if not args.flex and args.padding > 0 and remain > 0:
                    # Add padding at the end of each side
                    print("P: T:%d: Adding padding for %d sector(s)" % (track, remain))
                    for i in range(remain):
                        f.write(b'\x00'*256)
            if args.flex and args.padding > 0 and remain > 0:
                # Add padding after both sides of the track are written
                print("P: T:%d: Adding padding for %d sector(s)" % (track, remain))
                for i in range(remain):
                    f.write(b'\x00'*256)
    else:
        parser.print_help()
