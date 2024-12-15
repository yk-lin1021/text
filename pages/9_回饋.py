import streamlit as st
import geopandas as gpd
import pandas as pd

# 讀取 GeoJSON 檔案
file_url = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"
toilets_gdf = gpd.read_file(file_url)

# 假設 GeoJSON 包含 '行政區', '公廁名稱', '公廁類別' 欄位
if "行政區" not in toilets_gdf.columns or "公廁名稱" not in toilets_gdf.columns or "公廁類別" not in toilets_gdf.columns:
    st.error("GeoJSON 檔案缺少必要的 '行政區', '公廁名稱' 或 '公廁類別' 欄位，請確認檔案格式。")
else:
    # 初始化回饋資料
    if "feedback_data" not in st.session_state:
        st.session_state.feedback_data = pd.DataFrame(columns=["行政區", "公廁類別", "公廁名稱", "評分", "回饋時間"])

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
        # 儲存回饋資料
        new_feedback = pd.DataFrame({
            "行政區": [selected_district],
            "公廁類別": [selected_category],
            "公廁名稱": [toilet_choice],
            "評分": [rating],
            "回饋時間": [pd.Timestamp.now()]
        })

        # 使用 pd.concat() 來合併新資料
        st.session_state.feedback_data = pd.concat([st.session_state.feedback_data, new_feedback], ignore_index=True)
        st.success("回饋已提交，謝謝您的參與！")

    # 顯示回饋表單
    st.subheader("所有用戶回饋")
    st.dataframe(st.session_state.feedback_data)

