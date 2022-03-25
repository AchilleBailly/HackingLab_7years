import gzip
import os

import json
from asn_to_HG_keyword import *
from HG_asns import *
import pytricia
from utils import load_ip_to_as_mapping


def write_HG_certs(dataset_dir, out_dir, asn_to_kw, hg_asns):
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

                        """
                        getting first thee IP and the corresponding ASN.
                        Through the CAIDA dataset we get the HG owning that ASN and make its keyword is appearing in the line
                        """
                        ip = data["ip"]
                        asn = str(data["asn"])
                        try:
                            HG = asn_to_kw[asn]
                            if HG.lower() in data["org"].lower():
                                nline = {
                                    "ip": ip,
                                    "asn": asn,
                                    "dns_names": data["dns_names"],
                                    "org": data["org"]
                                }
                                hg_files[HG.lower()].write(
                                    json.dumps(nline)+"\n")

                        except:
                            continue

            for hg in hg_files:
                hg_files[hg].close()


if __name__ == "__main__":
    # filenames to configure
    HG_asns_filename = "../Dataset-samples/HG_asns.json"
    asn_to_kw_filename = "../Dataset-samples/asn_to_kw2.json"
    asns_file = "../Dataset-samples/20210101.as-org2info.jsonl"

    certs_fles_folder = "../Dataset-ignore/censys_formatted/"
    output_dir = "../Dataset-ignore/output/censys_onnets/"

    HG_kw_list = [
        "google",
        "facebook",
        "netflix",
        "akamai",
        "alibaba",
        "yahoo",
        "apple",
        "cdnetworks",
        "limelight",
        "microsoft",
        "amazon",
        "bitgravity",
        "cachefly",
        "cloudflare",
        "disney",
        "highwinds",
        "hulu",
        "incapsula",
        "cdn77",
        "twitter",
        "fastly"
    ]

    hg_asns = get_HG_asns(asns_file, HG_asns_filename, HG_kw_list)

    asn_to_kw = get_asn_to_kw(HG_asns_filename, asn_to_kw_filename)

    write_HG_certs(certs_fles_folder, output_dir, asn_to_kw, hg_asns)
