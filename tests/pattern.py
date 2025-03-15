import re

plate_pattern = re.compile(r'^[A-Z]\d[A-Z]-\d{3}$')

if plate_pattern.match("A1B-234"):
    print("PASA")
else:
    print("NO PASA")
