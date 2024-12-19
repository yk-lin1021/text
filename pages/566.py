import streamlit as st
import leafmap.foliumap as leafmap
from geopy.geocoders import Nominatim

# 創建地理編碼器
geolocator = Nominatim(user_agent="geoapiExercises")

# 在 Streamlit 上顯示標題
st.title("Address to Coordinates")

# 讓用戶輸入地址
address = st.text_input("Enter an address:")

if address:
    # 使用 geopy 進行地址轉換
    location = geolocator.geocode(address)
    
    if location:
        lat, lon = location.latitude, location.longitude
        
        # 顯示轉換後的座標
        st.write(f"Latitude: {lat}, Longitude: {lon}")
        
        # 創建地圖並顯示位置
        m = leafmap.Map(center=(lat, lon), zoom=12)
        m.add_marker(location=(lat, lon), popup=f"Location: {address}")
        m.to_streamlit()
    else:
        st.write("Address not found. Please try another one.")
