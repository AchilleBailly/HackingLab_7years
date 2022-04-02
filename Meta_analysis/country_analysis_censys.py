import json
import os
from time import time
import pandas
import numpy as np


def get_orgid2country(caida_file):
    res = dict()
    with open(caida_file, "rt") as file:
        for line in file:
            if 'country' in line:
                data = json.loads(line)

                res[data["organizationId"]] = data["country"]
    return res


def get_asn2country(caida_file):
    res = dict()
    org2country = get_orgid2country(caida_file)
    with open(caida_file, "rt") as file:
        for line in file:
            data = json.loads(line)

            if "asn" in data:
                asn = data["asn"]
                org = data["organizationId"]
                res[asn] = org2country[org]

    return res


def get_country2continent(filename, separator=","):
    res = dict()
    with open(filename, "rt") as file:
        for line in file:
            if separator in line:
                l = line.split(separator)
                res[l[0]] = l[1].strip()
    return res


if __name__ == "__main__":
    off_nets_folder = "../Dataset-ignore/output/off_nets_my_way2/"
    excel_file_name = "Results_country.xlsx"

    excel_file_name_bis = "continents_timestamp.xlsx"

    caida_dir = "../Dataset-samples/caida/"
    country2continent_file = "../datasets/country_to_continent/country_to_continent.txt"

    country2continent = get_country2continent(country2continent_file)

    continent_list = ["EU", "AS", "OC", "AF", "NA", "SA"]

    per_hg = dict()
    per_timestamp = dict()

    for dir, _, files in os.walk(off_nets_folder):
        hg_list = []
        if files != []:
            timestamp = dir.split("/")[-1]

            if timestamp not in per_timestamp:
                per_timestamp[timestamp] = dict()
                per_timestamp[timestamp + " count"] = dict()

            caida_file = caida_dir + timestamp + "/as-org2info.jsonl"
            asn2country = get_asn2country(caida_file)

            for filename in files:
                hg_kw = filename.split(".")[0]

                if hg_kw not in per_hg:
                    hg_list.append(hg_kw)
                    per_hg[hg_kw] = dict()

                if hg_kw not in per_timestamp[timestamp]:
                    per_timestamp[timestamp][hg_kw] = dict()
                    per_timestamp[timestamp + " count"][hg_kw] = dict()

                    for cnt in continent_list:
                        per_timestamp[timestamp][hg_kw][cnt] = set()
                        per_timestamp[timestamp + " count"][hg_kw][cnt] = 0

                if timestamp not in per_hg[hg_kw]:
                    per_hg[hg_kw][timestamp] = dict()
                    per_hg[hg_kw][timestamp+" count"] = dict()

                    for cnt in continent_list:
                        per_hg[hg_kw][timestamp][cnt] = set()
                        per_hg[hg_kw][timestamp + " count"][cnt] = 0

                with open(dir+"/"+filename) as file:
                    for line in file:
                        data = json.loads(line)

                        asn = data["asn"]
                        if asn in asn2country:
                            country = asn2country[asn]
                            if country == "Sweden":
                                country = "SE"
                            continent = country2continent[country]

                            per_hg[hg_kw][timestamp][continent].add(asn)

                            per_timestamp[timestamp][hg_kw][continent].add(asn)

    for hg in per_hg:
        for timestamp in per_timestamp:
            if "count" not in timestamp:
                for continent in per_hg[hg][timestamp]:
                    count = len(per_hg[hg][timestamp][continent])
                    per_hg[hg][timestamp+ " count"][continent] = count
                    per_timestamp[timestamp + " count"][hg][continent] = count

    with pandas.ExcelWriter(excel_file_name) as writer:
        for hg in per_hg:
            to_write = pandas.DataFrame.from_dict(per_hg[hg])
            to_write.to_excel(writer, sheet_name=hg)
    
    with pandas.ExcelWriter(excel_file_name_bis) as writer:
        for timestamp in per_timestamp:
            to_write = pandas.DataFrame.from_dict(per_timestamp[timestamp])
            to_write.to_excel(writer, sheet_name=timestamp)
