import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import json

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
show_accessible = st.checkbox("顯示無障礙廁座數", value=True)
show_parent_child = st.checkbox("顯示親子廁座數", value=True)

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

# Initialize user location variables
user_lat = None
user_lon = None

# Get user location manually
st.write("\u26A0 若要顯示您的位置，請點擊下方按鈕允許存取您的定位資訊。")
if st.button("取得我的位置"):
    location_script = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = {"lat": position.coords.latitude, "lon": position.coords.longitude};
            const el = document.getElementById('location-data');
            el.innerText = JSON.stringify(coords);
        },
        (error) => {
            const el = document.getElementById('location-data');
            el.innerText = JSON.stringify({"error": error.message});
        }
    );
    </script>
    <div id="location-data" style="display: none;"></div>
    """
    user_location = st.components.v1.html(location_script, height=0)

    if user_location:
        try:
            coords = json.loads(user_location)
            if "lat" in coords and "lon" in coords:
                user_lat = coords["lat"]
                user_lon = coords["lon"]
            elif "error" in coords:
                st.error(f"定位失敗: {coords['error']}")
        except json.JSONDecodeError:
            st.error("定位資料解析失敗，請重試。")

# Initialize the map
m = leafmap.Map(center=(25.033, 121.565), zoom=12)

# Add user location marker if available
if user_lat and user_lon:
    m.add_marker(location=(user_lat, user_lon), tooltip="您的位置", icon="blue")

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

# Display the map
m.to_streamlit(height=700)
