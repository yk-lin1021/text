import streamlit as st
import geopandas as gpd
import pandas as pd
from datetime import datetime
import pytz
import os

# 檔案路徑，用於儲存與讀取用戶回饋
feedback_file = "feedback_data.csv"

# 讀取 GeoJSON 檔案
file_url = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"
toilets_gdf = gpd.read_file(file_url)

# 讀取或初始化回饋資料
if os.path.exists(feedback_file):
    feedback_data = pd.read_csv(feedback_file)
else:
    feedback_data = pd.DataFrame(columns=["行政區", "公廁類別", "公廁名稱", "評分", "回饋時間"])

# 提取行政區與公廁類別列表
district_list = sorted(toilets_gdf["行政區"].unique())
category_list = sorted(toilets_gdf["公廁類別"].unique())

st.title("廁所回饋系統")

# 行政區選擇
selected_district = st.selectbox("請選擇行政區", district_list)

# 篩選該行政區的公廁類別
filtered_by_district = toilets_gdf[toilets_gdf["行政區"] == selected_district]
district_categories = sorted(filtered_by_district["公廁類別"].unique())
selected_category = st.selectbox("請選擇公廁類別", district_categories)

# 篩選該行政區和公廁類別的廁所
filtered_toilets = filtered_by_district[filtered_by_district["公廁類別"] == selected_category]
toilet_list = filtered_toilets["公廁名稱"].tolist()

# 公廁選擇
toilet_choice = st.selectbox("請選擇公廁", toilet_list)

# 評分輸入
rating = st.slider("請給予評分 (1-5)", 1, 5, 3)

# 提交按鈕
if st.button("提交回饋"):
    # 取得當前時間並轉換為 GMT+8
    taipei_tz = pytz.timezone("Asia/Taipei")
    current_time = datetime.now(taipei_tz).strftime("%Y-%m-%d %H:%M:%S")

    # 新的回饋資料
    new_feedback = pd.DataFrame({
        "行政區": [selected_district],
        "公廁類別": [selected_category],
        "公廁名稱": [toilet_choice],
        "評分": [rating],
        "回饋時間": [current_time]
    })

    # 更新回饋資料並儲存到檔案
    feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)
    feedback_data.to_csv(feedback_file, index=False)

    # 上傳更新的回饋資料至 GitHub（手動執行
