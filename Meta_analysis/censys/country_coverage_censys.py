import json
import os
import pandas as pd


if __name__ == "__main__":
    apnic_file = "../datasets/apnic_population_estimates/2020_11.json"
    off_net_folder = "../Dataset-ignore/output/censys_onnets2/Censys-2021-04-15/"

    xcel_out_file = "country_coverage_onnets.xlsx"

    coverage_per_hg = dict()
    asns_per_hg = dict()

    with open(apnic_file, "rt") as file:
        apnic_data = json.load(file)

    for dir, _, files in os.walk(off_net_folder):
        if files != []:
            for filename in files:
                hg_kw = filename.split(".")[0]

                asns_per_hg[hg_kw] = dict()
                with open(dir+"/"+filename, "rt") as file:
                    for line in file:
                        data = json.loads(line)

                        asns_per_hg[hg_kw][data["asn"]] = None

    for hg_kw in asns_per_hg:
        coverage_per_hg[hg_kw] = dict()
        for asn in asns_per_hg[hg_kw]:
            for cc in apnic_data:
                if cc not in coverage_per_hg[hg_kw]:
                    coverage_per_hg[hg_kw][cc] = 0
                if asn in apnic_data[cc]:
                    if cc not in coverage_per_hg[hg_kw]:
                        coverage_per_hg[hg_kw][cc] = apnic_data[cc][asn]
                    else:
                        coverage_per_hg[hg_kw][cc] += apnic_data[cc][asn]

    with pd.ExcelWriter(xcel_out_file) as writer:
        to_write = pd.DataFrame.from_dict(coverage_per_hg)
        to_write.to_excel(writer, sheet_name="test")
