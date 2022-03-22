import gzip
import os

import json
from asn_to_HG_keyword import *
from HG_asns import *
import pytricia


def load_ip_to_as_mapping(filename):
    pyt = pytricia.PyTricia()
    try:
        with open(filename, 'rt') as f:
            data = json.load(f)
        for prefix in data:
            pyt[prefix] = data[prefix]
    except:
        print("Couldn't load/process IP-to-AS mapping file \"{}\"".format(filename))
        return None
    return pyt


def write_HG_certs(dataset_dir, out_dir, ip_to_as, asn_to_kw, hg_asns):
    for dir, _, files in os.walk(dataset_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            hg_files = dict()
            for hg in hg_asns:
                hg_files[hg.lower()] = open(
                    out_dir+temp+"/"+hg.lower()+".txt", "wt")

            for filename in files:
                print(filename)
                with open(dir+"/"+filename, "rt") as file:
                    for line in file:
                        data = json.loads(line)

                        try:
                            data["subject_dn"]
                            ip = data["ip"]
                            asn = str(ip_to_as[ip][0])
                            HG = asn_to_kw[asn]
                            if HG.lower() in line.lower():
                                nline = {
                                    "ip": ip,
                                    "asn": asn,
                                    "dns_names": data["names"]
                                }
                                hg_files[HG.lower()].write(
                                    json.dumps(nline)+"\n")

                        except:
                            continue

            for hg in hg_files:
                hg_files[hg].close()


if __name__ == "__main__":
    # filenames to configure
    iptoas_filename = "../Dataset-samples/ip_to_as_test.json"
    HG_asns_filename = "../Dataset-samples/asns.json"
    asn_to_kw_filename = "../Dataset-samples/asn_to_kw.json"
    asns_file = "../Dataset-samples/20220101.as-org2info.jsonl"
    ip_to_as_filename = "../Dataset-samples/ip_to_as_test.json"

    certs_fles_folder = "../Dataset-ignore/Dataset/"
    output_dir = "../Dataset-ignore/output/"

    get_HG_asns(asns_file, HG_asns_filename, ["GOOGLE", "NETFLIX"])

    get_asn_to_kw(HG_asns_filename, asn_to_kw_filename)

    ip_to_as = load_ip_to_as_mapping(ip_to_as_filename)

    with open(asn_to_kw_filename, "rt") as file:
        asn_to_kw = json.load(file)

    with open(HG_asns_filename, "rt") as file:
        hg_asns = json.load(file)

    write_HG_certs(certs_fles_folder, output_dir, ip_to_as, asn_to_kw, hg_asns)
