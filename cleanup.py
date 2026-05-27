import re

with open('omnisec_engine.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Remove orphaned logger.error blocks
pattern = r'\n\s{12}logger\.error\(f\[.*?\] \{target_ip\}: \{e\}\"\)\n\s{12}return False\n'
content = re.sub(pattern, '\n', content)

# Also remove any remaining orphaned logger.error lines
lines = content.split('\n')
cleaned_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    if re.match(r'^\s{12}logger\.error\(f\[.*?\] \{target_ip\}: \{e\}\"\)', line):
        # Check if next line is return False
        if i + 1 < len(lines) and lines[i+1].strip() == 'return False':
            skip_next = True
        continue
    cleaned_lines.append(line)

with open('omnisec_engine.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(cleaned_lines))

print('Cleaned up orphaned logger.error lines')