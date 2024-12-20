import streamlit as st
import requests
import os

# 從環境變數中讀取 API 密鑰
api_key = os.getenv("API_KEY")  # 確保環境變數中有設置 API_KEY

# 如果未設置環境變數，顯示錯誤消息
if not api_key:
    st.error("API 密鑰未設定！請設定環境變數 API_KEY。")
else:
    # Streamlit 標題
    st.title("地址轉換為座標")

    # 輸入框
    address = st.text_input("請輸入地址或地點名稱：")

    # 當按下按鈕時，發送請求
    if st.button("查詢座標"):
        if address:
            # OpenCage Geocoder API 的 URL
            url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}&language=zh-TW'
            
            # 發送請求
            response = requests.get(url)

            # 檢查是否成功
            if response.status_code == 200:
                data = response.json()
                
                # 檢查是否找到結果
                if data['results']:
                    # 獲取經緯度
                    lat = data['results'][0]['geometry']['lat']
                    lon = data['results'][0]['geometry']['lng']
                    st.write(f"地址: {address} 的座標是：({lat}, {lon})")
                else:
                    st.write("未找到該地址的結果。")
            else:
                st.write(f"錯誤: {response.status_code}")
        else:
            st.write("請輸入一個地址。")
