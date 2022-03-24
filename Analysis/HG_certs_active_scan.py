from doctest import OutputChecker
import pytricia
import os
from asn_to_HG_keyword import *
from HG_asns import *
from utils import load_ip_to_as_mapping


def write_HG_certs(certs_filename, ip_to_as, out_directory, asn_to_kw, hg_asns):
    out = open(out_directory+"output_active_scan_HG_certs.txt", "w")
    try:
        with open(certs_filename, "rt") as certs_file:
            for line in certs_file:
                data = json.loads(line)

                for ip in data:
                    try:
                        for HG in hg_asns:
                            if HG.lower() in line:
                                asn = str(ip_to_as[ip][0])
                                try:
                                    HG = asn_to_kw[asn]
                                    out.write(line)
                                except:
                                    continue
                    except:
                        continue
    except:
        print("Could not open certs file.")
    out.close()


if __name__ == "__main__":
    # filenames to configure
    iptoas_filename = "../Dataset-samples/ip_to_as_test.json"
    HG_asns_filename = "../Dataset-samples/asns.json"
    asn_to_kw_filename = "../Dataset-samples/asn_to_kw.json"
    asns_file = "../Dataset-samples/20220101.as-org2info.jsonl"
    ip_to_as_filename = "../Dataset-samples/ip_to_as_test.json"

    certs_fles_folder = "../Dataset-ignore/active_scan/"

    output_directory = "../Dataset-ignore/output/"

    get_HG_asns(asns_file, HG_asns_filename, [
                "YAHOO", "GOOGLE", "FACEBOOK", "NETFLIX", "AKAMAI", "MICROSOFT"])

    get_asn_to_kw(HG_asns_filename, asn_to_kw_filename)

    ip_to_as = load_ip_to_as_mapping(ip_to_as_filename)

    with open(asn_to_kw_filename, "rt") as file:
        asn_to_kw = json.load(file)

    with open(HG_asns_filename, "rt") as file:
        hg_asns = json.load(file)

    for dir, subdir, files in os.walk(certs_fles_folder):
        for filename in files:
            write_HG_certs(dir+"/"+filename, ip_to_as,
                           output_directory, asn_to_kw, hg_asns)
