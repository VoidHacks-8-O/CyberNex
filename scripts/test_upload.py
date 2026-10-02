import urllib.request
import json

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
file_path = 'data/raw/synthetic_banking_transactions.csv'
with open(file_path, 'rb') as f:
    file_bytes = f.read()

header = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="synthetic_banking_transactions.csv"\r\nContent-Type: text/csv\r\n\r\n'.encode('utf-8')
footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
body = header + file_bytes + footer

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/dataset/inspect',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)

try:
    with urllib.request.urlopen(req) as res:
        print('STATUS:', res.status)
        data = json.loads(res.read().decode('utf-8'))
        print('RESPONSE KEYS:', list(data.keys()))
        print('FILE NAME:', data.get('file_name'))
        print('EST ROWS:', data.get('estimated_rows'))
except urllib.error.HTTPError as e:
    print('ERROR:', e.code, e.read().decode('utf-8'))
except Exception as ex:
    print('EXCEPTION:', ex)
