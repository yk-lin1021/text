import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# Load the geojson file
data = gpd.read_file("https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson")

# Streamlit App
st.title("公廁互動地圖")

# Add filter options above the map
st.subheader("篩選條件")

# Selection options for filtering
toilet_types = ['全選'] + list(data['公廁類別'].unique())
selected_type = st.selectbox("選擇公廁類別", options=toilet_types, index=0)

# Checkbox options for additional information
show_accessible = st.checkbox("無障礙廁座", value=True)
show_parent_child = st.checkbox("親子廁座", value=True)

# Filter data based on selection
if selected_type == '全選':
    filtered_data = data.copy()
else:
    filtered_data = data[data['公廁類別'] == selected_type]

# Further filter data based on checkboxes
if show_accessible:
    filtered_data = filtered_data[filtered_data['無障礙廁座數'] > 0]
if show_parent_child:
    filtered_data = filtered_data[filtered_data['親子廁座數'] > 0]

# Initialize the map
m = leafmap.Map(center=(25.033, 121.565), zoom=12)

# Add filtered data to the map
for _, row in filtered_data.iterrows():
    popup_info = (
        f"<b>公廁名稱:</b> {row['公廁名稱']}<br>"
        f"<b>地址:</b> {row['公廁地址']}<br>"
        f"<b>管理單位:</b> {row['管理單位']}<br>"
        f"<b>座數:</b> {row['座數']}<br>"
        f"<b>特優級:</b> {row['特優級']}<br>"
        f"<b>優等級:</b> {row['優等級']}<br>"
        f"<b>普通級:</b> {row['普通級']}<br>"
        f"<b>改善級:</b> {row['改善級']}<br>"
    )

    if show_accessible:
        popup_info += f"<b>無障礙廁座數:</b> {row['無障礙廁座數']}<br>"
    if show_parent_child:
        popup_info += f"<b>親子廁座數:</b> {row['親子廁座數']}<br>"

    m.add_marker(location=(row['緯度'], row['經度']), tooltip=popup_info, popup_max_width=300)

# Get user location
def get_user_location():
    st.write("請允許瀏覽器取得您的位置以顯示在地圖上。")
    user_lat = st.number_input("輸入您的緯度：", value=25.033)
    user_lon = st.number_input("輸入您的經度：", value=121.565)
    return user_lat, user_lon

user_lat, user_lon = get_user_location()

# Add user location to the map
if user_lat and user_lon:
    m.add_marker(location=(user_lat, user_lon), tooltip="您的位置", popup="<b>這是您的位置</b>", icon_color="blue")

# Display the map
m.to_streamlit(height=700)
