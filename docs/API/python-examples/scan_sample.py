from __future__ import print_function
import sys, os
import time
import pprint
import json
import http.client
import re

# Configuration Parameters
VERBOSE = False
SCAN_COUNT = 10
SCAN_INTERVAL = 0
DEFAULT_DWELL = 8
CAPTURE_FILE = "my-scan.msd"
TARGET_IP_ADDR = "192.168.1.100"
SHOW_SCANS = False

class SingleMass:
    def __init__(self, mass, dwell=None):
        self.mass = mass
        self.dwell = dwell

class MassSweep:
    def __init__(self, start, stop, ppamu, dwell=None):
        self.start = start
        self.stop  = stop
        self.ppamu = ppamu
        self.dwell = dwell

#
# channels is a comma separated list (in square brackest) of the channel settings.
# The values may be SingleMass or MassSWeep (in amu, with decimal point if needed), or one of the
# channel modes (in quotes), see apidoc.html /mmsp/scanSetup/channel/<index#>/channelMode
#       'timestamp'
#       'totalPressure'
#       'fixedNumber'
#       'systemStatus'
#       'hardwareErrors'
#       'hardwareWarnings'
CHANNELS = [
    'fixedNumber',
    'timestamp',
    'systemStatus',
    'baseline',
    SingleMass(4.0),
    MassSweep(18.0, 28.0, 10, 32),
    MassSweep(40.0, 80.0,  5, 8),
    'TPQuad',
    'EmissionCurrent',
    'totalpressure']

#########################################################################
#
#        Do not modify code below this point
#
#########################################################################

class MMSP:
    def __init__(self, target_ip, port=80):
        self.conn = http.client.HTTPConnection('%s:%d' % (target_ip, port), timeout=10)

    def send(self, request, verbose=None):
        if verbose is None:
            verbose = VERBOSE

        if verbose:
            print(("Request: %s" % request))

        self.conn.request('GET', request)
        resp = self.conn.getresponse()
        http_status = resp.status

        if http_status != 200:
            if not verbose:
                print(("Request: %s" % request))

            print(("HTTP Status:", http_status))
            print(("Response:", resp))
            return (http_status, resp.read())
        
        resp_txt = resp.read()
        try:
            resp_rtn = json.loads(resp_txt)
        except:
            resp_rtn = resp_txt
        if verbose:
            self._printResponse(resp_rtn)

        return (http_status, resp_rtn)

    def _printResponse(self, resp):
        if not isinstance(resp, dict):
            print("Response:")
            print("   ", resp)
            return

        data = resp.get('data', None)
        conditions = resp.get('conditions')
        status = resp.get('name', None)
        if data is None:
            print("Response:")
            print("### Couldn't find 'data' entry in response")
            for key,value in list(resp.items()):
                print((" - %s:" % (key), value)) # pprint.pformat(value))
        else:
            outstr = pprint.pformat(data,2)
            line_cnt = outstr.count("\n")
            if line_cnt > 1:
                outstr = re.sub( '^',' '*4, outstr ,flags=re.MULTILINE )
                print(("Response: [%s]" % status))
                print(outstr)
            else:
                print(("Response: [%s]" % status, outstr))
            if conditions is not None:
                outstr = pprint.pformat(conditions, 2)
                outstr = re.sub( '^',' '*4, outstr ,flags=re.MULTILINE )
                print("Conditions:")
                print(outstr)
        print("")
    
    def getFile(self, remote_fname, local_fname="output.bin"):
        self.conn.request('GET', remote_fname)
        resp = self.conn.getresponse()

        if resp.status == 404:
            resp.read()
        else:
            with open(local_fname, 'wb') as f:
                f.write(resp.read())
        return resp.status, resp.length, remote_fname

###############################################################################

def start_scan(mmsp, channels):
    # Take control to the unit and make sure it's stopped
    print("Taking control...")
    mmsp.send("/mmsp/communication/control/set?force")
    mmsp.send('/mmsp/scanSetup/set?scanstop=1')

    # Setup the channels
    print("Setting up channels...")
    chan_num = 0
    for c in channels:
        chan_num += 1
        dwell = DEFAULT_DWELL
        if type(c) == str:
            print("Channel #%d: %s" % (chan_num, c))
            mmsp.send("/mmsp/scanSetup/set?@channel=%d&channelMode=%s&dwell=8&enabled=True" % (chan_num, c))
        elif isinstance(c, SingleMass):
            if c.dwell is not None:
                dwell = c.dwell

            print("Channel #%d: Single Mass %f [dwell=%d]" % (chan_num, c.mass, dwell))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&channelMode=Single' % chan_num)
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&enabled=True' % chan_num)
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&startmass=%.1f' % (chan_num, c.mass))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&dwell=%d' % (chan_num, dwell))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&ppamu=1' % chan_num)
        elif isinstance(c, MassSweep):
            if c.dwell is not None:
                dwell = c.dwell

            print("Channel #%d: Sweep %f..%f [dwell=%d, ppamu=%d]" % (chan_num, c.start, c.stop, dwell, c.ppamu))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&channelMode=Sweep' % chan_num)
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&enabled=True' % chan_num)
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&startmass=%.1f' % (chan_num, c.start))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&stopmass=%.1f' % (chan_num, c.stop))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&dwell=%d' % (chan_num, dwell))
            mmsp.send('/mmsp/scanSetup/set?@channel=%d&ppamu=%d' % (chan_num, c.ppamu))
        else:
            print("Don't know how to handle", type(c), c)

    # Start the scan 
    print("Starting Scan...")
    mmsp.send("/mmsp/scanSetup/set?startchannel=1&stopchannel=%d" % chan_num)
    mmsp.send("/mmsp/scanSetup/set?scancount=%d" % SCAN_COUNT)
    mmsp.send("/mmsp/scanSetup/CaptureFileName/set?%s" % CAPTURE_FILE)
    mmsp.send("/mmsp/scanSetup/set?scanInterval=%d&scanstart=1" % SCAN_INTERVAL)

###############################################################################

def wait_for_scans(mmsp):
    last_report = -1
    while True:
        time.sleep(1)
        http_code, resp = mmsp.send("/mmsp/scanInfo/get?currentScan&scanning")
        current_scan = resp['data']['currentScan']
        scanning = resp['data']['scanning']
        if not scanning:
            print("\rAll Done, finished scanning")
            break
        elif current_scan != last_report:
            msg = "Scan %d/%d" % (current_scan, SCAN_COUNT)
            print("\r\t%-20s" % msg, end='')
            last_report = current_scan

###############################################################################

def dump_scans(mmsp):
    last_report = -1
    while True:
        time.sleep(1)
        http_code, resp = mmsp.send("/mmsp/measurement/nextScan/get")
        data = resp['data']
        system_status = data['systemStatus']
        current_scan  = data['currentScan']
        scan_num      = data['scannum']
        scan_values   = data['values']

        if scan_values is not None:
            print(scan_num, scan_values)

        if (system_status & 0x2) == 0:
            # Scanning Inactive
            if current_scan == scan_num:
                # All scans have be processed
                break

###############################################################################

# Open up a connection to the target
mmsp = MMSP(TARGET_IP_ADDR)

# Setup the channels and start scanning
start_scan(mmsp, CHANNELS)

# Wait for the scanning to complete
if SHOW_SCANS:
    dump_scans(mmsp)
else:
    wait_for_scans(mmsp)

# Grab the capture file
print("Downloading Capture File (%s)..." % CAPTURE_FILE)
mmsp.getFile("//user_data/%s" % CAPTURE_FILE, CAPTURE_FILE)

# Delete the capture file on the target
mmsp.send('/@rm?\\user_data\\%s' % CAPTURE_FILE)
