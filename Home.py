import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")


# Customize page title
st.title("台北公廁資訊系統")

st.markdown(
    """
    113-1 地理資訊系統運用程式期末報告\n
    S1143037 林奕穀  S1143040 賈雅涵
    """
)

st.header("網站內容")

markdown2 = """
1. 可以呈現台北市公廁類別和廁所等級關係圖表\n
2. 可以將廁所資訊呈現再地圖上並讓用戶挑選自己想去的廁所並看到其資訊\n
3. 可以讓用戶回饋廁所使用體驗
"""

st.markdown(markdown2)

