import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- Load and parse the MapReduce output ----
def load_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                hour_part, topics_part = line.split('\t')
                topics_list = topics_part.split(', ')
                for t in topics_list:
                    topic, count = t.split(':')
                    data.append({
                        'hour': hour_part,
                        'topic': topic,
                        'count': int(count)
                    })
            except:
                continue
    return pd.DataFrame(data)

df = load_data('C:/Users/syedj/OneDrive/Desktop/JawadAhmad-221980065/output/part-00000')

# ---- Streamlit UI ----
st.title("Hourly Trending Topics Dashboard")

st.sidebar.header("Filters")
selected_hour = st.sidebar.selectbox("Select Hour", sorted(df['hour'].unique()))
top_n = st.sidebar.slider("Top N Topics", 1, 20, 10)

# Filter for selected hour
hour_df = df[df['hour'] == selected_hour].sort_values(by='count', ascending=False).head(top_n)

st.subheader(f"Top {top_n} Topics for Hour: {selected_hour}")

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(hour_df['topic'][::-1], hour_df['count'][::-1], color='skyblue')
ax.set_xlabel("Count")
ax.set_ylabel("Topic")
st.pyplot(fig)

# ---- Trend over time for selected topics ----
st.subheader("Trend of Selected Topics Over Hours")

selected_topics = st.multiselect("Select topics to track", df['topic'].unique())

if selected_topics:
    trend_df = df[df['topic'].isin(selected_topics)]
    pivot_df = trend_df.pivot_table(index='hour', columns='topic', values='count', fill_value=0).sort_index()
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    pivot_df.plot(ax=ax2)
    ax2.set_ylabel("Count")
    ax2.set_title("Topic Trends Over Hours")
    st.pyplot(fig2)

# ---- Show raw data ----
if st.checkbox("Show Raw Data"):
    st.write(df)
