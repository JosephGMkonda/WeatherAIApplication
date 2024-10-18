import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializer import WeatherAPISerializer
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np 


@api_view(['GET'])
def get_weatherData(request, district):
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={district},Malawi&format=json&limit=1"
    headers = {
        'User-Agent': 'weatherAPI (josephmkonda1@gmail.com)' 
    }

    try:
        geocode_response = requests.get(geocode_url, headers=headers)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if not geocode_data or 'Malawi' not in geocode_data[0]['display_name']:
            return Response({'Error': 'District not found'}, status=status.HTTP_404_NOT_FOUND)

        latitude = float(geocode_data[0]['lat'])
        longitude = float(geocode_data[0]['lon'])

        # Fetching historical weather data (last 7 days)
        today = datetime.today()
        start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

        historical_weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min&timezone=GMT"
        
        historical_response = requests.get(historical_weather_url)
        historical_response.raise_for_status()
        historical_data = historical_response.json()

        # Fetching current weather data
        current_weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        current_weather_response = requests.get(current_weather_url)
        current_weather_response.raise_for_status()
        current_weather_data = current_weather_response.json()

        # Prepare the combined data
        # Parse daily weather data from the arrays
        daily_data = historical_data['daily']
        weather_history = []
        alerts = []

        # Defining weather threshold

        high_temp_threshold = 30
        low_temp_threshold = 10

        
        for i in range(len(daily_data["time"])):

            max_temp = daily_data["temperature_2m_max"][i]
            min_temp = daily_data["temperature_2m_min"][i]

            
            if max_temp > high_temp_threshold:
                alerts.append(f"On {daily_data['time'][i]}, it is expected to be hot ({max_temp})°C. Remember to drink more water")
            if min_temp < low_temp_threshold:
            
                alerts.append(f"On {daily_data['time'][i]}, it is expected to be cold ({min_temp})°C. Stay warm and dress in layers")
            
            
            weather_history.append({
                "date": daily_data["time"][i],  
                "temperature_max": max_temp,
                "temperature_min": min_temp
                 })

        # add alert to the current temperature
        current_temp = current_weather_data["current_weather"]["temperature"]

        if current_temp > high_temp_threshold:
            alerts.append(f"Currently it is hot ({current_temp})°C. Drink plenty water")
        if current_temp < low_temp_threshold:
            alerts.append(f"Currently it is cold ({current_temp})°C. Stay indoor if Possible")

        # preparing historical data frame into pandas
        df = pd.DataFrame(weather_history)
         # converting dates into formatt which machine learning can understand

        df["date"] = pd.to_datetime(df["date"])
        df['day_of_year'] = df['date'].dt.dayofyear

        # Selecting features for (X) and (Y) for max and min temperature prediction
        X = df[['day_of_year']]
        y_max = df['temperature_max']
        y_min = df['temperature_min']

        model_max = LinearRegression()
        model_min = LinearRegression()

        # training the model 
        model_max.fit(X, y_max)
        model_min.fit(X, y_min)

        # Predicting the temperature for the next 7 days
        future_dates = pd.date_range(today, periods=7).to_frame(index=False, name='date')
        future_dates['day_of_year'] = future_dates['date'].dt.dayofyear

        # Make of Predictions
        predicted_max_temps = model_max.predict(future_dates[['day_of_year']])
        predicted_min_temps = model_min.predict(future_dates[['day_of_year']])

        future_weather = []
        for i in range(len(future_dates)):
            future_weather.append({
                'date': future_dates['date'].iloc[i].strftime('%Y-%m-%d'),
                'predicted_temperature_max': float(predicted_max_temps[i]),
                'predicted_temperature_min': float(predicted_min_temps[i])

            })
            

        weather_data = {
            'generationtime_ms': current_weather_data.get('generationtime_ms', 0),
            'utc_offset_seconds': current_weather_data.get('utc_offset_seconds', 0),
            'timezone': current_weather_data.get('timezone', ''),
            'timezone_abbreviation': current_weather_data.get('timezone_abbreviation', ''),
            'elevation': current_weather_data.get('elevation', 0),
            'historical': weather_history, 
            'current_weather': current_weather_data['current_weather'],
            'predicted_weather': future_weather,
            'alerts': alerts


        }

        

        # Serialize the data
        serializer = WeatherAPISerializer(data=weather_data)
        if serializer.is_valid():
            
            return Response(serializer.data)
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
