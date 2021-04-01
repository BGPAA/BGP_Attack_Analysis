# -*- coding: utf-8 -*

import json
import sys

with open(sys.argv[1]) as f:
    with open("filtre_json/filtred_hijacks.json", "w") as f_out:

        for x in f:
            data = json.loads(x[:-1])
            if(data["announce"]["prefix"] == data["conflict_with"]["prefix"]):
                f_out.write(x)
