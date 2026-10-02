import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find all function calls in onclick, onchange, etc.
calls = re.findall(r'on\w+=\"([^\"]+)\"', html)
calls += re.findall(r'on\w+=\'([^\']+)\'', html)

js_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
js_async_funcs = set(re.findall(r'async\s+function\s+([a-zA-Z0-9_]+)\s*\(', html))
all_defined = js_funcs | js_async_funcs

print('Defined JS functions count:', len(all_defined))
for fn in sorted(list(all_defined)):
    print(f'  - {fn}')

print('\nChecking HTML event handler calls:')
missing = set()
for c in calls:
    found_funcs = re.findall(r'([a-zA-Z0-9_]+)\s*\(', c)
    for fn in found_funcs:
        if fn in ['alert', 'confirm', 'setTimeout', 'setInterval', 'switchTab', 'setQuery', 'document', 'event', 'Math', 'JSON', 'parseInt', 'parseFloat']:
            continue
        if fn not in all_defined:
            print(f'MISSING FUNCTION: {fn} (called in handler: "{c}")')
            missing.add(fn)

if not missing:
    print('ALL HANDLERS MAP TO VALID DEFINED FUNCTIONS!')
else:
    print('Total missing functions:', len(missing))
