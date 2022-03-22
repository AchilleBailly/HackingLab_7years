import json
import os
import socket
import re


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
    files = os.listdir(on_net_dir)

    dns_to_hg = dict()

    for filenames in files:
        with open(on_net_dir+files, "rt") as file:
            hg_keyword = file.split('.')[0]
            if hg_keyword not in dns_to_hg:
                dns_to_hg[hg_keyword] = dict()

            for line in file:
                data = json.loads(line)

                if "dns_name" in data:
                    for dns in data["dns_name"]:
                        if is_hostname(dns):
                            data[hg_keyword][calc_TLD_plus_one(
                                dns, suffixes)] = None
    return dns_to_hg


def off_nets(dataset_dir, ip_to_as, hg_asns, dns_to_hg, suffixes, out_dir, on_net_dir):
    for dir, _, files in os.walk(dataset_dir):
        if files != []:
            temp = dir.split("/")[-1]
            if not os.path.exists(out_dir+temp):
                os.makedirs(out_dir+temp)

            hg_files = dict()
            for hg in hg_asns:
                hg_files[hg.lower()] = open(
                    out_dir+temp+"/"+hg.lower()+".txt", "wt")

            dns_to_hg = extract_fingerprint(on_net_dir+"/"+temp, suffixes)

            for filename in files:
                print(filename)
                with open(dir+"/"+filename, "rt") as file:
                    for line in file:
                        data = json.loads(line)

                        for ip in data:
                            asns = list()
                            try:
                                asns = ip_to_as[ip]
                            except:
                                pass

                        if len(asns) > 0:
                            if "subject_dn" in data:
                                for hg_kw in hg_asns:
                                    if hg_kw in data["subject_dn"]:
                                        continue
