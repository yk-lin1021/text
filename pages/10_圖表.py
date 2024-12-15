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
st.title("公廁類別與級數分佈")
gdf = load_data(filepath)

# 資料處理
# 假設有「公廁類別」和「級數」兩個欄位
if '公廁類別' in gdf.columns and '級數' in gdf.columns:
    # 統計數據
    grouped_data = gdf.groupby(['公廁類別', '級數']).size().reset_index(name='數量')

    # 確保級數按正確的順序排列
    ordered_levels = ["特優級", "優等級", "普通級", "改善級"]
    grouped_data['級數'] = pd.Categorical(grouped_data['級數'], categories=ordered_levels, ordered=True)

    # 繪製圖表
    fig = px.bar(
        grouped_data,
        x="公廁類別",
        y="數量",
        color="級數",
        title="公廁類別與級數分佈",
        labels={"公廁類別": "公廁類別", "數量": "數量", "級數": "級數"},
        barmode="group",
    )

    # 顯示圖表
    st.plotly_chart(fig)
else:
    st.error("資料中缺少必要的欄位：'公廁類別' 或 '級數'")
