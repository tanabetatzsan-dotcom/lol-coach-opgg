# app.py - OP.GG風 LoL Coach AI
import streamlit as st
import pandas as pd
import time
# === CSS: OP.GG風デザイン ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Roboto:wght@400&display=swap');
    .main {background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%); color: #c9d1d9; font-family: 'Roboto', sans-serif;}
    .title {font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 2.8rem; background: linear-gradient(90deg, #64b5f6, #42a5f5);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 10px;}
    .subtitle {text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 30px;}
    .stat-card {background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 16px; margin: 10px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s;}
    .stat-card:hover {border-color: #58a6ff; transform: translateY(-2px);}
    .card-title {color: #58a6ff; font-weight: 600; margin-bottom: 8px; font-size: 0.9rem;}
    .card-value {font-size: 1.8rem; font-weight: 700; color: #f0f6fc;}
    .stButton > button {background: linear-gradient(90deg, #238636, #2ea043); color: white; border: none; border-radius: 8px;
                        padding: 12px 24px; font-weight: 600; font-size: 1rem; width: 100%;}
    .stButton > button:hover {background: linear-gradient(90deg, #2ea043, #238636); transform: translateY(-2px);}
    .stTextInput > div > div > input {background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">LoL Coach AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pantheon Platinum vs Emerald+ | マッチアップ調整分析</div>', unsafe_allow_html=True)
with st.sidebar:
    st.image("https://opgg-static.akamaized.net/logo/2023/OP.GG_logo.png", width=150)
    role = st.selectbox("ロール", ["Top", "Mid", "Support", "Jungle"])
    opponent = st.text_input("敵チャンピオン", "Vayne")
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("ゲーム動画 (.mp4)", type=["mp4"])
with col2:
    match_id = st.text_input("Match ID")
if st.button("分析開始"):
    with st.spinner("解析中..."):
        time.sleep(2)
        user = {"cs_min": 6.8, "vision": 28, "dpm": 680, "wr": 48.0, "harass": 17, "roam": 5, "gank_lost": 8}
        emerald = {"cs_min": 7.5, "vision": 30, "dpm": 680, "wr": 42.0, "harass": 18, "roam": 6, "gank_lost": 8} if "vayne" in opponent.lower() else \
                  {"cs_min": 8.1, "vision": 35, "dpm": 750, "wr": 51.5, "harass": 22, "roam": 7, "gank_lost": 6}
    st.markdown("### 対面マッチアップ分析")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="card-title">CS/min</div><div class="card-value">{user["cs_min"]}</div><div style="color:#{"10b981" if user["cs_min"]>=emerald["cs_min"] else "ef4444"}">vs {emerald["cs_min"]} ({user["cs_min"]-emerald["cs_min"]:+.1f})</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="card-title">視界スコア</div><div class="card-value">{user["vision"]}</div><div style="color:#10b981">vs {emerald["vision"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="card-title">DPM</div><div class="card-value">{user["dpm"]}</div><div style="color:#10b981">vs {emerald["dpm"]}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><div class="card-title">Win Rate</div><div class="card-value">{user["wr"]}%</div><div style="color:#10b981">vs {emerald["wr"]}% ({user["wr"]-emerald["wr"]:+.1f}%)</div></div>', unsafe_allow_html=True)
    df = pd.DataFrame({
        "項目": ["CS/min", "ハラス回数", "Roam回数", "ガンクロストCS"],
        "あなた": [6.8, 17, 5, 8],
        "vs相手 Emerald平均": [emerald["cs_min"], emerald["harass"], emerald["roam"], emerald["gank_lost"]]
    })
    st.dataframe(df.style.highlight_max(axis=1), use_container_width=True)
    st.success(f"**{opponent}戦でCS 6.8は優秀！** Emerald平均並み → 波管理が鍵")
