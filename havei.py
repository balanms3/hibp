#!/usr/bin/env python3

# Usage: python3 haveibeenpwned.py my-email-list.txt

import requests
import sys
import time
import csv

filename = "havei.csv"
fields = ['Email', 'Breachname', 'Domain', 'Confidence']



emails = sys.argv[1]

API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Firefox/76.0',
              'hibp-api-key': '43e85556b4964972b45e8e46ba0fb84d',  # Api key
              'api-version': '3',
              'content-type': 'application/json'}
with open(filename, 'w') as csvfile: 
 csvwriter = csv.writer(csvfile)
 csvwriter.writerow(fields) 
 try:
    print("[*] Reading file")
    with open(emails, "r") as emails:
        for email in emails:
            email = email.strip()
            url = API_URL + email + '?truncateResponse=false'
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 200:
                for d in r.json():
                    d['severity'] = ['Medium', 'High'][d['IsVerified'] and 'Passwords' in d['DataClasses']]
                    d['confidence'] = ['Medium', 'High'][d['IsVerified']]
                    print(f"[!] [{email}] - [{d['Name']}] - Domain: [{d['Domain']}] - "
                          f"Severity: [{d['severity']}] - Confidence: [{d['confidence']}] - "
                          f"Compromised: {d['DataClasses']}")
                    rows=[email,d['Name'],d['Domain'],d['confidence']]   
                    csvwriter.writerow(rows)      
            time.sleep(10)  # Prevent rate-limit
 except Exception as e:
    print(f"[Error] {e}")
