import streamlit as st
import pandas as pd

# スマホで見やすい画面設定
st.set_page_config(page_title="自分専用 競馬AI", layout="wide")

st.title("🏇 自分専用 競馬AI予想")

# 1. レース選択エリア（まずは仮のメニュー）
col1, col2, col3 = st.columns(3)
with col1:
    date = st.selectbox("開催日", ["11/29(日)", "11/28(土)"])
with col2:
    place = st.selectbox("競馬場", ["東京", "京都", "小倉"])
with col3:
    race = st.selectbox("レース", ["11R ジャパンC", "12R 最終レース", "1R 未勝利"])

st.subheader(f"{date} {place} {race}")

# 2. スコアモード切替
mode = st.radio(
    "AIスコア表示モード",
    ["🎯 的中重視モード（3着内確率）", "💰 回収率重視モード（期待値）"],
    horizontal=True
)

# 仮のデータ（次のステップで本物の出馬表データとAIに置き換えます）
data = [
    {"馬番": 1, "馬名": "ヘデントール", "性齢": "牡5", "騎手": "T.マーカンド", "オッズ": 11.7, "的中スコア": 82, "回収スコア": 118},
    {"馬番": 2, "馬名": "コスモキュランダ", "性齢": "牡5", "騎手": "丹内祐次", "オッズ": 74.1, "的中スコア": 45, "回収スコア": 135},
    {"馬番": 3, "馬名": "メイショウタバル", "性齢": "牡5", "騎手": "武豊", "オッズ": 12.4, "的中スコア": 78, "回収スコア": 105},
    {"馬番": 4, "馬名": "クロワデュノール", "性齢": "牡4", "騎手": "C.デムーロ", "オッズ": 6.5, "的中スコア": 91, "回収スコア": 98},
]
df = pd.DataFrame(data)

# モードに応じてスコアと印を計算
if "的中" in mode:
    df["表示スコア"] = df["的中スコア"]
else:
    df["表示スコア"] = df["回収スコア"]

df = df.sort_values("表示スコア", ascending=False).reset_index(drop=True)
marks = ["◎", "○", "▲", "△"]
df["印"] = [marks[i] if i < len(marks) else "" for i in range(len(df))]

# 3. netkeiba風のタブ切り替え
tab1, tab2, tab3 = st.tabs(["📋 出馬表・AIスコア", "🐎 馬別詳細", "📊 データ分析"])

with tab1:
    show_df = df[["印", "馬番", "馬名", "騎手", "オッズ", "表示スコア"]]
    st.dataframe(show_df, use_container_width=True, hide_index=True)

with tab2:
    selected_horse = st.selectbox("詳細を見る馬を選択", df["馬名"])
    horse_info = df[df["馬名"] == selected_horse].iloc[0]
    st.write(f"**{horse_info['馬名']}**（{horse_info['性齢']} / 騎手：{horse_info['騎手']}）")
    st.info("ここに今後、過去5走の成績やAIが高評価した根拠データを表示します。")

with tab3:
    st.write("ここに今後、コース傾向や枠順データを表示します。")
