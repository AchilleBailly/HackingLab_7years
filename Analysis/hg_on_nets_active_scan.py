# %%
import os
import json
import pprint
import argparse
import pytricia

from lib.helpers import load_ip_to_as_mapping, load_config_file, load_hypergiant_ases, process_configuration_file

# %%


def process_ee_certs(inputFile, ip_to_as, hg_asn_to_hg_keywords, filePathToStoreResults):
    openFiles_l = dict()
    hg_keywords_l = {v for v_list in hg_asn_to_hg_keywords.values()
                     for v in v_list}
    # print(hg_keywords_l)
    for hg_keyword in hg_keywords_l:
        filePath = filePathToStoreResults + hg_keyword + ".txt"
        openFiles_l[hg_keyword] = open(filePath, 'wt')

    with open(inputFile, 'rt') as f:
        for line in f:
            data = json.loads(line)

            for ip in data:
                asns = list()
                try:
                    asns = ip_to_as[ip]
                except:
                    pass

            keywords_matched = None
            foundASN = None
            # Iterate over all ASNs of the IP-to-AS mapping (MOAS)
            for asn in asns:
                # print(asn)
                # Check if the ASN match to any of the hypergiant ASes
                if asn in hg_asn_to_hg_keywords:
                    # print(asn)
                    keywords_matched = hg_asn_to_hg_keywords[asn]
                    foundASN = asn
                    print(keywords_matched, foundASN)
                    break

            if keywords_matched is not None:
                if 'subject' in data[ip]:
                    print("Subject")
                    if 'organization' in data[ip]['subject']:
                        organization_value = ""
                        organization_value = " ".join(
                            [i.lower() for i in data[ip]['subject']['organization'] if i is not None])
                        print(organization_value)
                        for item in data[ip]['subject']['organization']:
                            if item is not None:
                                organization_value += item.lower() + " "
                            # print(organization_value)
                        for keyword in keywords_matched:
                            if keyword in organization_value:
                                storeJSON = {
                                    "ip": ip,
                                    "ASN": foundASN,
                                    "dns_names": data[ip]['dns_names'],
                                    "subject:organization": organization_value
                                }
                                openFiles_l[keyword].write(
                                    "{}\n".format(json.dumps(storeJSON)))

    for file in openFiles_l:
        openFiles_l[file].close()


# %%
hg_ases_file = "../datasets/hypergiants/2019_11_hypergiants_asns.json"
ee_certs_file = "./results/ee_certs.txt"
config_file = "./configs/config.txt"
ip2as_file = "../datasets/ip_to_as/2019_11_25thres_db.json"

# Store results in specified path
result_path = "./results/on-nets/"
# print(filePathToStoreResults)

# Load the IP-to-AS mapping
ip_to_as = load_ip_to_as_mapping(ip2as_file)
# print(ip_to_as)

# Load the Hypergiant ASes
hg_ases = load_hypergiant_ases(hg_ases_file)
# print(hg_ases)

# Load the config file
configuration_input = load_config_file(config_file)
# print(configuration_input)

# Check if config file is valid and return a map between HG ASes and HG keywords
hg_asn_to_hg_keywords = process_configuration_file(
    configuration_input, hg_ases)
# print(hg_asn_to_hg_keywords)


process_ee_certs(ee_certs_file, ip_to_as, hg_asn_to_hg_keywords, result_path)

# %%


# %% [markdown]
# ## Check missing files for active scan

# %%
counter = 0

file_dirs = os.listdir(
    "/media/gerben/Seagate/Study/hacking_lab/tls_scans/active")
for i in range(1, 4001):
    if f"b_{i}" not in file_dirs:
        print(f"b_{i}")
    else:
        files = os.listdir(
            f"/media/gerben/Seagate/Study/hacking_lab/tls_scans/active/b_{i}/")
        if len(files) < 1:
            print(f"b_{i}")
            continue
    counter += 1

print(counter)

# counter = 0

# file_dirs = os.listdir("../datasets/tls_scans/active/")
# for i in range(1, 4001):
#     if f"b_{i}" not in file_dirs:
#         print(f"b_{i}")
#     else:
#         files = os.listdir(f"../datasets/tls_scans/active/b_{i}/")
#         if len(files) < 1:
#             print(f"b_{i}")
#             continue
#     counter += 1

# print(counter)
