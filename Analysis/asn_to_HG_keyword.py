import json


def asn_to_kw(hg_asns_file: str, output_file_name: str):
    """
        creates a file mapping the asns to their HG kw
        ARGS: hg_asns_file is the file containing the HGs asns
              out_file_name is the name of the output file
    """
    with open(hg_asns_file, "rt") as file:
        data = json.load(file)

    out = dict()
    for HG in data:
        for asn in data[HG]["asns"]:
            out[asn] = HG

    with open(output_file_name, "wt") as output:
        json.dump(out, output, indent=4)


def get_asn_to_kw(hg_asns_file: str, output_file_name: str):
    """
        opens output_file_name if it exists or creates a file mapping the asns to their HG kw and returns it as json obj
        ARGS: hg_asns_file is the file containing the HGs asns
              out_file_name is the name of the output file
    """
    try:
        with open(output_file_name, "rt") as file:
            print("HG ASNs to keyword mapping found.")
            return json.load(file)
    except:
        asn_to_kw(hg_asns_file, output_file_name)
        with open(output_file_name, "rt") as file:
            print("Creating HG ASNs to keyword mapping file.")
            return json.load(file)


if __name__ == "__main__":
    asn_to_kw("test.json", "asn_to_kw.json")
