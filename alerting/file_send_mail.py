import glob
import os
import gzip
import pytz
import shutil
from datetime import datetime, timedelta


def unzip(now_str):
    files = glob.glob("archives/"+now_str+"*_hijacks.json.gz")
    for f in files:
        with gzip.open(f, 'rb') as f_in:
            with open(f.split(".gz")[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def concat(now_str):
    files_in = glob.glob("archives/"+now_str+"*_hijacks.json")
    file_out = "archives/"+now_str+"hijacks.json"
    with open(file_out, 'w') as f_out :
        for f_in in files_in:
            with open(f_in) as infile:
                f_out.write(infile.read())
            os.remove(f_in)


now = datetime.now(pytz.utc)
now_str = now.strftime("%Y-%m-%d")

unzip(now_str)
concat(now_str)
