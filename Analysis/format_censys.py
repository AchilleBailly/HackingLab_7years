import json
import re
import os
from utils import *


def format_censys_file(filename, out_dir, ip_to_as):
    timestamp = filename.split("/")[-2] + "/"
    name = filename.split("/")[-1]

    if out_dir[-1] != "/":
        out_dir += "/"

    org_pat = re.compile(r"O=(.*),")
    dns_pat = re.compile(r"CN=(.*)")

    with open(filename, "rt") as file:
        if not os.path.exists(out_dir+timestamp):
            os.makedirs(out_dir+timestamp)

        with open(out_dir+timestamp+name, "wt") as out:
            for line in file:
                data = json.loads(line)

                if "subject_dn" in data and "ip" in data and "names" in data:
                    ip = data["ip"]
                    try:
                        asn = str(ip_to_as[ip][0])
                    except:
                        asn = ""

                    dns_names = data["names"]

                    search_res1 = org_pat.search(data["subject_dn"])
                    if search_res1 != None:
                        org = search_res1.group(1)
                    search_res2 = dns_pat.search(
                        data["subject_dn"])
                    if search_res2 != None:
                        dns_to_add = search_res2.group(1)

                    if search_res1 != None and search_res2 != None and "." in dns_to_add and " " not in dns_to_add:
                        dns_names.append(dns_to_add)
                        to_write = {
                            "ip": ip,
                            "asn": asn,
                            "org": org,
                            "dns_names": dns_names
                        }
                        out.write(json.dumps(to_write)+"\n")


if __name__ == "__main__":
    ip_to_as = load_ip_to_as_mapping(
        "../Dataset-samples/2020_11_25thres_db.json")

    file = "../Dataset-ignore/Dataset/Censys-2020-10-05/covid_Censys20201005_Censys20201005000000000000"
    out_dir = "../Dataset-ignore/censys_formatted/"

    for dir, _, files in os.walk("../Dataset-ignore/Dataset/"):
        if files != []:
            for file in files:
                print(file)
                path = dir+"/"+file
                format_censys_file(path, out_dir, ip_to_as)
