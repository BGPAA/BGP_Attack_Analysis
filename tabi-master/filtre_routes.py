import sys
import json

list_as_path=[]
with open(sys.argv[1]) as f:
    with open("filtre_json/filtred_routes.json", "w") as f_out:
        for x in f:
            data = json.loads(x[:-1])
            if data["action"] == "A":
                if data["as_path"] not in list_as_path:
                    if '{' not in data["as_path"] :
                        f_out.write(x)
                        list_as_path.append(data["as_path"])


