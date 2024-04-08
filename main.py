import streamlit as st
import requests
import json
import folium
from streamlit_folium import folium_static

def get_bus_stops():
    # OpenStreetMap Overpass API를 사용하여 버스 정류장 정보를 가져오는 함수
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
        [out:json];
        node["highway"="bus_stop"](around:1000, 37.495916,127.124865);
        out;
        """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

def get_bus_locations(api_key, bus_route_id):
    # 서울시 버스 실시간 위치 정보를 가져오는 함수
    url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid"
    params = {
        "ServiceKey": api_key,
        "busRouteId": bus_route_id,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 오류를 발생시킴
        data = response.json()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP 오류 발생: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        st.error(f"연결 오류 발생: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        st.error(f"시간 초과: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        st.error(f"요청 예외: {err}")
        return None
    except json.decoder.JSONDecodeError as json_err:
        st.error(f"JSON 디코딩 오류: {json_err}")
        return None
    
    return data

def main():
    st.title('버스 이동 정보 지도')

    # 버스 정류장 정보를 가져와 지도 위에 표시
    bus_stops_data = get_bus_stops()
    map_center = [37.495916, 127.124865]
    m = folium.Map(location=map_center, zoom_start=20)

    for stop in bus_stops_data['elements']:
        lat = stop['lat']
        lon = stop['lon']
        folium.Marker([lat, lon], popup='Bus Stop').add_to(m)

    # 실시간으로 버스 위치를 가져와 지도에 표시
    api_key = "PVlQlhVqCM51twmt0Adp4f3LjZLgbpOyYhUbDqt%2FLGW0xf0%2FvjPkfRAN8k6BWndKMws45AtjZBMuFbOn37HRxg%3D%3D"
    bus_route_id = "315"
    bus_locations_data = get_bus_locations(api_key, bus_route_id)
    if bus_locations_
