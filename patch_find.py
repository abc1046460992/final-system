import re

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Detect start of open_details and end of open_details
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('            def open_details(evt=None):'):
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if 'tv.bind("<Double-1>", open_details)' in lines[i]:
            end_idx = i - 1
            break

print(f"open_details: {start_idx} to {end_idx}")

# Also find where garbage starts and ends
garbage_start = -1
for i in range(end_idx, len(lines)):
    if 'return page# [DECOMPILATION FAILED]' in lines[i] or 'return page' in lines[i]:
        garbage_start = i + 1
        break

garbage_end = -1
for i in range(garbage_start, len(lines)):
    if 'def page_timings(self, parent=None):' in lines[i]:
        garbage_end = i - 2
        break

print(f"garbage: {garbage_start} to {garbage_end}")
