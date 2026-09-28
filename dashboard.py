import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Music Taste Analyzer",
    page_icon="🎵",
    layout="wide"
)

# Load dataset
df = pd.read_csv("music_taste_dataset.csv")

# Title
st.title("🎵 Music Taste Analyzer")
st.write("Discover your music personality!")

st.divider()

# Top statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎧 Total Songs", len(df))

with col2:
    st.metric("🎤 Artists", df["Artist"].nunique())

with col3:
    st.metric("🎼 Genres", df["Genre"].nunique())

with col4:
    st.metric("⚡ Avg Energy", round(df["Energy"].mean(), 1))

st.divider()

# Sidebar
st.sidebar.header("🎛️ Music Filters")

genres = ["All"] + sorted(df["Genre"].unique().tolist())
languages = ["All"] + sorted(df["Language"].unique().tolist())
moods = ["All"] + sorted(df["Mood"].unique().tolist())

selected_genre = st.sidebar.selectbox("Genre", genres)
selected_language = st.sidebar.selectbox("Language", languages)
selected_mood = st.sidebar.selectbox("Mood", moods)

# Filtering
filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["Genre"] == selected_genre
    ]

if selected_language != "All":
    filtered_df = filtered_df[
        filtered_df["Language"] == selected_language
    ]

if selected_mood != "All":
    filtered_df = filtered_df[
        filtered_df["Mood"] == selected_mood
    ]

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎼 Favorite Genres")

    genre_count = df["Genre"].value_counts()
    st.bar_chart(genre_count)

with col2:
    st.subheader("⚡ Song Energy")

    energy_data = df[["Song", "Energy"]].set_index("Song")
    st.bar_chart(energy_data)

st.divider()

# Music personality
favorite_genre = df["Genre"].value_counts().idxmax()
favorite_mood = df["Mood"].value_counts().idxmax()

st.subheader("❤️ Your Music Personality")

st.info(
    f"Your favorite genre is **{favorite_genre}** 🎵\n\n"
    f"Your most common mood is **{favorite_mood}** 💖"
)

# Recommendations
st.subheader("🎧 Recommended Songs")

recommendations = filtered_df.sort_values(
    by="Energy",
    ascending=False
)

st.dataframe(
    recommendations[
        ["Song", "Artist", "Genre", "Language", "Year", "Energy", "Mood"]
    ],
    use_container_width=True
)