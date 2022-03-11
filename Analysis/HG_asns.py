import json
from unicodedata import name
from pexpect import EOF


def get_HG_asns(input_file, output_file, HG_list):
    fulljson = dict()
    for HG in HG_list:
        HG_id = set()

        with open(input_file, "rt") as file:
            for line in file:
                data = json.loads(line)

                try:
                    data["asn"]
                    if HG in data["name"]:
                        HG_id.add(data["organizationId"])
                except:
                    pass

        HG_asns = set()
        with open(input_file, "rt") as file:
            for line in file:
                data = json.loads(line)

                try:
                    data["asn"]
                    if data["organizationId"] in HG_id:
                        HG_asns.add(data["asn"])
                except:
                    pass
        fulljson[HG] = {"asns": list(HG_asns), "orgId": list(HG_id)}

    with open(f"{output_file}", "wt") as file:
        json.dump(fulljson, file, indent=4)


if __name__ == "__main__":
    get_HG_asns("20220101.as-org2info.jsonl", "test.json", ["YAHOO", "GOOGLE"])
