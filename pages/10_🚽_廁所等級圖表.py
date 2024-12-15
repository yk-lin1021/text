import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# 讀取 GeoJSON 資料
@st.cache_data
def load_data(filepath):
    gdf = gpd.read_file(filepath)
    return gdf

# 設定檔案路徑
filepath = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"

# 加載資料
st.title("公廁類別與等級分佈")
gdf = load_data(filepath)

# 資料處理
if '公廁類別' in gdf.columns and '特優級' in gdf.columns and '優等級' in gdf.columns and '普通級' in gdf.columns and '改善級' in gdf.columns:
    # 轉換為長格式
    level_columns = ['特優級', '優等級', '普通級', '改善級']
    melted_data = gdf[['公廁類別'] + level_columns].melt(id_vars='公廁類別', value_vars=level_columns, var_name='等級', value_name='數量')

    # 計算每個公廁類別的總數量
    total_per_category = melted_data.groupby('公廁類別')['數量'].sum().reset_index(name='總數量')

    # 將總數量併入 melted_data
    melted_data = melted_data.merge(total_per_category, on='公廁類別')

    # 計算比例
    melted_data['比例'] = melted_data['數量'] / melted_data['總數量']

    # 創建下拉選單讓使用者選擇公廁類別
    categories = melted_data['公廁類別'].unique()
    selected_category = st.selectbox("選擇公廁類別", categories)

    # 根據選擇的公廁類別繪製圓餅圖
    selected_data = melted_data[melted_data['公廁類別'] == selected_category]

    # 繪製圓餅圖
    fig2 = px.pie(
        selected_data,
        names="等級",
        values="比例",
        title=f"{selected_category} - 公廁等級比例",
        color="等級",
        hole=0.3,  # 可選：用來製作圓環圖
    )

    # 顯示圓餅圖
    st.plotly_chart(fig2)

    # 繪製長條圖（顯示所有類別的級數數量）
    fig1 = px.bar(
        melted_data,
        x="公廁類別",
        y="數量",
        color="級數",
        title="公廁類別與等級分佈",
        labels={"公廁類別": "公廁類別", "數量": "數量", "級數": "級數"},
        barmode="group",
    )

    # 顯示長條圖
    st.plotly_chart(fig1)

else:
    st.error("資料中缺少必要的欄位：'公廁類別' 或 '特優級', '優等級', '普通級', '改善級'")
