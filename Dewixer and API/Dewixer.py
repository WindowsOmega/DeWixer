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
import base64
from neocities import NeoCities

lmproj_aero_fd = 0
api_av = 1
debug_flag = 0
archive_base = 'Site Archives'

# To find
error_flag = 0
username = os.getlogin()
url = input("What URL do we have here? ")
if " -d" in url:
    debug_flag = 1
    url = url.replace(" -d", "")
    print("Debug flag flagged!")
if " error" in url:
    error_flag = 1
    url = url.replace(" error", "")
    print("Error flag flagged!")
if " -aset" in url:
    url = url.replace(" -aset", "")
    api_key = input("What is your Neocites API key? (make sure no one knows it) ")
    string_bytes = api_key.encode('utf-8')
    encoded_bytes = base64.b64encode(string_bytes)
    base64_string = encoded_bytes.decode('ascii')
    fileapi = open(f"C:\\Users\\{username}\\Documents\\Neoapi.txt", "w")
    fileapi.write(base64_string)
    fileapi = "C:\\Users\\" + username + "\\Documents\\Neoapi.txt"
    with open(fileapi, 'r') as file:
        key64 = file.read()
    apik = base64.b64decode(key64)
    decoded_string = apik.decode('utf-8')
    nc = NeoCities(key=decoded_string)
else:
    try:
        fileapi = "C:\\Users\\" + username + "\\Documents\\Neoapi.txt"
        with open(fileapi, 'r') as file:
            key64 = file.read()
        apik = base64.b64decode(key64)
        decoded_string = apik.decode('utf-8')
        nc = NeoCities(key=decoded_string)    
    except FileNotFoundError:
        print("You have not added a Neocities API key. However, this script will continue to add the HTML doc manually.")
        api_av = 0
        pass
    
prog_bar = tqdm(total=100, desc="Making HTML", unit="%", ncols=100) 
prog_bar.update(12.5)


def curl_get_and_save(url, filename, wts):
    try:
        if wts == 0:
            command = ["curl", "-o", f'C:\\Users\\{username}\\Downloads\\' + filename, url]
            subprocess.run(command, check=True, capture_output=True)
            print(f"Successfully downloaded content from {url} and saved to {filename}")
        if wts == 1:
            documents_folder = os.path.expanduser("~\\Documents")
            archives_folder = os.path.join(documents_folder, "Site Archives")
            os.makedirs(archives_folder, exist_ok=True)
            date_str = datetime.now().strftime("%m-%d-%Y")
            dated_folder = os.path.join(archives_folder, date_str)
            os.makedirs(dated_folder, exist_ok=True)
            rounds = 1
            n_filename = filename
            while True:
                if os.path.exists(dated_folder + f"\\{n_filename}"):
                    n_filename = n_filename.replace(".html", "")
                    n_filename = n_filename.replace(f" ({rounds-1})", "")
                    n_filename = n_filename + f" ({rounds})" + ".html"
                    rounds = rounds + 1
                else:
                    break
            command = ["curl", "-o", dated_folder + f"\\{n_filename}", url]
            subprocess.run(command, check=True, capture_output=True)
            print(f"Successfully downloaded content from {url} and saved to {n_filename}")
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
curl_get_and_save(url, filename, 0)


filepath = f'C:\\Users\\{username}\\Downloads\\' + filename

prog_bar.update(12.5)
# Word Finder+
if '"' in filepath:
        filepath = filepath.replace('"', '')
if '.html' in filepath:
    oldfilepath = filepath
    oldnewfilepath = oldfilepath.replace('.html', '.')
    print(oldnewfilepath)
    newfilepath = oldnewfilepath + 'txt'
    try:
        os.rename(filepath, newfilepath)
    except FileExistsError:
        os.remove(newfilepath)
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
    global filename
    global filepath
    global url
    global nctag
    global main
    global n_url_arch
    global lmproj_aero_fd
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    if "wixstudio" in url:
        wix_domain = "wixstudio"
        match = re.search(r'https://([^.]+)\.wixstudio\.com', url)
        if match:
            nctag = match.group(1)
            print(f'nctag is {nctag}')
            if "landmphone" in nctag:
                lmproj_aero_fd = 1
        suburl = re.search(r'wixstudio\.com/([^/]+)', url)
        if suburl:
            main = suburl.group(1)
            print(f'main is {main}')
        else:
            main = ''
    if "wixsite" in url:
        wix_domain = "wixsite"
        match = re.search(r'https://([^.]+)\.wixsite\.com', url)
        if match:
            nctag = match.group(1)
            print(f'nctag is {nctag}')
            if "landmphone" in nctag:
                lmproj_aero_fd = 1
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
        line = line.replace('--wix-ads-height:30px;', '--wix-ads-height:0px;')
        line = line.replace('--wix-ads-top-height:30px;', '--wix-ads-top-height:0px;')
        line = line.replace(f'{wix_domain}.com', 'neocities.org')
        line = line.replace(main, '')
        line = re.sub(f'https://{nctag}.neocities.org/+', f'https://{nctag}.neocities.org/', line)
        old_fn = filename
        n_url_arch = f"https://{nctag}.neocities.org/" + filename.replace(".html", "")
        filename = old_fn
        line = line.replace('https://www.wix.com/favicon.ico', f'https://{nctag}.neocities.org/favicon.ico')
        modified_lines.append(line)

    with open(filepath, 'w', encoding="utf-8") as file:
        for line in modified_lines:
            file.write(line)
            if debug_flag == 1:
                print(".", end="")
                time.sleep(0.01)
prog_bar.update(12.5)          

find_and_delete_word()
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
curl_get_and_save(n_url_arch, filename, 1)

def find_dynamic_key_value_pairs(filepath):
    with open(filepath, 'r') as file:
        file_content = file.read()
        
    pattern = r'"([^"]+)":\s*"HtmlComponent"'
    matches = re.findall(pattern, file_content)
    return matches



matches = find_dynamic_key_value_pairs(filepath)
print("Found embeds:", matches)
matchess = 0
times_embed = len(matches)


def find_and_replace_div(input_file_path, output_file_path, div_id, new_content):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = rf'<div class="[^"]*" id="{div_id}"></div>'
    print(pattern)
    matches3 = re.findall(pattern, content, re.DOTALL)

    if matches3:
        updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print("Content replaced successfully.")
    else:
        pattern = rf'<div id="{div_id}" class="[^"]*"></div>'
        print(pattern)
        matches3 = re.findall(pattern, content, re.DOTALL)
        if matches3:
            updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print("Content replaced successfully.")
        else:
            print("No matching div found.")

for i in range(times_embed):
    embed_cur = matches[matchess]
    try:
        fileembed = "C:\\Users\\" + username + "\\Documents\\" + embed_cur + ".txt"
        with open(fileembed, 'r', encoding='utf-8') as file:
            content = file.read()
        print(content)
        find_and_replace_div(filepath, filepath, embed_cur, content)
        matchess = matchess + 1
    except FileNotFoundError:
        cur_wixiframe= input(f"You have not added the {embed_cur}'s wix-iframe id(s). Go to the GitHub page for more info. Paste it here. ")
        fileembed = "C:\\Users\\" + username + "\\Documents\\" + embed_cur + ".txt"
        with open(fileembed, 'w', encoding='utf-8') as file:
            file.write(cur_wixiframe)
            find_and_replace_div(filepath, filepath, embed_cur, cur_wixiframe)
            matchess = matchess + 1
            pass

def read_file_and_process(file_name):
    with open(file_name, 'r') as file:
        number_of_files = int(file.readline().strip())
        file_paths = []
        for _ in range(number_of_files):
            file_path = file.readline().strip()
            file_paths.append(file_path)
        return file_paths

def js_div(input_file_path, output_file_path, div_id, new_content):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = rf'<div class="[^"]*" id="{div_id}">.+?</div>(?!\s*</div>)'
    print(f"Pattern: {pattern}")
    
    matches = re.findall(pattern, content, re.DOTALL)

    if matches:
        updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print("Content replaced successfully with no </div>.")
    else:
        pattern = rf'<div class="[^"]*" id="{div_id}">.+?</div>(?!\s*</div>)'
        print(f"Pattern: {pattern}")
        
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)
            
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print("Content replaced successfully with no </div>.")

def js_div_embed(input_file_path, output_file_path, div_id, new_content):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = rf'<div class="[^"]*" id="{div_id}">.+?</div></wix-iframe></div>'
    print(pattern)
    matches3 = re.findall(pattern, content, re.DOTALL)

    if matches3:
        updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print("Content replaced successfully.")
    else:
        pattern = rf'<div id="{div_id}" class="[^"]*">.+?</div></wix-iframe></div>'
        print(pattern)
        matches3 = re.findall(pattern, content, re.DOTALL)
        if matches3:
            updated_content = re.sub(pattern, new_content, content, flags=re.DOTALL)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print("Content replaced successfully.")

def remove_path(file_paths, path_to_remove):
    if path_to_remove in file_paths:
        file_paths.remove(path_to_remove)
        print(f"Removed: {path_to_remove}")
    else:
        print(f"Path '{path_to_remove}' not found in the list.")


js_filename = read_file_and_process(os.path.expanduser("~\\Documents") + "\\customjs.txt")
for path in js_filename:
    js_div_name = path.replace(".txt", "")
    js_div_name = js_div_name.replace("--js", "")
    if js_div_name in matches:
        print("Embed JS found.")
        with open(os.path.expanduser("~\\Documents") + f"\\{path}", 'r', encoding='utf-8') as file:
            content = file.read()
        js_div_embed(filepath, filepath, js_div_name, content)
    else:
        print(js_div_name)
        with open(os.path.expanduser("~\\Documents") + f"\\{path}", 'r', encoding='utf-8') as file:
            content = file.read()
        js_div(filepath, filepath, js_div_name, content)


if '.txt' in filepath:
    oldfilepath = filepath
    oldnewfilepath = oldfilepath.replace('.txt', '.')
    print(oldnewfilepath)
    newfilepath = oldnewfilepath + 'html'
    os.rename(filepath, newfilepath)
    print("Renamed", filepath)
    filepath = newfilepath
if lmproj_aero_fd == 1:
    with open(filepath, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    footer = soup.find("footer", id="SITE_FOOTER")
    if footer:
        footer.decompose()
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
    print("Land Proj Aero footer is gone!")
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
if api_av == 1:
    nc.upload((filename, filepath))
