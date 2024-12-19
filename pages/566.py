import streamlit as st
import leafmap.foliumap as leafmap
import geocoder

def main():
    st.title("地址轉換為地圖標記")
    
    # 使用者輸入地址
    city = st.text_input("請輸入地址:", "")
    
    if st.button("取得地圖"):
        if city:
            # 取得經緯度
            city_gps = geocoder.osm(city).latlng
            
            if city_gps:
                st.write(f"地址: {city}")
                st.write(f"經緯度座標: {city_gps}")
                
                # 使用 leafmap 繪製地圖
                m = leafmap.Map(center=city_gps, zoom=16)
                m.add_marker(location=city_gps, popup=city)
                
                # 在 Streamlit 中顯示地圖
                m.to_streamlit(height=500)
            else:
                st.error("無法取得地址的經緯度，請確認地址是否正確。")
        else:
            st.warning("請輸入地址。")

if __name__ == "__main__":
    main()
