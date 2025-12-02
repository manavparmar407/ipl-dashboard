import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
import plotly.io as pio
import tempfile
import os

# =============================
#   PAGE SETTINGS
# =============================
st.set_page_config(page_title="IPL Dashboard", layout="wide")

# =============================
#   NEON HEADER
# =============================
st.markdown(
    """
    <h1 style='text-align:center; 
    color:#00eaff; 
    text-shadow:0 0 20px #00eaff; 
    font-size:45px;'>
    🏏 IPL DATA ANALYTICS (2008–2022)
    </h1>
    """,
    unsafe_allow_html=True,
)

# =============================
#   LOGOS BANNER
# =============================
st.image("logos/all team.png", use_container_width=True)

# =============================
#   LOAD DATA
# =============================
matches = pd.read_csv("IPL_Matches_2008_2022.csv")
balls = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")

# ======================================================
# 🔍 NEW PREMIUM FILTERS WITH SEARCH BARS (REPLACED HERE)
# ======================================================
st.sidebar.header("Filters")

# ---- ONLY 10 ACTIVE IPL TEAMS ----
active_teams = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Rajasthan Royals",
    "Sunrisers Hyderabad",
    "Delhi Capitals",
    "Punjab Kings",
    "Gujarat Titans",
    "Lucknow Super Giants"
]

# ---- TEAM SEARCH ----
team_search = st.sidebar.text_input("🔍 Search Team")

filtered_teams = ["All Teams"] + [t for t in active_teams if team_search.lower() in t.lower()]
selected_team = st.sidebar.selectbox("Select Team", filtered_teams)

# ---- PLAYER SEARCH ----
all_players = sorted(list(set(balls["batter"].unique().tolist() + balls["bowler"].unique().tolist())))

player_search = st.sidebar.text_input("🔍 Search Player")

filtered_players = ["All Players"] + [p for p in all_players if player_search.lower() in p.lower()]
selected_player = st.sidebar.selectbox("Select Player", filtered_players)

# ---- SEASON FILTER ----
available_seasons = sorted(matches["Season"].unique())
selected_seasons = st.sidebar.multiselect("Select Seasons", available_seasons, default=available_seasons)

# ---- APPLY FILTERS ----
df = matches[matches["Season"].isin(selected_seasons)]
balls_filtered = balls[balls["ID"].isin(df["ID"])]

if selected_team != "All Teams":
    df = df[(df["Team1"] == selected_team) | (df["Team2"] == selected_team)]
    balls_filtered = balls_filtered[balls_filtered["BattingTeam"] == selected_team]

if selected_player != "All Players":
    balls_filtered = balls_filtered[
        (balls_filtered["batter"] == selected_player) | (balls_filtered["bowler"] == selected_player)
    ]

# ======================================================
#   SECTION TITLE WITH ICONS
# ======================================================
def section_title(icon, text):
    st.markdown(
        f"""
        <h2 style='color:#ff66ff; text-shadow:0 0 15px #ff66ff;'>
        {icon} {text}
        </h2>
        """,
        unsafe_allow_html=True,
    )

# ======================================================
#   1 — WINNING TEAMS
# ======================================================
section_title("🏆", "Top Winning Teams")

top_wins = df["WinningTeam"].value_counts().head(10)
fig1 = px.bar(
    top_wins,
    x=top_wins.index,
    y=top_wins.values,
    labels={"x": "Team", "y": "Wins"},
    template="plotly_dark",
)
st.plotly_chart(fig1, use_container_width=True)

# ======================================================
#   2 — SIX HITTERS
# ======================================================
section_title("💥", "Top Six Hitters")

sixes = balls_filtered.groupby("batter")["batsman_run"].apply(lambda x: (x == 6).sum()).sort_values(ascending=False).head(10)

fig2 = px.bar(
    sixes,
    x=sixes.index,
    y=sixes.values,
    labels={"x": "Batsman", "y": "Sixes"},
    template="plotly_dark",
)
st.plotly_chart(fig2, use_container_width=True)

# ======================================================
#   3 — WICKET TAKERS
# ======================================================
section_title("🎯", "Top Wicket Takers")

wickets = balls_filtered[balls_filtered["isWicketDelivery"] == 1]["bowler"].value_counts().head(10)

fig3 = px.bar(
    wickets,
    x=wickets.index,
    y=wickets.values,
    labels={"x": "Bowler", "y": "Wickets"},
    template="plotly_dark",
)
st.plotly_chart(fig3, use_container_width=True)

# ======================================================
#   4 — MATCHES PER SEASON
# ======================================================
section_title("📊", "Matches Per Season")

season_count = df["Season"].value_counts().sort_index()

fig4 = px.line(
    season_count,
    x=season_count.index,
    y=season_count.values,
    labels={"x": "Season", "y": "Matches"},
    markers=True,
    template="plotly_dark",
)
st.plotly_chart(fig4, use_container_width=True)


st.success("Dashboard Loaded Successfully 🎉")
