import os
import re
import glob
import sys
import pytz
import wget
import requests
import gzip
import shutil
import subprocess
import shlex
from datetime import datetime, timedelta


def download_files(date_begin, date_end):
    
    while(date_begin != date_end):
        url = 'http://data.ris.ripe.net/rrc21/'+str(date_begin.year)+'.'+str(date_begin.month).zfill(2)+'/updates.'+str(date_begin.year)+str(date_begin.month).zfill(2)+str(date_begin.day).zfill(2)+'.'+str(date_begin.hour).zfill(2)+str(date_begin.minute).zfill(2)+'.gz'
        date_begin += timedelta(minutes=5)
        output_directory = os.getcwd()+"/tabi-master/input/rrc21"
        wget.download(url, out=output_directory)

    url = 'http://data.ris.ripe.net/rrc21/'+str(date_begin.year)+'.'+str(date_begin.month).zfill(2)+'/updates.'+str(date_begin.year)+str(date_begin.month).zfill(2)+str(date_begin.day).zfill(2)+'.'+str(date_begin.hour).zfill(2)+str(date_begin.minute).zfill(2)+'.gz'
    output_directory = os.getcwd()+"/tabi-master/input/rrc21"
    wget.download(url, out=output_directory)



def unzip_files(path):
    
    files = glob.glob(os.getcwd()+path)
    for f in files:
        with gzip.open(f, 'rb') as f_in:
            with open(f.split(".gz")[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(f)

def maboed():
    
    files = glob.glob(os.getcwd() + "/tabi-master/input/rrc21/updates*")
    for f in files:
        cmd = "./mabo-master/mabo dump " + f
        args = shlex.split(cmd)
        with open("output/"+f.split("/")[-1]+"_dump", "w") as f_out:
            subprocess.call(args, stdout=f_out)
        os.remove(f)

def tabied():
    
    files = glob.glob(os.getcwd()+"/output/updates*")
    for f in files:    
        cmd = "tabi -d -f -j8 rrc21 output/ " + f
        args = shlex.split(cmd)
        subprocess.call(args)
        os.rename("output/no_name/all.routes.json.gz", "output/no_name/all.routes_"+ f.split("/")[-1].split("_")[0].split(".")[1] + "_" + f.split("/")[-1].split("_")[0].split(".")[2] + ".json.gz")
        os.rename("output/no_name/all.hijacks.json.gz", "output/no_name/all.hijacks_"+ f.split("/")[-1].split("_")[0].split(".")[1] + "_" + f.split("/")[-1].split("_")[0].split(".")[2] + ".json.gz")
        os.remove("output/no_name/all.defaults.json.gz")
        os.remove(f)

def concat_file(date_debut, date_fin):

    files_routes = glob.glob(os.getcwd() + "/output/no_name/all.routes*")
    routes_out = "output/no_name/all.routes.json"
    #routes_out = "output/no_name/all.routes_" + str(date_debut.year) + "-" + str(date_debut.month).zfill(2) + "-" + str(date_debut.day).zfill(2) + "_" + str(date_debut.hour).zfill(2) + ":" + str(date_debut.minute).zfill(2) + "__" + str(date_fin.year) + "-" + str(date_fin.month).zfill(2) + "-" + str(date_fin.day).zfill(2) + "_" + str(date_fin.hour).zfill(2) + ":" + str(date_fin.minute).zfill(2) + ".json"

    with open(routes_out, "w") as f_out:
        for f_in in files_routes:
            with open(f_in) as infile:
                f_out.write(infile.read())
            #f_out.write("\n")
            os.remove(f_in)

    files_hijacks = glob.glob(os.getcwd() + "/output/no_name/all.hijacks*")
    hijacks_out = "output/no_name/all.hijacks.json"
    #hijacks_out = "output/no_name/all.hijacks_" + str(date_debut.year) + "-" + str(date_debut.month).zfill(2) + "-"  + str(date_debut.day).zfill(2) + "_" + str(date_debut.hour).zfill(2) + ":" + str(date_debut.minute).zfill(2) + "__" + str(date_fin.year) + "-" + str(date_fin.month).zfill(2) + "-" + str(date_fin.day).zfill(2) + "_" + str(date_fin.hour).zfill(2) + ":" + str(date_fin.minute).zfill(2) + ".json"

    with open(hijacks_out, "w") as f_out:
        for f_in in files_hijacks:
            with open(f_in) as infile:
                f_out.write(infile.read())
            #f_out.write("\n")
            os.remove(f_in)

    with open(routes_out, 'rb') as f_in, gzip.open(routes_out + '.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    #os.remove(routes_out)


    with open(hijacks_out, 'rb') as f_in, gzip.open(hijacks_out + '.gz', 'wb') as f_out:
        f_out.writelines(f_in)
    #os.remove(hijacks_out)



now = datetime.now(pytz.utc) - timedelta(minutes=5)
now_str = now.strftime("%Y-%m-%d_%H:%M")
now = datetime.strptime(now_str, "%Y-%m-%d_%H:%M")
now -= timedelta(minutes=int(now.minute)%5)


begin = sys.argv[1]
end = sys.argv[2]
pattern = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]:[0-9][0-9]"

if not re.match(pattern, begin) or not re.match(pattern, end):
    raise Exception("Datetimes must be in the following format : YYYY-mm-dd_HH:MM")

date_begin = datetime.strptime(begin, "%Y-%m-%d_%H:%M")
date_begin -= timedelta(minutes=int(date_begin.minute)%5)

date_end = datetime.strptime(end, "%Y-%m-%d_%H:%M")
date_end -= timedelta(minutes=int(date_end.minute)%5)


if (date_begin > date_end):
    raise Exception("The start datetime must be less than the end datetime")

if (date_begin > now) or (date_end > now):
    raise Exception("The start datetime and the end datetime must be less than now")


download_files(date_begin, date_end)
unzip_files("/tabi-master/input/rrc21/*gz")
maboed()
tabied()
unzip_files("/output/no_name/*gz")
concat_file(date_begin, date_end)
print("\n\n")
