#!/usr/bin/env python
import sys
import re

for line in sys.stdin:
    try:
        line = line.strip()
        if not line or '\t' not in line:
            continue
        hour, text = line.split('\t', 1)
        # Extract words: sequences of at least 3 lowercase letters.
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        for word in words:
            print "%s\t%s\t1" % (hour, word)
    except Exception as e:
        continue
