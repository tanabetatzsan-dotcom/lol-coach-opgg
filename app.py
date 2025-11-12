# app.py - 全チャンピオン×全マッチアップ動画分析Webサービス
import streamlit as st
import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup
import cv2  # 動画解析（簡易デモ）
import numpy as np
# OP.GG風CSS（前と同じ）
st.markdown("""
<style>
    /* 前のCSS省略（コピペ） */
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">LoL Coach AI - 全チャンピオン対応</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">全162体×全マッチアップ | 動画解析 + Emerald+比較</div>', unsafe_allow_html=True)
# 全チャンピオンリスト取得（Riot DataDragon）
@st.cache_data(ttl=86400)  # 1日キャッシュ
def get_all_champions():
    url = "https://ddragon.leagueoflegends.com/cdn/15.22/data/en_US/champion.json"  # 最新パッチ
    resp = requests.get(url)
    data = resp.json()["data"]
    return list(data.keys())  # ['Aatrox', 'Ahri', ...]
champs = get_all_champions()
with st.sidebar:
    my_champ = st.selectbox("あなたのチャンピオン", champs, index=champs.index('Pantheon'))
    role = st.selectbox("レーン", ["top", "mid", "sup", "jg", "bot"])
    opponent = st.selectbox("敵チャンピオン", champs, index=champs.index('Vayne'))
    tier = st.selectbox("比較ティア", ["platinum", "emerald_plus"])
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(":ムービーカメラ: 動画アップロード (.mp4)")
with col2:
    match_id = st.text_input(":リンク: Match ID (Riot API補正)")
if st.button(":ロケット: 全マッチアップ分析開始"):
    with st.spinner("YOLO解析 + LoLalytics取得中..."):
        time.sleep(3)  # シミュ（本番: CV実行）
        # 動画解析デモ（本番: YOLOv8 CS/harass検出）
        if uploaded_file:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video = cv2.VideoCapture(tfile.name)
            # YOLO+OCRでCS/min等抽出（GitHub LeagueAI実装）
            user_stats = {"cs_min": 7.2, "vision": 28, "harass": 18, "roam": 6, "gank_lost": 8}
        else:
            user_stats = {"cs_min": 7.0, "vision": 26, "harass": 17, "roam": 5, "gank_lost": 9}
        # LoLalyticsスクレイプ（全マッチ対応）
        @st.cache_data(ttl=3600)
        def get_lolalytics_stats(champ, lane, opp, tier):
            url = f"https://lolalytics.com/lol/{champ}/build/?tier={tier}&lane={lane}&opp={opp}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            # JSレンダー→Selenium or キャッシュ実データ（本番: 数値抽出）
            return {"cs_min": 8.1, "vision": 32, "harass": 22, "roam": 7, "gank_lost": 6}  # デモ
        avg_stats = get_lolalytics_stats(my_champ.lower(), role, opponent.lower(), tier)
        # 比較/フィードバック
        df = pd.DataFrame({
            "項目": ["CS/min", "視界スコア", "ハラス回数", "Roam回数", "ガンクロストCS"],
            "あなた": [user_stats[k] for k in user_stats],
            f"{tier.title()}平均": [avg_stats[k] for k in user_stats]
        })
        st.dataframe(df)
        st.bar_chart(df.set_index("項目"))
        st.success(f"**{my_champ} vs {opponent} ({role}): CS優秀！ Emerald+ {tier}調整後スコア: 82/100**")
# requirements.txt追加: opencv-python beautifulsoup4 lxml ultralytics（YOLO）






19:16
# app.py - 全チャンピオン×全マッチアップ動画分析Webサービス
import streamlit as st
import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup
import cv2  # 動画解析（簡易デモ）
import numpy as np
# OP.GG風CSS（前と同じ）
st.markdown("""
<style>
    /* 前のCSS省略（コピペ） */
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">LoL Coach AI - 全チャンピオン対応</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">全162体×全マッチアップ | 動画解析 + Emerald+比較</div>', unsafe_allow_html=True)
# 全チャンピオンリスト取得（Riot DataDragon）
@st.cache_data(ttl=86400)  # 1日キャッシュ
def get_all_champions():
    url = "https://ddragon.leagueoflegends.com/cdn/15.22/data/en_US/champion.json"  # 最新パッチ
    resp = requests.get(url)
    data = resp.json()["data"]
    return list(data.keys())  # ['Aatrox', 'Ahri', ...]
champs = get_all_champions()
with st.sidebar:
    my_champ = st.selectbox("あなたのチャンピオン", champs, index=champs.index('Pantheon'))
    role = st.selectbox("レーン", ["top", "mid", "sup", "jg", "bot"])
    opponent = st.selectbox("敵チャンピオン", champs, index=champs.index('Vayne'))
    tier = st.selectbox("比較ティア", ["platinum", "emerald_plus"])
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader(":ムービーカメラ: 動画アップロード (.mp4)")
with col2:
    match_id = st.text_input(":リンク: Match ID (Riot API補正)")
if st.button(":ロケット: 全マッチアップ分析開始"):
    with st.spinner("YOLO解析 + LoLalytics取得中..."):
        time.sleep(3)  # シミュ（本番: CV実行）
        # 動画解析デモ（本番: YOLOv8 CS/harass検出）
        if uploaded_file:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video = cv2.VideoCapture(tfile.name)
            # YOLO+OCRでCS/min等抽出（GitHub LeagueAI実装）
            user_stats = {"cs_min": 7.2, "vision": 28, "harass": 18, "roam": 6, "gank_lost": 8}
        else:
            user_stats = {"cs_min": 7.0, "vision": 26, "harass": 17, "roam": 5, "gank_lost": 9}
        # LoLalyticsスクレイプ（全マッチ対応）
        @st.cache_data(ttl=3600)
        def get_lolalytics_stats(champ, lane, opp, tier):
            url = f"https://lolalytics.com/lol/{champ}/build/?tier={tier}&lane={lane}&opp={opp}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            # JSレンダー→Selenium or キャッシュ実データ（本番: 数値抽出）
            return {"cs_min": 8.1, "vision": 32, "harass": 22, "roam": 7, "gank_lost": 6}  # デモ
        avg_stats = get_lolalytics_stats(my_champ.lower(), role, opponent.lower(), tier)
        # 比較/フィードバック
        df = pd.DataFrame({
            "項目": ["CS/min", "視界スコア", "ハラス回数", "Roam回数", "ガンクロストCS"],
            "あなた": [user_stats[k] for k in user_stats],
            f"{tier.title()}平均": [avg_stats[k] for k in user_stats]
        })
        st.dataframe(df)
        st.bar_chart(df.set_index("項目"))
        st.success(f"**{my_champ} vs {opponent} ({role}): CS優秀！ Emerald+ {tier}調整後スコア: 82/100**")

