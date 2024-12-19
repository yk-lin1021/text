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
1. **公廁資訊地圖**可以將公廁資訊呈現再地圖上並讓用戶挑選自己想去的公廁並看到其資訊\n
2. **用戶回饋**可以讓用戶回饋公廁使用體驗\n
3. **公廁分析圖**可以呈現台北市公廁類別和用戶即時回饋分數、公廁等級關係圖表
"""

st.markdown(markdown2)

