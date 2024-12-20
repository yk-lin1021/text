import os
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
from folium.plugins import HeatMap
import pandas as pd
from github import Github
import io
import requests

# 從 Streamlit Secrets 中讀取 API 金鑰
api_key = st.secrets["general"]["api_key"]

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "yk-lin1021/113-1gis"  # 替換為您的儲存庫名稱
FEEDBACK_FILE_PATH = "feedback_data.csv"  # 儲存回饋資料的檔案路徑

# 初始化 GitHub API
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 從 GitHub 載入回饋資料
try:
    file_content = repo.get_contents(FEEDBACK_FILE_PATH)
    feedback_data = pd.read_csv(io.StringIO(file_content.decoded_content.decode('utf-8')))
except Exception as e:
    st.warning(f"無法讀取回饋資料：{e}")
    feedback_data = pd.DataFrame(columns=["行政區", "公廁類別", "公廁名稱", "評分", "回饋時間"])

# 載入 GeoJSON 檔案
data = gpd.read_file("https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson")

# 載入回饋資料
feedback_file = "feedback_data.csv"
if os.path.exists(feedback_file):
    feedback_data = pd.read_csv(feedback_file)
else:
    feedback_data = pd.DataFrame(columns=["行政區", "公廁類別", "公廁名稱", "評分", "回饋時間"])

# 建立 Streamlit 應用程式
st.title("公廁互動地圖")

# 在地圖上方新增篩選條件
st.subheader("篩選條件")

# 提供多選選項篩選行政區
districts = ['全選'] + list(data['行政區'].unique())
selected_districts = st.multiselect("選擇行政區", options=districts, default=['全選'])

# 提供多選選項篩選公廁類別
toilet_types = ['全選'] + list(data['公廁類別'].unique())
selected_types = st.multiselect("選擇公廁類別", options=toilet_types, default=['全選'])

# 勾選選項以顯示附加資訊
show_accessible = st.checkbox("無障礙廁座", value=True)
show_parent_child = st.checkbox("親子廁座", value=True)

# 用戶輸入地址
user_address = st.text_input("請輸入地址以顯示在地圖上")

# 地理編碼：將地址轉換為經緯度
def geocode_address(address):
    # OpenCage API 連結
    url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}&language=zh-TW'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
    return None, None

# 如果用戶輸入地址，將其顯示在地圖上
if user_address:
    lat, lon = geocode_address(user_address)
    if lat and lon:
        st.success(f"地址 '{user_address}' 的位置已顯示在地圖上")
    else:
        st.warning(f"無法找到地址 '{user_address}' 的位置")
else:
    lat, lon = 25.033, 121.565  # 預設地圖中心（台北市）

# 根據選擇的公廁類別篩選資料
if '全選' not in selected_types:
    filtered_data = data[data['公廁類別'].isin(selected_types)]
else:
    filtered_data = data.copy()

# 根據選擇的行政區進一步篩選資料
if '全選' not in selected_districts:
    filtered_data = filtered_data[filtered_data['行政區'].isin(selected_districts)]

# 根據勾選框進一步篩選資料
if show_accessible:
    filtered_data = filtered_data[filtered_data['無障礙廁座數'] > 0]
if show_parent_child:
    filtered_data = filtered_data[filtered_data['親子廁座數'] > 0]

# 計算每個公廁的平均評分
def calculate_average_rating(toilet_name):
    feedback = feedback_data[feedback_data['公廁名稱'] == toilet_name]
    if not feedback.empty:
        return feedback['評分'].mean()
    else:
        return None

# 將平均評分新增至篩選後的資料
filtered_data['平均評分'] = filtered_data['公廁名稱'].apply(calculate_average_rating)

# 初始化地圖
m = leafmap.Map(center=(lat, lon), zoom=12)

# 如果有用戶地址，添加標註
if user_address and lat and lon:
    m.add_marker(location=(lat, lon), popup=f"<b>地址:</b> {user_address}", icon=leafmap.folium.Icon(color='green'))

# 建立公廁標註圖層
marker_layer = leafmap.folium.FeatureGroup(name="公廁標註")

# 將篩選後的資料新增至標註圖層
for _, row in filtered_data.iterrows():
    toilet_name = row['公廁名稱']
    feedback = feedback_data[feedback_data['公廁名稱'] == toilet_name]

    # 如果沒有回饋資料，預設回饋訊息
    feedback_message = "<b>評分:</b> 尚無回饋"

    # 如果有回饋資料，計算並顯示平均評分
    if not feedback.empty:
        average_rating = feedback['評分'].mean()  # 計算平均評分
        feedback_message = f"<b>評分:</b> {average_rating:.2f} (來自 {len(feedback)} 個回饋)"

    popup_info = (
        f"<b>公廁名稱:</b> {row['公廁名稱']}<br>"
        f"<b>地址:</b> {row['公廁地址']}<br>"
        f"<b>管理單位:</b> {row['管理單位']}<br>"
        f"<b>座數:</b> {row['座數']}<br>"
        f"<b>特優級:</b> {row['特優級']}<br>"
        f"<b>優等級:</b> {row['優等級']}<br>"
        f"<b>普通級:</b> {row['普通級']}<br>"
        f"<b>改善級:</b> {row['改善級']}<br>"
        f"{feedback_message}<br>"# 加入回饋訊息
        f"<b>無障礙廁座數:</b> {row['無障礙廁座數']}<br>"
        f"<b>親子廁座數:</b> {row['親子廁座數']}<br>"
    )

    # 將標註新增至標註圖層
    marker_layer.add_child(
        leafmap.folium.Marker(
            location=(row['緯度'], row['經度']),
            tooltip=popup_info,
            icon=leafmap.folium.Icon(color='blue')
        )
    )

# 將標註圖層新增至地圖
m.add_child(marker_layer)

# 新增圖層控制以切換圖層
leafmap.folium.LayerControl().add_to(m)

# 在 Streamlit 中顯示地圖
m.to_streamlit(height=700)

# 在底部顯示篩選後的公廁資訊
st.subheader("選擇的公廁資訊")
if filtered_data.empty:
    st.write("沒有符合條件的公廁。")
else:
    st.dataframe(filtered_data[['公廁名稱', '公廁地址', '管理單位', '平均評分', '座數', '特優級', '優等級', '普通級', '改善級', '無障礙廁座數', '親子廁座數']])
