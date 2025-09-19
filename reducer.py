#!/usr/bin/env python
import sys
from collections import defaultdict

current_hour = None
word_counts = defaultdict(int)

for line in sys.stdin:
    try:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 3:
            continue
        hour, word, count = parts
        count = int(count)

        if current_hour and current_hour != hour:
            # Get top 5 words for the previous hour.
            top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:5]
            formatted = ', '.join(["%s:%d" % (w, c) for w, c in top_words])
            print "%s\t%s" % (current_hour, formatted)
            word_counts = defaultdict(int)
        current_hour = hour
        word_counts[word] += count
    except:
        continue

if current_hour:
    top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:5]
    formatted = ', '.join(["%s:%d" % (w, c) for w, c in top_words])
    print "%s\t%s" % (current_hour, formatted)
