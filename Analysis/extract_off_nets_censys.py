import json
import os
import socket
import re

from HG_asns import get_HG_asns


def is_hostname(dns_name):
    try:
        socket.inet_aton(dns_name)
        return False
    except socket.error as e:
        return True


def load_tld_suffixes(suffixes_filename):
    suffixes = dict()
    try:
        with open(suffixes_filename, "rt") as file:
            for line in file:
                if "!" in line or "//" in line:
                    continue
                if line[0] == "*":
                    suffixes[line[2:].rstrip()] = None
                else:
                    suffixes[line.rstrip()] = None
    except:
        print("Couldn't load/process TLD suffixes file \"{}\"".format(suffixes_filename))
        return None
    return suffixes


def calc_TLD_plus_one(dns_name, suffixes):
    dns_name = dns_name.lstrip('*.')
    if '/' in dns_name:
        dns_name = dns_name.replace('/', '')
    # If not a valid dns_name skip it
    if '.' not in dns_name:
        return None, None
    # Split domain name to parts
    domain_name_fragmented = dns_name.split('.')
    # Construct TLD+1 key (e.g '.google.com' -> 'com.google')
    tld_plus_one = domain_name_fragmented[-1] + \
        '.' + domain_name_fragmented[-2]
    tld_plus_one_check_suffix = domain_name_fragmented[-2] + \
        '.' + domain_name_fragmented[-1]
    if tld_plus_one_check_suffix in suffixes:
        if len(domain_name_fragmented) > 3:
            tld_plus_one = domain_name_fragmented[-1] + '.' + \
                domain_name_fragmented[-2] + '.' + domain_name_fragmented[-3]
            domain_name_fragmented[-2] = domain_name_fragmented[-1] + \
                '.' + domain_name_fragmented[-2]
            del domain_name_fragmented[-1]
        else:
            return None, None

    return tld_plus_one


def extract_fingerprint(on_net_dir, suffixes):
    if on_net_dir[-1] != "/":
        on_net_dir += "/"
    files = os.listdir(on_net_dir)

    dns_to_hg = dict()

    for filename in files:
        with open(on_net_dir+filename, "rt") as file:
            hg_keyword = filename.split('.')[0]
            if hg_keyword not in dns_to_hg:
                dns_to_hg[hg_keyword] = dict()

            for line in file:
                data = json.loads(line)

                if "dns_names" in data:
                    for dns in data["dns_names"]:
                        if is_hostname(dns):
                            dns_to_hg[hg_keyword][calc_TLD_plus_one(
                                dns, suffixes)] = None
    return dns_to_hg


def off_nets(dataset_dir, on_nets_dir, asn_to_kw_dir, asn_to_kw_filename, hg_asns_dir, hg_asns_filename, suffixes, out_dir):
    discr_counter = 0
    for dir, _, files in os.walk(dataset_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            dns_to_hg = extract_fingerprint(on_nets_dir+temp, suffixes)

            with open(hg_asns_dir+temp+"/"+hg_asns_filename, "rt") as file:
                hg_asns = json.load(file)

            with open(asn_to_kw_dir+temp+"/"+asn_to_kw_filename, "rt") as file:
                asn_to_hg = json.load(file)

            hg_files = dict()
            for hg in hg_asns:
                hg_files[hg.lower()] = open(
                    out_dir+temp+"/"+hg.lower()+".txt", "wt")

            for filename in files:
                print(filename)
                with open(dir+"/"+filename, "rt") as file:
                    for line in file:
                        data = json.loads(line)

                        ip = data["ip"]
                        asn = data["asn"]
                        org = data["org"]
                        dns_list = data["dns_names"]

                        if len(asn) > 0:

                            for hg_kw in hg_asns:
                                if hg_kw.lower() in org.lower():

                                    is_on_net = False
                                    if asn in asn_to_hg:
                                        if asn_to_hg[asn] in hg_kw:
                                            is_on_net = True

                                    if not is_on_net:
                                        dns_match = True
                                        for dns in dns_list:
                                            dns_match2 = True
                                            stript_dns = calc_TLD_plus_one(
                                                dns, suffixes)
                                            if stript_dns not in dns_to_hg[hg_kw]:
                                                dns_match = False
                                                dns_match2 = False

                                        if dns_match != dns_match2:
                                            discr_counter += 1

                                        if dns_match:
                                            to_write = {
                                                "ip": ip,
                                                "asn": asn,
                                                "dns_names": dns_list,
                                                "org": org
                                            }
                                            hg_files[hg_kw].write(
                                                json.dumps(to_write)+"\n")

            for file in hg_files:
                hg_files[file].close()
    print("Number of discrapancy : ", discr_counter)


if __name__ == "__main__":
    censys_formatted_dir = "../Dataset-ignore/censys_formatted/"
    out_dir = "../Dataset-ignore/output/off_nets_my_way2/"
    suffixes_file = "../Dataset-samples/suffixes.txt"
    on_nets_dir = "../Dataset-ignore/output/censys_onnets2/"

    hg_asns_dir = "../Dataset-samples/HG_asns/"
    asn_to_kw_dir = "../Dataset-samples/asn_to_kw/"

    hg_asns_filename = "hg_asns.json"
    asn_to_kw_filename = "asn_to_kw.json"

    suffixes = load_tld_suffixes(suffixes_file)

    off_nets(censys_formatted_dir, on_nets_dir, asn_to_kw_dir,
             asn_to_kw_filename, hg_asns_dir, hg_asns_filename, suffixes, out_dir)
