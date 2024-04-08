import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# 버스 위치 정보를 가져오는 함수
def get_bus_locations(api_key, start_lat, start_lon, end_lat, end_lon):
    url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid"
    params = {
        "ServiceKey": api_key,
        "startLat": start_lat,
        "startLong": start_lon,
        "endLat": end_lat,
        "endLong": end_lon,
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

    return data

def main():
    st.title('간단한 출퇴근 지도')

    # 출발지와 도착지 위경도를 입력 받음
    start_lat, start_lon, end_lat, end_lon = st.columns(4)
    with start_lat:
        start_lat_val = st.number_input('출발지 위도', value=37.480621)
    with start_lon:
        start_lon_val = st.number_input('출발지 경도', value=127.059480)
    with end_lat:
        end_lat_val = st.number_input('도착지 위도', value=37.402056)
    with end_lon:
        end_lon_val = st.number_input('도착지 경도', value=127.108212)

    # 출발지와 도착지 위치를 스위치하여 변경
    if st.button('출발지와 도착지 위치 바꾸기'):
        start_lat_val, end_lat_val = end_lat_val, start_lat_val
        start_lon_val, end_lon_val = end_lon_val, start_lon_val

    # 출발지와 도착지를 연결하는 지도 표시
    m = folium.Map(location=[start_lat_val, start_lon_val], zoom_start=12)
    folium.Marker([start_lat_val, start_lon_val], popup='출발지').add_to(m)
    folium.Marker([end_lat_val, end_lon_val], popup='도착지').add_to(m)
    folium.PolyLine(locations=[[start_lat_val, start_lon_val], [end_lat_val, end_lon_val]], color='blue').add_to(m)

    # 실시간으로 버스 위치를 가져와 지도에 표시
    api_key = "PVlQlhVqCM51twmt0Adp4f3LjZLgbpOyYhUbDqt%2FLGW0xf0%2FvjPkfRAN8k6BWndKMws45AtjZBMuFbOn37HRxg%3D%3D"
    bus_locations_data = get_bus_locations(api_key, start_lat_val, start_lon_val, end_lat_val, end_lon_val)
    if bus_locations_data:
        for bus_location in bus_locations_data['ServiceResult']['msgBody']['itemList']:
            lat = float(bus_location['gpsY'])
            lon = float(bus_location['gpsX'])
            folium.Marker([lat, lon], popup='버스').add_to(m)

    folium_static(m)

if __name__ == "__main__":
    main()
