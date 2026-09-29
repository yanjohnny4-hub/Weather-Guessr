# Weather-Guessr
A GeoGuessr inspired web game where players identify cities around the world using real-time weather data.
## Overview
*Weather-Guessr* is a Python and Streamlit web application that challenges users to guess a city based solely on its current weather conditions and meteorological data.
The game retrieves live weather data through a REST API and presents players with multiple weather variables as clues. Players must use these clues to determine which city they believe the data belongs to.
### Features
* 60+ cities across 47 countries
* Real-time weather data
* 7 weather variables used as clues, including:
  * Temperature
  * Humidity
  * Atmospheric pressure
  * Sea level
  * Ground level
  * Longitude
  * Latitude
* Interactive weather visualizations
* Score counter for competitive gameplay 

## Installation
[Click here to play](https://weather-guessr-o9reqqt2se8rjvvb7mwrpf.streamlit.app/)

Alternatively:

Clone the repository:
```
git clone https://github.com/yanjohnny4-hub/Weather-Guessr.git
cd Weather-Guessr
```
Install the required dependencies:
```
pip install -r requirements.txt
```
Run the Streamlit application with:
```
streamlit run app.py
```
The app will then run in your browser.

## Author
Cai Xin (Johnny) Yan

Built with Python and Streamlit.
