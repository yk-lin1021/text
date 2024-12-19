import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from github import Github
import os
from io import StringIO

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 從環境變數讀取
REPO_NAME = 'yk-lin1021/113-1gis'
FILE_PATH = 'feedback_data.csv'

# 讀取 GeoJSON 資料
@st.cache_data
def load_geojson(filepath):
    gdf = gpd.read_file(filepath)
    return gdf

# 從 GitHub 加載回饋資料
@st.cache_data
def load_feedback_from_github(token, repo_name, file_path):
    g = Github(token)
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    feedback_data = pd.read_csv(StringIO(file_content.decoded_content.decode()))
    return feedback_data

# 設定檔案路徑與初始化
geojson_path = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson"

# 標題
st.title("公廁分析：等級與用戶回饋")

# 快取清除按鈕
if st.button("清除快取並重新載入資料"):
    st.cache_data.clear()  # 清除所有快取
    st.success("快取已清除，請重新執行應用程式！")

# 加載 GeoJSON 資料
gdf = load_geojson(geojson_path)

# 加載 GitHub 的回饋資料
try:
    feedback_df = load_feedback_from_github(GITHUB_TOKEN, REPO_NAME, FILE_PATH)

    # 確保回饋資料中存在必要欄位
    if '公廁類別' in feedback_df.columns and '評分' in feedback_df.columns:
        # 計算每個公廁類別的平均評分
        avg_rating = feedback_df.groupby('公廁類別')['評分'].mean().reset_index()
        avg_rating = avg_rating.rename(columns={"公廁類別": "公廁類別", "評分": "平均評分"})
        st.subheader("用戶回饋平均評分")
        # 繪製平均評分的長條圖
        fig3 = px.bar(
            avg_rating,
            x="公廁類別",
            y="平均評分",
            title="公廁類別與平均評分",
            labels={"公廁類別": "公廁類別", "平均評分": "平均評分"},
            color="平均評分",
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig3)
    else:
        st.error("回饋資料缺少必要的欄位：'公廁類別' 或 '評分'")
except Exception as e:
    st.error(f"無法載入回饋資料：{str(e)}")

# 繼續原本的等級分佈分析
if '公廁類別' in gdf.columns and '特優級' in gdf.columns and '優等級' in gdf.columns and '普通級' in gdf.columns and '改善級' in gdf.columns:
    
    st.subheader("環保局-公廁設施環境衛生檢查評分")
    # 顯示內文
    st.markdown("""
    **特優級**：九十五分以上。  
    **優等級**：八十六分以上九十四分以下。  
    **普通級**：七十六分以上八十五分以下。  
    **改善級**：七十五分以下。  
    """)
    
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
        hole=0.3,
    )

    # 顯示圓餅圖
    st.plotly_chart(fig2)

    # 繪製長條圖（顯示所有類別的級數數量）
    fig1 = px.bar(
        melted_data,
        x="公廁類別",
        y="數量",
        color="等級",
        title="公廁類別與等級分佈",
        labels={"公廁類別": "公廁類別", "數量": "數量", "等級": "等級"},
        barmode="group",
    )
    
    # 顯示長條圖
    st.plotly_chart(fig1)
else:
    st.error("資料中缺少必要的欄位：'公廁類別' 或 '特優級', '優等級', '普通級', '改善級'")
