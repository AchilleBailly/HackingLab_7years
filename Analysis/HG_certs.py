import pytricia
from asn_to_HG_keyword import *
from HG_asns import *

from simplejson import load


def load_ip_to_as_mapping(filename):
    pyt = pytricia.PyTricia()
    try:
        with open(filename, 'rt') as f:
            data = json.load(f)
        for prefix in data:
            pyt[prefix] = data[prefix]
    except:
        print("Couldn't load/process IP-to-AS mapping file \"{}\"".format(filename))
        return None
    return pyt


def get_HG_certs(certs_filename, ip_to_as, hg_asns, asn_to_kw):
    try:
        with open(certs_filename, "rt") as certs_file:
            for line in certs_file:
                data = json.loads(line)

                for ip in data:
                    try:
                        asn = ip_to_as[ip][0]
                        try:
                            HG = asn_to_kw[asn]
                            print(HG)
                            print(data)
                        except:
                            pass
                    except:
                        continue
    except:
        print("Could not open certs file.")


if __name__ == "__main__":
    # filenames to configure
    iptoas_filename = "../Dataset-samples/ip_to_as_test.json"
    HG_asns_filename = "../Dataset-samples/asns.json"
    asn_to_kw_filename = "../Dataset-samples/asn_to_kw.json"
    asns_file = "../Dataset-samples/20220101.as-org2info.jsonl"
    ip_to_as_filename = "../Dataset-samples/ip_to_as_test.json"

    certs_fles_folder = "../Dataset-ignore"

    get_HG_asns(asns_file, HG_asns_filename, [
                "YAHOO", "GOOGLE", "FACEBOOK", "NETFLIX", "AKAMAI", "MICROSOFT"])

    get_asn_to_kw(HG_asns_filename, asn_to_kw_filename)

    ip_to_as = load_ip_to_as_mapping(ip_to_as_filename)

    with open(asn_to_kw_filename, "rt") as file:
        asn_to_kw = json.load(file)

    with open(HG_asns_filename, "rt") as file:
        hg_asns = json.load(file)

    for i in range(994, 1000):
        file = f"{certs_fles_folder}/b_{i}/certs.txt"
        print(file)
        get_HG_certs(file, ip_to_as, hg_asns, asn_to_kw)
