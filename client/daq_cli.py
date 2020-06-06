import argparse
import json
from broker_client import BrokerClient

#module load psi-python36/4.4.0
#python daq_cli.py 11696646000 11696646300 -c channel_list


def main():
    parser = argparse.ArgumentParser(description="Broker Test")

    parser.add_argument("start_pulseid", type=int, help="start pulseid")
    parser.add_argument("stop_pulseid", type=int, help="stop pulseid")

    parser.add_argument("-p", "--pgroup", help="Example p12345", default="p18493")
    parser.add_argument("-o", "--output_dir", help="Output directory relative to the raw directory in the pgroup or /dev/null (default)", default="/dev/null")
    parser.add_argument("-c", "--channels_file", help="Text file with list of channels", default="channel_list")
    parser.add_argument("-e", "--epics_file", help="Text file with list of epics channels", default=None)
    parser.add_argument("-d", "--detectors_file", help="JSON file with the detector list", default=None)
    parser.add_argument("-s", "--scan_info_file", help="JSON file with the scan step information", default=None)
    parser.add_argument("-r", "--rate_multiplicator", type=int, help="Rate multiplicator (1(default): 100Hz, 2: 50Hz, ...)", default=1)

    clargs = parser.parse_args()

    channels = load_channels(clargs.channels_file)
    pvs = load_channels(clargs.epics_file)
    detectors = load_json(clargs.detectors_file)
    scan_info = load_json(clargs.scan_info_file)

    bc = BrokerClient(clargs.pgroup, clargs.rate_multiplicator)
    rn = bc.retrieve(clargs.output_dir, clargs.start_pulseid, clargs.stop_pulseid, detectors=detectors, channels=channels, pvs=pvs, scan_info=scan_info)
    print(rn)



def load_channels(fname):
    if not fname:
        return None
    out = set()
    with open(fname, "r") as f:
        for line in f:
            line = line.split("#")[0] # remove comments
            line = line.strip()
            if not line:
                continue
            out.add(line)
    return sorted(out)


def load_json(fname):
    if not fname:
        return None
    with open(fname) as f:
        return json.load(f)





if __name__ == "__main__":
    main()



