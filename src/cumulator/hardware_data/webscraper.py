# All the data is taken from the website "https://www.techpowerup.com/"
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random 
from tqdm import tqdm
import json


headers={
        'User-Agent': 'Mozilla/5.0',
    }

#function for processing dump of all cpus/gpus obtained in scrape_all
def process_dump(path_dump, path_csv):
    with open(path_dump, 'r') as file:
        dump=json.load(file)
        data_list=[]
        for data in tqdm(dump):
            soup=BeautifulSoup(data['html'],'html.parser')
            rows=soup.select('table.processors > tr')
            tdp=data['TDP']
            if tdp == "unkown":
                pass
            for row in rows:
                cells=row.find_all('td')
                data_list.append({'name':cells[0].getText().strip(), 'gpu_chip':cells[1].getText().strip(), 'released':cells[2].getText().strip(), 'bus':cells[3].getText().strip(), 'memory':cells[4].getText().strip(), 'gpu_clock':cells[5].getText().strip(), 'memory_clock':cells[6].getText().strip(), 'shaders/TMUs/ROPs':cells[7].getText().strip(), 'TDP':tdp})
        df=pd.DataFrame.from_dict(data_list)
        df.to_csv(path_csv, index=False)
        
#It first obtains a dump of all CPUs/GPUs whose TDP is known, and then calls process_dump for processing it and obtaing cpu.csv/gpu.csv
def scrape_all(cpu=True):
    if cpu:
        hardware="cpu"
    else:
        hardware="gpu"
    url=f"https://www.techpowerup.com/{hardware}-specs/?sort=name"
    r=requests.get(url, headers=headers)
    soup=BeautifulSoup(r.text, 'html.parser')

    #Obtain all TDPs
    TDP_options=soup.select('select#tdp > option')
    TDP=[]
    #options:'All','unknown' are not considered
    for option in TDP_options[1:-1]:
        tdp=option.getText().split()[0]
        TDP.append(tdp)

    sleep_minutes = 20
    dump=[]
    for tdp in tqdm(TDP):
        print(f'\nTDP:{tdp}\n')
        url=f"https://www.techpowerup.com/{hardware}-specs/?tdp={tdp}%20W&sort=name"
        r=requests.get(url, headers=headers)
        print(url)
        while r.status_code != 200:
            time.sleep(sleep_minutes*60)
            r=requests.get(url, headers=headers)
        dump.append({'TDP':tdp, 'html':r.text})
        with open(f'dump_{hardware}.json', 'w') as file:
            file.write(json.dumps(dump))
    process_dump(f'dump_{hardware}.json', f'{hardware}.csv')


# scrape_all(cpu=True)