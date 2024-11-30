import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("石門水庫集水區雨量資料")

with st.expander("See source code"):
    with st.echo():

        m = leafmap.Map(center=[40, -100], zoom=6)
        cities = "https://github.com/yk-lin1021/113-1gis/raw/refs/heads/main/rain.csv"
        regions = "https://raw.githubusercontent.com/yk-lin1021/113-1gis/refs/heads/main/1130.geojson"

        m.add_geojson(regions, layer_name="石門水庫集水區")
        m.add_points_from_xy(
            cities,
            x="lon",
            y="lat",
            icon_names=["2023", "2022", "2021", "單位"],
            spin=True,
            add_legend=True,
        )

m.to_streamlit(height=700)

csv_file = st.file_uploader("https://github.com/yk-lin1021/113-1gis/raw/refs/heads/main/rain.csv", type=["csv"])
df = pd.read_csv(csv_file)
st.dataframe(df)
