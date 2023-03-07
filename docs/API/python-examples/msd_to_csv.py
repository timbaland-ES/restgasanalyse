from __future__ import print_function
import sys, os
import ctypes
import binascii
import pprint
import struct
import csv

DEBUG = False

class ChannelDescriptor(ctypes.BigEndianStructure):
    mode = ""
    _fields_ = [
        ('raw_mode',    ctypes.c_char * 32),
        ('enabled',     ctypes.c_uint16),
        ('start_mass',  ctypes.c_uint16),
        ('stop_mass',   ctypes.c_uint16),
        ('ppamu',       ctypes.c_uint16),
        ('extra',       ctypes.c_uint16),
        ('dwell',       ctypes.c_uint16),
        ('data_format',     ctypes.c_uint16),
        ('pts_per_chan',    ctypes.c_uint16),
    ]

    def load(self, f):
        size = ctypes.sizeof(self)
        bytes = f.read(size)
        if len(bytes) == 0:
            return False
        ctypes.memmove(ctypes.addressof(self), bytes, len(bytes))
        self.mode = self.raw_mode.decode()
        return True

    def dump(self):
        print("mode:         %s" % self.mode)
        print("enabled:      %d" % self.enabled)
        print("start_mass:   %d" % self.start_mass)
        print("stop_mass:    %d" % self.stop_mass)
        print("ppamu:        %d" % self.ppamu)
        print("dwell:        %d" % self.dwell)
        print("extra:        %d" % self.extra)
        print("data_format:  %d" % self.data_format)
        print("pts_per_chan: %d" % self.pts_per_chan)

class GroupHeader(ctypes.BigEndianStructure):
    _fields_ = [
        ('start_scan',      ctypes.c_uint32),
        ('num_scans',       ctypes.c_uint32),
        ('pts_per_scan',    ctypes.c_uint32),
        ('error_dropped',   ctypes.c_uint32),
        ('error_overflow',  ctypes.c_uint32),
        ('reserved',        ctypes.c_uint32),
    ]

    def load(self, f):
        size = ctypes.sizeof(self)
        bytes = f.read(size)
        if len(bytes) == 0:
            return False
        ctypes.memmove(ctypes.addressof(self), bytes, len(bytes))
        return True

    def dump(self):
        print("start_scan:     %d" % self.start_scan)
        print("num_scans:      %d" % self.num_scans)
        print("pts_per_scan:   %d" % self.pts_per_scan)
        print("error_dropped:  %d" % self.error_dropped)
        print("error_overflow: %d" % self.error_overflow)
        print("reserved:       %d" % self.reserved)

    def meta_row(self):
        print("META,%d,%d,%d,%d,%d,%d" % (
            self.start_scan, self.num_scans, self.pts_per_scan,
            self.error_dropped, self.error_overflow, self.reserved
        ))

def read_file_header(f):
    chan = ChannelDescriptor()
    data = f.read(40)
    trim = data[-4:]
    num_channels,  = struct.unpack(">L", trim);
    channels = []
    if DEBUG:
        print("Found %d channels" % num_channels)
    pts_per_scan = 0
    scan_format  = [">"]
    header_parse = []
    for idx in range(num_channels):
        if DEBUG:
            print("")
            print("Channel", idx+1)
        chan.load(f)
        if DEBUG:
            chan.dump()

        if chan.mode == "Sweep":
            ppamu = chan.ppamu
            mode = chan.mode
            start = chan.start_mass
            pts = chan.pts_per_chan
            num = 0
            for i in range(pts):
                num = float(start + (100/ppamu)*i) / 100
                head = mode + ": " + str(num)
                header_parse.append(head)
        elif chan.mode == "Single":
            ppamu = chan.ppamu
            mode = chan.mode
            start = chan.start_mass
            num = float(start) / 100
            head = mode + ": " + str(num)
            header_parse.append(head)
        else:
            header_parse.append(chan.mode)

        if chan.data_format == 1: 
            pts_per_scan += chan.pts_per_chan
            scan_format.append("f" * chan.pts_per_chan)
        elif chan.data_format == 2:
            pts_per_scan += chan.pts_per_chan
            scan_format.append("L" * chan.pts_per_chan)
            

    unpack_format = "".join(scan_format)
    if DEBUG:
        print("Points Per Scan:", pts_per_scan)
        print("Unpack Format:", unpack_format)

    return header_parse, pts_per_scan, unpack_format


def group_iterator(f):
    while True:
        header = GroupHeader()
        if header.load(f):
            yield header
        else:
            return

def scan_iterator(f, header, unpack_format):
    start = header.start_scan
    end = start+header.num_scans
    pps = header.pts_per_scan

    for n in range(start, end):
        data = f.read(4*pps)
        scan =  (n, ) + struct.unpack(unpack_format, data)
        yield scan


def write_output_file(fname):
    out_Name = fname[0:-4] + '.csv'
    with open(out_Name, mode='w') as output_file:
        header = GroupHeader()
        headers = []
        writer = csv.writer(output_file, lineterminator='\n')
        console = csv.writer(sys.stdout, lineterminator='\n')
        f = open(fname, 'rb')

        header_parse, pts_per_scan, unpack_format = read_file_header(f)

        header_parse.insert(0,"Scan Number")
        writer.writerow(header_parse)

        for header in group_iterator(f):
            if DEBUG:
                header.meta_row()
            if header.pts_per_scan != pts_per_scan:
                raise Exception("Points Per Scan Mismatch [%d, %d]" % (header.pts_per_scan, pts_per_scan))

            for scan in scan_iterator(f, header, unpack_format):
                writer.writerow(scan)
                if DEBUG:
                    console.writerow(scan)




if __name__ == "__main__":
    if "-v" in sys.argv:
        DEBUG = True
        sys.argv.remove("-v") 
    elif "--help" in sys.argv:
        print("[-v] Print Output <Document to be converted to .csv>")
        sys.exit()
    else:
        DEBUG = False
    write_output_file(sys.argv[1])