# DeWixer
DeWixer is a Python program that removes Wix ads, and converts a Wix link to Neocities.
# Neocities API
The Neocities API allows you to automatically upload your converted Wix site to your Neocities one. To set up the API, you need a API key. Once you have retrieved that, type after your site name: -aset. Example: 
```
https://example.wixsite.com/example -aset
```
You'll see a prompt asking for your API key, paste it in and you're done.
# Embed Fixer Setup
So you use DeWixer and it tells you to go to the GitHub. That is due to you having iframes in your Wixsite. Due to how horrible the Wix's Thunderbolt framework is, "wix-iframe" never loads on Neocities. Even if the iframe did load, it would take a stupid amound of time, since Thunderbolt forces lazy-loading. In the scope of workablity and speed, you have to enter in the "wix-iframe" manually. This will save to a file in your Documents folder so you never have to enter that iframe's code again. <br> <br>
Step 1: Go to your Wixsite and inspect your iframe. You should see something like this:
<img width="579" height="302" alt="Screenshot 2025-07-16 103509" src="https://github.com/user-attachments/assets/d39557cd-8d5f-43b5-b36e-64ea37480f5d" />
<br> <br>
Step 2: Right click the parent (the upper most div within the tree) and click "Edit as HTML."
<img width="408" height="99" alt="Screenshot 2025-07-16 103840" src="https://github.com/user-attachments/assets/c2ed78e3-cb9d-4da7-825c-9d73571bb894" />
<br> <br>
Step 3: Copy and paste the HTML code into DeWixer. Repeat if prompted.
# Dependencies
* bs4
* tqdm
* io
* subprocess
* re
* os
* time
* pycurl
* shutil
* datetime
* base64
