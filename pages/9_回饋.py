import streamlit as st
import geopandas as gpd
import pandas as pd

# 讀取 GeoJSON 檔案
file_path = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"
toilets_gdf = gpd.read_file(file_path)

# 假設 GeoJSON 包含地址 (address) 和廁所名稱 (name) 欄位
if "address" not in toilets_gdf.columns or "name" not in toilets_gdf.columns:
    st.error("GeoJSON 檔案缺少必要的 'address' 或 'name' 欄位，請確認檔案格式。")
else:
    # 提取行政區資料
    def extract_district(address):
        # 假設地址格式為 "台北市中正區某某路" 或 "中正區某某路"
        import re
        match = re.search(r"[縣市](\S+?區)", address)
        return match.group(1) if match else "未知行政區"

    toilets_gdf["district"] = toilets_gdf["address"].apply(extract_district)

    # 初始化回饋資料
    if "feedback_data" not in st.session_state:
        st.session_state.feedback_data = pd.DataFrame(columns=["行政區", "廁所名稱", "評分", "回饋時間"])

    # 提取行政區列表
    district_list = sorted(toilets_gdf["district"].unique())

    st.title("廁所回饋系統")

    # 行政區選擇
    selected_district = st.selectbox("請選擇行政區", district_list)

    # 篩選該行政區的廁所
    filtered_toilets = toilets_gdf[toilets_gdf["district"] == selected_district]
    toilet_list = filtered_toilets["name"].tolist()

    # 廁所選擇
    toilet_choice = st.selectbox("請選擇廁所", toilet_list)

    # 評分輸入
    rating = st.slider("請給予評分 (1-5)", 1, 5, 3)

    # 提交按鈕
    if st.button("提交回饋"):
        # 儲存回饋資料
        new_feedback = {
            "行政區": selected_district,
            "廁所名稱": toilet_choice,
            "評分": rating,
            "回饋時間": pd.Timestamp.now()
        }
        st.session_state.feedback_data = st.session_state.feedback_data.append(new_feedback, ignore_index=True)
        st.success("回饋已提交，謝謝您的參與！")

    # 顯示回饋表單
    st.subheader("所有用戶回饋")
    st.dataframe(st.session_state.feedback_data)
