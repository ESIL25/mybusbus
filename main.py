import streamlit as st
import requests
import folium

def get_bus_stops():
    # OpenStreetMap Overpass API를 사용하여 버스 정류장 정보를 가져오는 함수
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
        [out:json];
        node["highway"="bus_stop"](around:1000,37.5665,126.9780);
        out;
        """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

def main():
    st.title('버스 이동 정보 지도')

    # 버스 정류장 정보를 가져와 지도 위에 표시
    bus_stops_data = get_bus_stops()
    map_center = [37.5665, 126.9780]
    m = folium.Map(location=map_center, zoom_start=15)

    for stop in bus_stops_data['elements']:
        lat = stop['lat']
        lon = stop['lon']
        folium.Marker([lat, lon], popup='Bus Stop').add_to(m)

    folium_static(m)

if __name__ == "__main__":
    main()