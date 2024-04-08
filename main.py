import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

def get_bus_stops():
    # OpenStreetMap Overpass API를 사용하여 버스 정류장 정보를 가져오는 함수
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
        [out:json];
        node["highway"="bus_stop"](around:500, 37.404988,127.106007);
        out;
        """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

def get_bus_locations(api_key, bus_route_id):
    # 서울시 버스 실시간 위치 정보를 가져오는 함수
    url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt"
    params = {
        "ServiceKey": api_key,
        "busRouteId": bus_route_id,
        "startOrd": 1,
        "endOrd": 13
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def main():
    st.title('버스 이동 정보 지도')

    # 버스 정류장 정보를 가져와 지도 위에 표시
    bus_stops_data = get_bus_stops()
    map_center = [37.403051, 127.107626]
    m = folium.Map(location=map_center, zoom_start=20)

    for stop in bus_stops_data['elements']:
        lat = stop['lat']
        lon = stop['lon']
        folium.Marker([lat, lon], popup='Bus Stop').add_to(m)

    # 실시간으로 버스 위치를 가져와 지도에 표시
    api_key = "PVlQlhVqCM51twmt0Adp4f3LjZLgbpOyYhUbDqt%2FLGW0xf0%2FvjPkfRAN8k6BWndKMws45AtjZBMuFbOn37HRxg%3D%3D"
    bus_route_id = "100100118"  # 관심 있는 버스 노선 ID로 변경해야 합니다
    bus_locations_data = get_bus_locations(api_key, bus_route_id)
    for bus_location in bus_locations_data['ServiceResult']['msgBody']['itemList']:
        lat = float(bus_location['gpsY'])
        lon = float(bus_location['gpsX'])
        folium.Marker([lat, lon], popup='Bus').add_to(m)

    folium_static(m)

if __name__ == "__main__":
    main()
