import json
import pytricia


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
