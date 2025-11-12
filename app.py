# app.py - OP.GG風 LoL Coach AI v3
# コピペで即公開 → https://yourname-lol-coach-opgg.streamlit.app

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# === OP.GG風カスタムCSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Roboto:wght@400;500&display=swap');

    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: #c9d1d9;
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background: transparent;
    }

    /* タイトル */
    .title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #64b5f6, #42a5f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* カード */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }
    .stat-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }
    .card-title {
        color: #58a6ff;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
    .card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f0f6fc;
    }

    /* ボタン */
    .stButton > button {
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2ea043, #238636);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46,160,67,0.4);
    }

    /* 入力 */
    .stTextInput > div > div > input {
        background: #0d1117;
        border: 1px solid #30363d;
        color: #c9d1d9;
        border-radius: 8px;
    }

    /* テーブル */
    .dataframe {
        background: #161b22;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# === タイトル ===
st.markdown('<div class="title">LoL Coach AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pantheon Platinum vs Emerald+ | マッチアップ調整済み分析</div>', unsafe_allow_html=True)

# === サイドバー ===
with st.sidebar:
    st.image("https://opgg-static.akamaized.net/logo/2023/OP.GG_logo.png", width=150)
    st.markdown("### 設定")
    role = st.selectbox("ロール", ["Top", "Mid", "Support", "Jungle"])
    opponent = st.text_input("敵チャンピオン", "Vayne")
    st.markdown("---")
    st.markdown("**Patch 15.22**")

# === メイン入力 ===
col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("ゲーム動画 (.mp4)", type=["mp4"])
with col2:
    match_id = st.text_input("Match ID")

analyze = st.button("分析開始")

# === ダミーデータ（本番はRiot API + CV）===
if analyze:
    with st.spinner("解析中..."):
        time.sleep(2)

        user = {
            "cs_min": 6.8, "vision": 28, "dpm": 680, "kda": "3.9/2.4/6.0",
            "kp": 60, "harass": 17, "roam": 5, "gank_lost": 8, "wr": 48.0
        }

        emerald_matchup = {
            "cs_min": 7.5, "vision": 30, "dpm": 680, "wr": 42.0,
            "harass": 18, "roam": 6, "gank_lost": 8
        } if "vayne" in opponent.lower() else {
            "cs_min": 8.1, "vision": 35, "dpm": 750, "wr": 51.5,
            "harass": 22, "roam": 7, "gank_lost": 6
        }

    # === 統計カード ===
    st.markdown("### 対面マッチアップ分析")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="card-title">CS/min</div>
            <div class="card-value">{user['cs_min']}</div>
            <div style="color:#{ '10b981' if user['cs_min'] >= emerald_matchup['cs_min'] else 'ef4444'}; font-size:0.9rem;">
            vs {emerald_matchup['cs_min']} ({user['cs_min'] - emerald_matchup['cs_min']:+.1f})
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="card-title">視界スコア</div>
            <div class="card-value">{user['vision']}</div>
            <div style="color:#10b981; font-size:0.9rem;">vs {emerald_matchup['vision']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="card-title">DPM</div>
            <div class="card-value">{user['dpm']}</div>
            <div style="color:#10b981; font-size:0.9rem;">vs {emerald_matchup['dpm']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="card-title">Win Rate</div>
            <div class="card-value">{user['wr']}%</div>
            <div style="color:#10b981; font-size:0.9rem;">
            vs {emerald_matchup['wr']}% ({user['wr'] - emerald_matchup['wr']:+.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === 詳細テーブル ===
    st.markdown("### 詳細比較")
    df = pd.DataFrame({
        "項目": ["CS/min", "ハラス回数", "Roam回数", "ガンクロストCS"],
        "あなた": [6.8, 17, 5, 8],
        "vs相手 Emerald平均": [emerald_matchup['cs_min'], emerald_matchup['harass'], emerald_matchup['roam'], emerald_matchup['gank_lost']],
        "差": [-0.7, -1, -1, 0]
    })
    st.dataframe(df.style.highlight_max(axis=1), use_container_width=True)

    # === フィードバック ===
    st.markdown("### AIコーチング")
    st.success(f"**{opponent}戦でCS 6.8は優秀！** Emerald平均並み → 波管理が鍵")  
