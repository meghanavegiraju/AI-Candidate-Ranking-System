import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("output/ranked_candidates.csv")

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🤖 AI Recruitment Assistant")

st.sidebar.markdown("---")

min_score = st.sidebar.slider(
    "Minimum Match Score",
    0.0,
    1.0,
    0.30,
    0.05
)

filtered_df = df[df["final_score"] >= min_score]

candidate_id = st.sidebar.selectbox(
    "Select Candidate",
    filtered_df["candidate_id"]
)

csv = filtered_df.to_csv(index=False)

st.sidebar.download_button(
    "⬇ Download Results",
    csv,
    file_name="ranked_candidates.csv",
    mime="text/csv"
)

candidate = filtered_df[
    filtered_df["candidate_id"] == candidate_id
].iloc[0]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🤖 AI Candidate Ranking Dashboard")

st.markdown(
"""
This dashboard ranks candidates using:

- Semantic Search
- Skill Matching
- Experience Analysis
- Behavioral Signals
- Hybrid AI Scoring
"""
)

st.markdown("---")

# ---------------------------------------------------
# KPI
# ---------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric(
    "Candidates",
    len(filtered_df)
)

c2.metric(
    "Top Score",
    f"{filtered_df['final_score'].max()*100:.1f}%"
)

c3.metric(
    "Average Score",
    f"{filtered_df['final_score'].mean()*100:.1f}%"
)

st.markdown("---")

# ---------------------------------------------------
# TOP CANDIDATES
# ---------------------------------------------------
st.subheader("🏆 Top 5 Candidates")

top5 = filtered_df.head(5)

st.dataframe(
    top5[
[
"rank",
"candidate_id",
"semantic_score",
"skill_score",
"experience_score",
"behavior_score",
"final_score"
]
],
    use_container_width=True
)

st.markdown("---")

# ---------------------------------------------------
# PROFILE
# ---------------------------------------------------
st.subheader("👤 Candidate Profile")

left, right = st.columns([1,2])

with left:

    st.metric(
        "Overall Match",
        f"{candidate['final_score']*100:.1f}%"
    )

    st.metric(
        "Rank",
        int(candidate["rank"])
    )

    score = candidate["final_score"]

    if score >= 0.80:
        st.success("⭐⭐⭐⭐⭐ Highly Recommended")

    elif score >= 0.60:
        st.success("⭐⭐⭐⭐ Recommended")

    elif score >= 0.45:
        st.warning("⭐⭐⭐ Consider")

    else:
        st.error("⭐⭐ Not Recommended")

with right:

    st.subheader("🤖 AI Recruiter Summary")

    st.info(candidate["reason"])

st.markdown("---")
# ---------------------------------------------------
# CANDIDATE COMPARISON
# ---------------------------------------------------

st.markdown("---")

st.subheader("⚖️ Candidate Comparison")

col1, col2 = st.columns(2)

with col1:
    compare_a = st.selectbox(
        "Candidate A",
        df["candidate_id"],
        key="compare_a"
    )

with col2:
    compare_b = st.selectbox(
        "Candidate B",
        df["candidate_id"],
        index=1,
        key="compare_b"
    )

cand_a = df[df["candidate_id"] == compare_a].iloc[0]
cand_b = df[df["candidate_id"] == compare_b].iloc[0]

comparison = pd.DataFrame({

    "Feature":[
        "Rank",
        "Overall Match",
        "Semantic Score",
        "Skill Score",
        "Experience Score",
        "Behavior Score"
    ],

    compare_a:[
        cand_a["rank"],
        f"{cand_a['final_score']*100:.1f}%",
        f"{cand_a['semantic_score']*100:.1f}%",
        f"{cand_a['skill_score']*100:.1f}%",
        f"{cand_a['experience_score']*100:.1f}%",
        f"{cand_a['behavior_score']*100:.1f}%"
    ],

    compare_b:[
        cand_b["rank"],
        f"{cand_b['final_score']*100:.1f}%",
        f"{cand_b['semantic_score']*100:.1f}%",
        f"{cand_b['skill_score']*100:.1f}%",
        f"{cand_b['experience_score']*100:.1f}%",
        f"{cand_b['behavior_score']*100:.1f}%"
    ]

})

st.dataframe(
    comparison,
    use_container_width=True
)
# ---------------------------------------------------
# SCORE CARDS
# ---------------------------------------------------
st.subheader("📊 AI Score Breakdown")

a, b, c, d = st.columns(4)

a.metric(
    "Semantic",
    f"{candidate['semantic_score']*100:.1f}%"
)

b.metric(
    "Skills",
    f"{candidate['skill_score']*100:.1f}%"
)

c.metric(
    "Experience",
    f"{candidate['experience_score']*100:.1f}%"
)

d.metric(
    "Behavior",
    f"{candidate['behavior_score']*100:.1f}%"
)

st.markdown("---")

# ---------------------------------------------------
# PROGRESS BARS
# ---------------------------------------------------
st.subheader("📈 Match Analysis")

st.write("Semantic Match")
st.progress(float(candidate["semantic_score"]))

st.write("Skill Match")
st.progress(float(candidate["skill_score"]))

st.write("Experience Match")
st.progress(float(candidate["experience_score"]))

st.write("Behavior Match")
st.progress(float(candidate["behavior_score"]))

st.markdown("---")

# ---------------------------------------------------
# SCORE DISTRIBUTION
# ---------------------------------------------------
st.subheader("📉 Candidate Score Distribution")

chart = filtered_df.set_index(
    "candidate_id"
)["final_score"]

st.line_chart(chart)

st.markdown("---")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.caption(
    "Developed using Sentence Transformers, Hybrid AI Ranking, Semantic Search, and Explainable AI."
)