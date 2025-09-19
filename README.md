# MapReduce-Based Hourly Trending Topics Analysis

This repository contains a Hadoop MapReduce pipeline that identifies **top trending topics per hour** from timestamped tweet data, plus a Streamlit dashboard for interactive visualization.

---

## 🚀 Features
- **Mapper (`mapper.py`)** — parses each line, extracts `(hour, word)` pairs, and emits `(hour, word, 1)`.
- **Reducer (`reducer.py`)** — aggregates counts and outputs the **top N (default 5)** words per hour.
- **Visualization (`visualization.py`)** — Streamlit app to explore top topics per hour and their trends over time.
- **Report (`report.docx`)** — project write‑up with approach, pipeline, and insights.

---

## 📊 Input Data
- **Expected format:** Each line has a timestamp and tweet text separated by a tab. The timestamp is `YYYY-MM-DD HH` (hour precision).
- **Example:**
  ```
  2015-02-24 11\t@virginamerica what @dhepburn said.
  2015-02-24 11\t@virginamerica plus you've added commercials to the experience... tacky.
  ```
- Place your input file (e.g., `tweets.txt`) into HDFS (see below).

---

## ⚙️ Running on Hadoop (Streaming)
Use Hadoop Streaming to run the mapper and reducer.

```bash
# 1) Put input into HDFS
hdfs dfs -mkdir -p /user/<yourname>/queries
hdfs dfs -put /path/to/tweets.txt /user/<yourname>/queries/tweets.txt

# 2) Run Hadoop Streaming
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -files src/mapper.py,src/reducer.py \
  -mapper "python mapper.py" \
  -reducer "python reducer.py" \
  -input /user/<yourname>/queries/tweets.txt \
  -output /user/<yourname>/output/topics_by_hour

# 3) Fetch output locally (optional)
hdfs dfs -cat /user/<yourname>/output/topics_by_hour/part-* | head
hdfs dfs -get  /user/<yourname>/output/topics_by_hour  ./data/output/
```

**Reducer output format (example):**
```
2015-02-24 11\tamericanair:132, united:85, flight:70, delay:54, service:50
```

---

## 📈 Visualization (Streamlit)
1. Install Python deps (see **Installation** below).
2. Make sure the Streamlit script can find your MapReduce output. In `visualization.py`, update the path that loads the output (e.g., `.../output/part-00000`) to your local file path, or move the file to a known location.
3. Run:
   ```bash
   streamlit run visualization.py
   ```
4. Use the sidebar to select an hour and the number of top topics to display; optionally plot trends for specific topics over time.

> Tip: You can copy the HDFS output `part-00000` file to `data/output/part-00000` and point the script there for convenience.

---

## 🛠️ Installation
```bash
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- Hadoop (for the production MapReduce run) — not installed via pip
- Python libraries: `streamlit`, `pandas`, `matplotlib`

---

## ✅ Local Dry-Run (Optional)
If you want to test logic locally without Hadoop, you can simulate streaming by piping data:
```bash
# Simulate mapper on a small sample
python mapper.py < data/sample_tweets.txt | head

# Simulate reducer (mapper output must be sorted/grouped by hour then word if needed)
python mapper.py < data/sample_tweets.txt | sort | python reducer.py | head
```
> For large datasets and correct grouping, use Hadoop as above.

---
