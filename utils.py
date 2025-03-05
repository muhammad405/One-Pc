import requests

r = requests.post('http://195.158.30.91/ONECOMPUTERS/hs/item/getdata', auth=('HttpUser', '85!@fdfd$DES35wgf&%'), data={
        "sap_codes": ["050000000000081350"]
})

if r.status_code == 200:
    data = r.json()
    print(data)
else:
    print(f"Request failed with status code {r.status_code}")