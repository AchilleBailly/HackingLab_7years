import json
import os
from time import time
import pandas
import numpy as np


if __name__ == "__main__":
    off_nets_folder = "../Dataset-ignore/output/off_nets_my_way/"
    excel_file_name = "Results.xlsx"

    per_timestamp = dict()

    for dir, _, files in os.walk(off_nets_folder):
        hg_list = []
        if files != []:
            timestamp = dir.split("/")[-1]

            off_nets_count = dict()

            for filename in files:
                hg_kw = filename.split(".")[0]

                if hg_kw not in off_nets_count:
                    hg_list.append(hg_kw)
                    off_nets_count[hg_kw] = set()

                with open(dir+"/"+filename) as file:
                    for line in file:
                        data = json.loads(line)

                        off_nets_count[hg_kw].add(data["ASN"])

            per_timestamp[timestamp] = off_nets_count

    per_timestamp_count = dict()
    for index_t, timestamp in enumerate(per_timestamp):
        per_timestamp_count[timestamp] = dict()
        for index_hg, hg_kw in enumerate(per_timestamp[timestamp]):
            per_timestamp_count[timestamp][hg_kw] = len(off_nets_count[hg_kw])

    res = pandas.DataFrame.from_dict(per_timestamp)

    res_count = pandas.DataFrame.from_dict(per_timestamp_count, mode='a')

    with pandas.ExcelWriter(excel_file_name) as writer:
        res.to_excel(writer, sheet_name="List of ASNs Active")
        res_count.to_excel(writer, sheet_name="Off-nets counts Active")
