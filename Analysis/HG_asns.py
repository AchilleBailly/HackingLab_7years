import json
from unicodedata import name


def HG_asns(input_file, output_file, HG_list):
    """
        produce a .json file containing for each HG keyword in HG_list, their orgId and their ASNs
        ARGS: input_file_name is the name of the CAIDA dataset file containing the worlds' ASNs
              output_file_name is the name of the output file
              HG_list is the list of the HG's keywords (eg. "GOOGLE" or "YAHOO")
    """
    fulljson = dict()
    for HG in HG_list:
        HG_id = set()

        with open(input_file, "rt", encoding="utf8") as file:
            for line in file:
                data = json.loads(line)

                try:
                    data["asn"]
                    if HG.lower() in data["name"].lower():
                        HG_id.add(data["organizationId"])
                except:
                    pass

        HG_asns = set()
        with open(input_file, "rt", encoding="utf8") as file:
            for line in file:
                data = json.loads(line)

                try:
                    data["asn"]
                    if data["organizationId"] in HG_id:
                        HG_asns.add(data["asn"])
                except:
                    pass
        fulljson[HG] = {"asns": list(HG_asns), "orgId": list(HG_id)}

    with open(output_file, "wt", encoding="utf8") as file:
        json.dump(fulljson, file, indent=4)


def get_HG_asns(input_file_name, save_file_name, HG_kw_list):
    """
        opens save_file_name if it exists or creates it with function:HG_asns and returns json obj.
        ARGS: save_file_name is the name of the CAIDA dataset file containing the worlds' ASNs
              output_file_name is the name of the output file
              HG_kw_list is the list of the HG's keywords (eg. "GOOGLE" or "YAHOO")
    """
    try:
        with open(save_file_name, "rt", encoding="utf8") as file:
            print("HG's ASNs file found.")
            return json.load(file)
    except:
        HG_asns(input_file_name, save_file_name, HG_kw_list)
        with open(save_file_name, "rt", encoding="utf8") as file:
            print("Creating HGs' ASNs list file.")
            return json.load(file)


if __name__ == "__main__":
    HG_asns("20220101.as-org2info.jsonl", "test.json",
            ["YAHOO", "GOOGLE", "FACEBOOK", "NETFLIX", "AKAMAI", "MICROSOFT"])
