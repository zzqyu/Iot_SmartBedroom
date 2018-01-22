import requests

# https://developers.skplanetx.com/develop/
# 앱 등록 및 키 발급
appKey = "89fbca5e-e9a8-383f-96b3-4f0f0ede45d0"


# 현재 날씨(시간별)
url_hourly = "http://apis.skplanetx.com/weather/current/hourly"

headers = {'Content-Type': 'application/json; charset=utf-8',
           'appKey': appKey}

weather_list=[]
weather_info=[]

#현재 날씨(시간별)
def hourly(weather):
    global weather_list
    # print(weather)
    # 상대 습도
    humidity     = weather['humidity']

    # 발표 시간
    timeRelease  = weather['timeRelease']

    # 격자정보
    # 위도
    grid_latitude  = weather['grid']['latitude']
    # 경도
    grid_longitude = weather['grid']['longitude']
    # 시, 도
    grid_city      = weather['grid']['city']
    # 시, 군, 구
    grid_county    = weather['grid']['county']
    # 읍, 면, 동
    grid_village   = weather['grid']['village']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']

    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']
    '''str = '시간별 온도 ' + temperature_tc + ', 최고 ' + temperature_tmax + ', 최저 ' + temperature_tmin + ', 하늘 ' + sky_name + ', 습도' + humidity'''
    str = '시간별 온도 ' + temperature_tc + ', 하늘 ' + sky_name
    print(str)
    weather_list.append(sky_name)
    weather_list.append(temperature_tc)
    '''print(weather_list)'''


## 값을 전달하기 위한 함수 설정
def print_info():
    print("info : ", weather_list)
    return weather_list

def requestCurrentWeather(city, county, village, isHourly = True):
    params = { "version": "1",
                "city": city,
                "county": county,
                "village": village }
 
    response = requests.get(url_hourly, params=params, headers=headers)

    if response.status_code == 200:
        #json을 딕셔너리로 변경
        response_body = response.json()

        #날씨 정보
        try:
            weather_data = response_body['weather']['hourly'][0]
            hourly(weather_data)
            
        
        except requests.exceptions.RequestException as e:
            print('Connection error: '+str(e))
    else:
        pass
        #에러


#if __name__ == '__main__':
    #city = '경기'  #'도' 나 '시'는 빼고 넣는다.
    #county = '김포시' #시 or 구
    #village = '장기동' #동
    # 시간별 (기본)
requestCurrentWeather('서울','노원구','중계동')
weather_info = print_info()
