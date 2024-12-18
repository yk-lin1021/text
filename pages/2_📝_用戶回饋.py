import streamlit as st
import geopandas as gpd
import pandas as pd
from datetime import datetime
import pytz
import os
from github import Github  # PyGithub 模組

# GitHub 設定
GITHUB_TOKEN = st.secrets("GITHUB_TOKEN")  # 從環境變數讀取
REPO_NAME = 'yk-lin1021/113-1gis'
FILE_PATH = 'feedback_data.csv'

# 初始化 GitHub API
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 檔案路徑，用於儲存與讀取用戶回饋
feedback_file = "feedback_data.csv"

# 讀取 GeoJSON 檔案
file_url = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"
toilets_gdf = gpd.read_file(file_url)

# 確保 GeoJSON 包含必要欄位
if "行政區" not in toilets_gdf.columns or "公廁名稱" not in toilets_gdf.columns or "公廁類別" not in toilets_gdf.columns:
    st.error("GeoJSON 檔案缺少必要的 '行政區', '公廁名稱' 或 '公廁類別' 欄位，請確認檔案格式。")
else:
    # 讀取或初始化回饋資料
    if os.path.exists(feedback_file):
        feedback_data = pd.read_csv(feedback_file)
    else:
        feedback_data = pd.DataFrame(columns=["行政區", "公廁類別", "公廁名稱", "評分", "回饋時間"])

    # 提取行政區與公廁類別列表
    district_list = sorted(toilets_gdf["行政區"].unique())
    category_list = sorted(toilets_gdf["公廁類別"].unique())

    st.title("公廁回饋系統")

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
    rating = st.slider("請給予評分 (1-5，5為體驗較好)", 1, 5, 3)

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

        # 更新本地回饋資料
        feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)
        feedback_data.to_csv(feedback_file, index=False)
        st.success("回饋已提交，謝謝您的參與！")

        # 更新至 GitHub
        try:
            # 轉換為 CSV 格式
            updated_csv = feedback_data.to_csv(index=False)

            # 取得原文件 SHA 值
            file = repo.get_contents(FILE_PATH)
            commit_message = "更新回饋資料"
            repo.update_file(
                path=FILE_PATH,
                message=commit_message,
                content=updated_csv,
                sha=file.sha  # 必須提供文件的 SHA 值
            )
            st.success("回饋資料已成功同步到 GitHub！")
        except Exception as e:
            st.error(f"無法更新 GitHub 上的 CSV 文件: {e}")

    # 顯示所有用戶回饋
    st.subheader("所有用戶回饋")
    st.dataframe(feedback_data)
