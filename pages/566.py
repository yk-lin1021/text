import streamlit as st
import leafmap.foliumap as leafmap
import geocoder  # 用來獲取用戶的 GPS 位置

# 取得用戶的 GPS 位置
g = geocoder.ip('me')
lat, lon = g.latlng

# 在 Streamlit 上顯示地圖
m = leafmap.Map(center=(lat, lon), zoom=12)

# 在地圖上標記用戶位置
m.add_marker(location=(lat, lon), popup="Your Location")

# 顯示地圖
st.title("Display User GPS Location")
st.write(f"User's Latitude: {lat}, Longitude: {lon}")
st.dataframe({"Latitude": [lat], "Longitude": [lon]})  # 顯示經緯度數據
m.to_streamlit()
