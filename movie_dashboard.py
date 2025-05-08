import pandas as pd
import plotly.express as px
import streamlit as st
from ast import literal_eval
import collections

# --- Page Config ---
st.set_page_config(page_title="🎬 Movie Dashboard", layout="wide")

# --- Custom Styling ---
# --- Custom Header Styling ---
st.markdown("""
    <style>
    .header {
        background: linear-gradient(90deg, rgba(255, 94, 77, 1) 0%, rgba(255, 218, 128, 1) 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header h1 {
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .header p {
        font-size: 1.2rem;
        font-weight: 300;
    }
    </style>
    <div class="header">
        <h1>🎬 Movie Dashboard</h1>
        <p>Explore top-rated movies by genre, actors, and keywords</p>
    </div>
""", unsafe_allow_html=True)


# --- Load Data ---
df = pd.read_csv("movies_metadata.csv", low_memory=False)
credits = pd.read_csv("credits.csv")
keywords = pd.read_csv("keywords.csv")

df["id"] = df["id"].astype(str)
credits["id"] = credits["id"].astype(str)
keywords["id"] = keywords["id"].astype(str)

# Merge data
df = df.merge(credits[['id', 'cast']], on='id', how='left')
df = df.merge(keywords[['id', 'keywords']], on='id', how='left')

df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
df = df[df["genres"].notna()]

# --- Extract Top Actors ---
def get_top_actors(cast):
    if isinstance(cast, str):
        cast_list = eval(cast)
        top_actors = [actor['name'] for actor in cast_list[:5]]
        return ", ".join(top_actors)
    return ""

df['top_actors'] = df['cast'].apply(get_top_actors)

# --- UI Title ---
#st.title("🎬 Movie Dashboard")
st.markdown("Use the filters below to explore top-rated movies by genre, vote count, and rating.")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Filters")
    genre = st.selectbox("🎭 Choose Genre", ["Action", "Comedy", "Drama", "Horror", "Animation", "Romance"])
    min_votes = st.slider("👍 Minimum Votes", 0, int(df["vote_count"].max()), 100)
    min_rating = st.slider("⭐ Minimum Rating", 0.0, 10.0, 5.0, step=0.1)

# --- Filter Data ---
filtered = df[
    df["genres"].str.contains(genre, na=False) &
    (df["vote_count"] >= min_votes) &
    (df["vote_average"] >= min_rating)
]

top_movies = filtered.sort_values(by="vote_average", ascending=False).head(10)

# --- Top Movies Chart ---
st.subheader(f"🏆 Top 10 {genre} Movies")
fig = px.bar(
    top_movies,
    x="title",
    y="vote_average",
    color="vote_average",
    color_continuous_scale="Viridis",
    title="Top Rated Movies",
    labels={"vote_average": "Rating", "title": "Movie Title"}
)
st.plotly_chart(fig, use_container_width=True)

# --- Top Actors ---
st.subheader(f"👨‍🎤 Top Actors in {genre} Movies")
actor_list = []

for cast in filtered[filtered["cast"].notna()]["cast"]:
    try:
        actors = literal_eval(cast)
        actor_names = [actor["name"] for actor in actors[:3]]
        actor_list.extend(actor_names)
    except:
        continue

actor_counts = collections.Counter(actor_list)
top_actors = actor_counts.most_common(10)
actor_df = pd.DataFrame(top_actors, columns=["Actor", "Appearances"])

fig_actors = px.bar(
    actor_df,
    x="Actor",
    y="Appearances",
    title="Top 10 Actors",
    color="Appearances",
    color_continuous_scale="Bluered"
)
st.plotly_chart(fig_actors, use_container_width=True)

# --- Top Keywords ---
st.subheader(f"🔑 Top Keywords in {genre} Movies")
keyword_list = []

for kws in filtered[filtered["keywords"].notna()]["keywords"]:
    try:
        kws_data = literal_eval(kws)
        keyword_names = [kw["name"] for kw in kws_data]
        keyword_list.extend(keyword_names)
    except:
        continue

keyword_counts = collections.Counter(keyword_list)
top_keywords = keyword_counts.most_common(10)
keyword_df = pd.DataFrame(top_keywords, columns=["Keyword", "Count"])

fig_keywords = px.bar(
    keyword_df,
    x="Keyword",
    y="Count",
    title="Top Keywords",
    color="Count",
    color_continuous_scale="Pinkyl"
)
st.plotly_chart(fig_keywords, use_container_width=True)

# --- Top Actors Table ---
st.markdown("### 🎬 Top Actors Across All Movies")
st.dataframe(df[['title', 'top_actors']].head(10))
