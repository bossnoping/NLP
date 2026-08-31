with open('Group_10.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = re.findall(r'<div class="section-title">(.*?)</div>', text)
print(f"Total Section Titles found: {len(sections)}")
for i, s in enumerate(sections, 1):
    print(f"Section {i}: {s}")
