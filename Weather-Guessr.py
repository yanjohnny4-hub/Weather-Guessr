import streamlit as st
import pandas as pd
import requests
import random
from datetime import date,timedelta

# INITIALIZATIONS
cities = [
    # Europe
    ('Paris', 'FR'),
    ('Moscow', 'RU'),
    ('London', 'GB'),
    ('Barcelona', 'ES'),
    ('Rome', 'IT'),
    ('Berlin', 'DE'),
    ('Amsterdam', 'NL'),
    ('Madrid', 'ES'),
    ('Lisbon', 'PT'),
    ('Vienna', 'AT'),
    ('Prague', 'CZ'),
    ('Stockholm', 'SE'),
    ('Oslo', 'NO'),
    ('Athens', 'GR'),
    ('Dublin', 'IE'),

    # North America
    ('Atlanta', 'US'),
    ('Seattle', 'US'),
    ('New York', 'US'),
    ('Los Angeles', 'US'),
    ('Toronto', 'CA'),
    ('Vancouver', 'CA'),
    ('Mexico City', 'MX'),
    ('Miami', 'US'),
    ('Chicago', 'US'),
    ('Montreal', 'CA'),
    ('Havana', 'CU'),
    ('Panama City', 'PA'),

    # South America
    ('São Paulo', 'BR'),
    ('Buenos Aires', 'AR'),
    ('Lima', 'PE'),
    ('Bogotá', 'CO'),
    ('Santiago', 'CL'),
    ('Quito', 'EC'),
    ('Montevideo', 'UY'),

    # Asia
    ('Beijing', 'CN'),
    ('Tokyo', 'JP'),
    ('Kyoto', 'JP'),
    ('Seoul', 'KR'),
    ('Singapore', 'SG'),
    ('Hong Kong', 'HK'),
    ('Mumbai', 'IN'),
    ('Delhi', 'IN'),
    ('Dubai', 'AE'),
    ('Bangkok', 'TH'),
    ('Jakarta', 'ID'),
    ('Manila', 'PH'),
    ('Hanoi', 'VN'),
    ('Kathmandu', 'NP'),
    ('Istanbul', 'TR'),

    # Africa
    ('Cairo', 'EG'),
    ('Cape Town', 'ZA'),
    ('Nairobi', 'KE'),
    ('Lagos', 'NG'),
    ('Casablanca', 'MA'),

    # Oceania
    ('Sydney', 'AU'),
    ('Melbourne', 'AU'),
    ('Auckland', 'NZ'),
    ('Perth', 'AU'),
]

if 'city' not in st.session_state:
    st.session_state.city, st.session_state.code = random.choice(cities)
if 'player_choices' not in st.session_state:
    st.session_state.player_choices = [x[0] for x in cities]
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num_days' not in st.session_state:
    st.session_state.num_days = 7

api_key = st.secrets["API_KEY"]

def get_weather(city_name, country_code):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_code}&cnt=14&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    return data

data = get_weather(st.session_state.city, st.session_state.code)
temp = data['list'][0]['main']['temp']
feels_like = data['list'][0]['main']['feels_like']
weather, desc = data['list'][0]['weather'][0]['main'], data['list'][1]['weather'][0]['description']
pressure = data['list'][0]['main']['pressure']
humidity = data['list'][0]['main']['humidity']
sea, ground = data['list'][0]['main']['sea_level'], data['list'][0]['main']['grnd_level']
lon, lat = data['city']['coord']['lon'], data['city']['coord']['lat']

forecast = []
dates = []
for i, info in enumerate(data['list']):
    forecast.append(info['main']['temp'])
    d = date.today() + timedelta(days=i)
    dates.append(d.strftime('%d %b %a'))
df = pd.DataFrame({'Temperature': forecast}, index=dates)
df.index.name = 'Day'

# PAGE CONFIGURATION
st.title('Weather-Guessr')
st.subheader('Welcome to Weather-Guessr! Try to guess the city based on its weather data!', divider='red')

col1, col2 = st.columns([0.5,1])

with col2: # Centers title and header
    st.header(f'{temp}°')
    st.subheader(f'Feels like {feels_like}°')
    st.image(f'https://openweathermap.org/img/wn/{data["list"][0]["weather"][0]["icon"]}@2x.png', width=200)
    st.subheader(f'{desc.capitalize()}')

st.slider('Select Number of Days to Display', 
          min_value=1, max_value=len(dates), 
          step=1, 
          key='num_days',
          value=st.session_state.num_days)
display_df = df.iloc[:st.session_state.num_days]
st.line_chart(display_df, x_label='Day', y_label='Temperature (°F)')

category, info = st.columns(2, border=True)
with category:
    st.header('Pressure')
    st.header('Humidity')
    st.header('Sea Level')
    st.header('Ground Level')
    st.header('Longitude')
    st.header('Latitude')
with info:
    st.header(f'{pressure} hPa')
    st.header(f'{humidity}%')
    st.header(sea)
    st.header(ground)
    st.header(lon)
    st.header(lat)

choice = st.selectbox('Choose a City', st.session_state.player_choices, key='choice', index=None)
if st.button('Submit'):
    if choice == st.session_state.city:
        st.success(f'Correct! The city was {st.session_state.city}!\nStarting new game...', icon='✅')
        st.session_state.city, st.session_state.code = random.choice(cities)
        st.session_state.player_choices = [x[0] for x in cities]
        st.session_state.score += 1
        st.session_state.attempts = 0
        data = get_weather(st.session_state.city, st.session_state.code)
    else:
        try:
            st.session_state.player_choices.remove(choice)
            st.error('Not quite...')
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.info(f'Hint: {st.session_state.code}')
        except:
            st.warning('Please select a valid city from the dropdown menu.')

st.header(f'Score: {st.session_state.score}')
