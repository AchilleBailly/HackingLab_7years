import gzip
import os

import json
from asn_to_HG_keyword import *
from HG_asns import *
from utils import load_ip_to_as_mapping


def create_hg_asns(asns_dir, out_dir, output_filename, hg_list):
    if asns_dir[-1] != "/":
        asns_dir += "/"

    if out_dir[-1] != "/":
        out_dir += "/"

    for dir, _, files in os.walk(asns_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            for filename in files:
                HG_asns(dir+"/"+filename, out_dir+temp +
                        "/"+output_filename, hg_list)


def creat_asn2kw(hg_asns_dir, out_dir, output_filename):
    if hg_asns_dir[-1] != "/":
        hg_asns_dir += "/"

    if out_dir[-1] != "/":
        out_dir += "/"

    for dir, _, files in os.walk(hg_asns_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            for filename in files:
                asn_to_kw(dir+"/"+filename, out_dir+temp+"/"+output_filename)


def write_HG_certs(dataset_dir, out_dir, asn_to_kw_dir, asn_to_kw_filename, hg_asns_dir, hg_asns_filename):
    if hg_asns_dir[-1] != "/":
        hg_asns_dir += "/"

    if out_dir[-1] != "/":
        out_dir += "/"

    if asn_to_kw_dir[-1] != "/":
        asn_to_kw_dir += "/"

    if hg_asns_dir[-1] != "/":
        hg_asns_dir += "/"

    for dir, _, files in os.walk(dataset_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            hg_files = dict()
            with open(hg_asns_dir+temp+"/"+hg_asns_filename, "rt") as file:
                hg_asns = json.load(file)

            with open(asn_to_kw_dir+temp+"/"+asn_to_kw_filename, "rt") as file:
                asn_to_kw = json.load(file)

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
    asns_dir = "../Dataset-samples/caida"
    hg_asns_dir = "../Dataset-samples/HG_asns/"
    asn_to_kw_dir = "../Dataset-samples/asn_to_kw"

    hg_asns_filename = "hg_asns.json"
    asn_to_kw_filename = "asn_to_kw.json"

    certs_fles_folder = "../Dataset-ignore/censys_formatted/"
    output_dir = "../Dataset-ignore/output/censys_onnets2/"

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

    create_hg_asns(asns_dir, hg_asns_dir, hg_asns_filename, HG_kw_list)

    creat_asn2kw(hg_asns_dir, asn_to_kw_dir, asn_to_kw_filename)

    write_HG_certs(certs_fles_folder, output_dir, asn_to_kw_dir,
                   asn_to_kw_filename, hg_asns_dir, hg_asns_filename)
