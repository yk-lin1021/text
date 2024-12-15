import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# Load the geojson file
data = gpd.read_file("https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/%E5%BB%81%E6%89%80%E4%BD%8D%E7%BD%AE.geojson")

# Streamlit App
st.title("公廁互動地圖")

# Add filter options above the map
st.subheader("篩選條件")

# Multi-select options for filtering by public toilet category (公廁類別)
toilet_types = ['全選'] + list(data['公廁類別'].unique())
selected_types = st.multiselect("選擇公廁類別", options=toilet_types, default=['全選'])

# Multi-select options for filtering by administrative districts (行政區)
districts = ['全選'] + list(data['行政區'].unique())
selected_districts = st.multiselect("選擇行政區", options=districts, default=['全選'])

# Checkbox options for additional information
show_accessible = st.checkbox("顯示無障礙廁座", value=True)
show_parent_child = st.checkbox("顯示親子廁座", value=True)

# Filter data based on selected public toilet categories
if '全選' not in selected_types:
    filtered_data = data[data['公廁類別'].isin(selected_types)]
else:
    filtered_data = data.copy()

# Further filter data based on selected administrative districts
if '全選' not in selected_districts:
    filtered_data = filtered_data[filtered_data['行政區'].isin(selected_districts)]

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

# Display the map
m.to_streamlit(height=700)

# Show the filtered toilet information at the bottom
st.subheader("選擇的公廁資訊")
if filtered_data.empty:
    st.write("沒有符合條件的公廁。")
else:
    st.dataframe(filtered_data[['公廁名稱', '公廁地址', '管理單位', '座數', '特優級', '優等級', '普通級', '改善級', '無障礙廁座數', '親子廁座數']])

