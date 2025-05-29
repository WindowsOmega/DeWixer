import os
import time
import shutil
from datetime import datetime
from tqdm import tqdm
import pycurl
from io import BytesIO
import subprocess
import re
from bs4 import BeautifulSoup

debug_flag = 0
archive_base = 'Site Archives'

# To find
error_flag = 0
url = input("What URL do we have here? ")
if " -d" in url:
    debug_flag = 1
    url = url.replace(" -d", "")
    print("Debug flag flagged!")
if " error" in url:
    error_flag = 1
    url = url.replace(" error", "")
    print("Error flag flagged!")
prog_bar = tqdm(total=100, desc="Making HTML", unit="%", ncols=100) 
prog_bar.update(12.5)
username = os.getlogin()

def curl_get_and_save(url, filename):
    try:
        command = ["curl", "-o", f'C:\\Users\\{username}\\Downloads\\' + filename, url]
        subprocess.run(command, check=True, capture_output=True)
        print(f"Successfully downloaded content from {url} and saved to {filename}")
    except subprocess.CalledProcessError as e:
         print(f"Error executing curl command: {e}")
    except FileNotFoundError:
        print("Error: curl command not found. Please ensure curl is installed and in your system's PATH.")
prog_bar.update(12.5)
# cURL 
if "/" in url:
    oldurl = url
    result = oldurl.rsplit('/', 1)[-1]
filename = f"{result}.html"
curl_get_and_save(url, filename)

def archive_file(src_file_path):
    documents_folder = os.path.expanduser("~/Documents")
    archives_folder = os.path.join(documents_folder, "Site Archives")
    os.makedirs(archives_folder, exist_ok=True)
    date_str = datetime.now().strftime("%m-%d-%Y")
    dated_folder = os.path.join(archives_folder, date_str)
    os.makedirs(dated_folder, exist_ok=True)
    file_name = os.path.basename(src_file_path)
    dest_file_path = os.path.join(dated_folder, file_name)
    shutil.copy2(src_file_path, dest_file_path)

    print(f"File copied to: {dest_file_path}")

filepath = f'C:\\Users\\{username}\\Downloads\\' + filename
archive_file(filepath)

prog_bar.update(12.5)
# Word Finder+
if '"' in filepath:
        filepath = filepath.replace('"', '')
if '.html' in filepath:
    oldfilepath = filepath
    oldnewfilepath = oldfilepath.replace('.html', '.')
    print(oldnewfilepath)
    newfilepath = oldnewfilepath + 'txt'
    os.rename(filepath, newfilepath)
    print("Renamed", filepath)
    filepath = newfilepath
prog_bar.update(12.5)

def find_and_delete_word():
    with open(filepath, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    wix_ads_div = soup.find("div", id="WIX_ADS")
    if wix_ads_div:
        wix_ads_div.decompose()
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
prog_bar.update(12.5)

def dewixer():
    global debug_flag
    global filepath
    global url
    global nctag
    global main
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    match = re.search(r'https://([^.]+)\.wixsite\.com', url)
    if match:
        nctag = match.group(1)
        print(f'nctag is {nctag}')
    suburl = re.search(r'wixsite\.com/([^/]+)', url)
    if suburl:
        main = suburl.group(1)
        print(f'main is {main}')
    else:
        main = ''
    modified_lines = []
    for line in lines:
        line = line.replace('--wix-ads-height:50px;', '--wix-ads-height:0px;')
        line = line.replace('--wix-ads-top-height:50px;', '--wix-ads-top-height:0px;')
        line = line.replace('wixsite.com', 'neocities.org')
        line = line.replace(main, '')
        line = re.sub(f'https://{nctag}.neocities.org/+', f'https://{nctag}.neocities.org/', line)
        line = line.replace('https://www.wix.com/favicon.ico', f'https://{nctag}.neocities.org/favicon.ico')
        modified_lines.append(line)

    with open(filepath, 'w', encoding="utf-8") as file:
        for line in modified_lines:
            file.write(line)
            if debug_flag == 1:
                print(".", end="")
                time.sleep(0.01)
prog_bar.update(12.5)          

word_to_delete = '<div id="WIX_ADS" class="EFLBov czJOIz ytGGBw"><a data-testid="linkElement" href="//www.wix.com/lpviral/enviral?utm_campaign=vir_wixad_live&amp;orig_msid=ab72da44-75fc-4752-9bcf-113720cbc616&amp;adsVersion=white" target="_blank" rel="nofollow" class="Oxzvyr YD5pSO has-custom-focus"><span class="aGHwBE"><span data-hook="freemium-text" class="areOb6">This site was designed with the <div data-testid="bannerLogo" class="dTTUA9"><div><svg class="_4i7Zy" viewBox="0 0 28 10.89" aria-label="wix"><path d="M16.02.2c-.55.3-.76.78-.76 2.14a2.17 2.17 0 0 1 .7-.42 3 3 0 0 0 .7-.4A1.62 1.62 0 0 0 17.22 0a3 3 0 0 0-1.18.2z" class="o4sLYL"></path><path d="M12.77.52a2.12 2.12 0 0 0-.58 1l-1.5 5.8-1.3-4.75a4.06 4.06 0 0 0-.7-1.55 2.08 2.08 0 0 0-2.9 0 4.06 4.06 0 0 0-.7 1.55L3.9 7.32l-1.5-5.8a2.12 2.12 0 0 0-.6-1A2.6 2.6 0 0 0 0 .02l2.9 10.83a3.53 3.53 0 0 0 1.42-.17c.62-.33.92-.57 1.3-2 .33-1.33 1.26-5.2 1.35-5.47a.5.5 0 0 1 .34-.4.5.5 0 0 1 .4.5c.1.3 1 4.2 1.4 5.5.4 1.5.7 1.7 1.3 2a3.53 3.53 0 0 0 1.4.2l2.8-11a2.6 2.6 0 0 0-1.82.53zm4.43 1.26a1.76 1.76 0 0 1-.58.5c-.26.16-.52.26-.8.4a.82.82 0 0 0-.57.82v7.36a2.47 2.47 0 0 0 1.2-.15c.6-.3.75-.6.75-2V1.8zm7.16 3.68L28 .06a3.22 3.22 0 0 0-2.3.42 8.67 8.67 0 0 0-1 1.24l-1.34 1.93a.3.3 0 0 1-.57 0l-1.4-1.93a8.67 8.67 0 0 0-1-1.24 3.22 3.22 0 0 0-2.3-.43l3.6 5.4-3.7 5.4a3.54 3.54 0 0 0 2.32-.48 7.22 7.22 0 0 0 1-1.16l1.33-1.9a.3.3 0 0 1 .57 0l1.37 2a8.2 8.2 0 0 0 1 1.2 3.47 3.47 0 0 0 2.33.5z"></path></svg></div><div class="uJDaUS">.com</div></div> website builder. Create your website today.</span><span data-hook="freemium-button" class="O0tKs2 Oxzvyr">Start Now</span></span></a></div>'
find_and_delete_word()
if debug_flag == 1:
    print(f"'{word_to_delete}' deleted from '{filepath}'")
dewixer()

time.sleep(1)

try:
    with open(filepath, 'r', encoding="utf-8") as file:
            lines = file.readlines()
except FileNotFoundError:
        print(f"Error: File not found at {filepath}")

fixed_lines = []
for line in lines:
    line = line.replace('https://.neocities.org//', f'https://{nctag}.neocities.org/')
    line = line.replace('https://.neocities.org/favicon.ico', f'https://{nctag}.neocities.org/favicon.ico')
    line = line.replace('Â', '')
    if debug_flag == 1:
        print("Fixed Errored URL")
    fixed_lines.append(line)
prog_bar.update(12.5)
with open(filepath, 'w', encoding='utf-8') as file:
    file.writelines(fixed_lines)


if '.txt' in filepath:
    oldfilepath = filepath
    oldnewfilepath = oldfilepath.replace('.txt', '.')
    print(oldnewfilepath)
    newfilepath = oldnewfilepath + 'html'
    os.rename(filepath, newfilepath)
    print("Renamed", filepath)
    filepath = newfilepath
if error_flag == 1:
    with open(filepath, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find("header", id="SITE_HEADER")
    if header:
        header.decompose()
    footer = soup.find("footer", id="SITE_FOOTER")
    if footer:
        footer.decompose()
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
    print("Error page created")
prog_bar.update(12.5)
time.sleep(1)
