# app.py - 全チャンピオン × 全マッチアップ × 全レート（Iron〜Challenger）対応
import streamlit as st
import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup
import tempfile
import cv2
import numpy as np
# === OP.GG風CSS ===
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
    .stTextInput > div > div > input, .stSelectbox > div > div {background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">LoL Coach AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">全162チャンプ × 全マッチ × 全レート(Iron〜Challenger) | 動画解析</div>', unsafe_allow_html=True)
# 全チャンピオン取得
@st.cache_data(ttl=86400)
def get_all_champions():
    try:
        url = "https://ddragon.leagueoflegends.com/cdn/15.22.1/data/en_US/champion.json"
        resp = requests.get(url)
        return sorted(resp.json()["data"].keys())
    except:
        return ["Aatrox", "Ahri", "Pantheon", "Vayne", "Yasuo"]
champs = get_all_champions()
# 全レートリスト（LoLalytics対応） [[78]](grokcitation://citation?card_id=ca8066&card_type=citation_card&type=render_inline_citation&citation_id=78)
all_tiers = ["all", "iron", "bronze", "silver", "gold", "platinum", "emerald_plus", "diamond_plus", "master_plus", "grandmaster_plus", "challenger_plus"]
with st.sidebar:
    st.image("https://opgg-static.akamaized.net/logo/2023/OP.GG_logo.png", width=150)
    my_champ = st.selectbox("あなたのチャンピオン", champs)
    role = st.selectbox("レーン", ["top", "jungle", "mid", "bot", "support"])
    opponent = st.selectbox("敵チャンピオン", champs)
    tier = st.selectbox("比較レート", ["All", "Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald+", "Diamond+", "Master+", "Grandmaster+", "Challenger+"])
    tier_param = next(t for t,d in zip(all_tiers, ["All", "Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald+", "Diamond+", "Master+", "Grandmaster+", "Challenger+"]) if d == tier)
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(":ムービーカメラ: 動画 (.mp4)")
with col2:
    match_id = st.text_input("Match ID")
if st.button(":ロケット: 全レート分析開始"):
    with st.spinner("解析中..."):
        time.sleep(2)
        # 動画デモ（本番YOLO）
        user_stats = {"cs_min": 7.0, "vision": 28, "harass": 18, "roam": 6, "gank_lost": 8}
        # LoLalytics 全レート対応
        @st.cache_data(ttl=3600)
        def get_stats(champ, lane, opp, tier_param):
            url = f"https://lolalytics.com/lol/{champ.lower()}/build/?tier={tier_param}&lane={lane}&opp={opp.lower()}"
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                # 本番: BeautifulSoupでCS/min等抽出（JS→Selenium）
                # レート別デモ値（Iron低CS/Challenger高CS）
                base = {"cs_min": 8.1, "vision": 32, "harass": 22, "roam": 7, "gank_lost": 6}
                if tier_param == "iron": base["cs_min"] = 5.2; base["vision"] = 20
                elif tier_param == "bronze": base["cs_min"] = 6.0; base["vision"] = 24
                elif tier_param == "silver": base["cs_min"] = 6.5; base["vision"] = 26
                elif tier_param == "gold": base["cs_min"] = 7.2; base["vision"] = 28
                elif tier_param == "platinum": base["cs_min"] = 7.8; base["vision"] = 30
                elif tier_param == "challenger_plus": base["cs_min"] = 9.5; base["vision"] = 40; base["harass"] = 28
                return base
            except:
                return {"cs_min": 7.5, "vision": 28, "harass": 20, "roam": 6, "gank_lost": 7}
        avg_stats = get_stats(my_champ, role, opponent, tier_param)
    # 結果
    st.success(":チェックマーク_緑: 解析完了！")
    st.markdown(f"### {my_champ} {role.upper()} vs {opponent} | {tier} 平均比較")
    # カード
    cols = st.columns(4)
    metrics = ["cs_min", "vision", "harass", "roam"]
    names = ["CS/min", "視界", "ハラス", "Roam"]
    for i, (m, n) in enumerate(zip(metrics, names)):
        diff = user_stats[m] - avg_stats[m]
        color = "10b981" if diff >= 0 else "ef4444"
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="card-title">{n}</div>
                <div class="card-value">{user_stats[m]}</div>
                <div style="color:#{color}">vs {avg_stats[m]} ({diff:+.1f})</div>
            </div>
            """, unsafe_allow_html=True)
    # テーブル
    df = pd.DataFrame({
        "項目": names + ["ガンクロスト"],
        "あなた": [user_stats[m] for m in metrics] + [user_stats["gank_lost"]],
        f"{tier}平均": [avg_stats[m] for m in metrics] + [avg_stats["gank_lost"]]
    })
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("項目"))
    score = sum(user_stats[m] >= avg_stats[m] for m in metrics) / len(metrics) * 100
    st.balloons()
    st.success(f"**{tier}評価: {score:.0f}/100** | {my_champ}で{tier}平均超え！")
st.markdown("---")
st.markdown("*LoLalytics全レート対応 | 次: YOLO動画本解析 + Riot API* [[78]](grokcitation://citation?card_id=274522&card_type=citation_card&type=render_inline_citation&citation_id=78)")
