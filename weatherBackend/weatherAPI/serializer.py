from rest_framework import serializers
from datetime import datetime 



class HistoricalWeatherSerializer(serializers.Serializer):
    date = serializers.DateField()
    temperature_max = serializers.FloatField()
    temperature_min = serializers.FloatField()
    

class CurrentWeatherSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    temperature = serializers.FloatField()
    windspeed = serializers.FloatField()
    winddirection = serializers.FloatField()
    is_day = serializers.BooleanField()
    weathercode = serializers.IntegerField()

class WeatherAPISerializer(serializers.Serializer):
    generationtime_ms = serializers.FloatField()
    utc_offset_seconds = serializers.IntegerField()
    timezone = serializers.CharField()
    timezone_abbreviation = serializers.CharField()
    elevation = serializers.FloatField()

    # historical = HistoricalWeatherSerializer(many=True)
    current_weather = CurrentWeatherSerializer()

    # historical = serializers.ListField(child=serializers.DictField())
    predicted_weather = serializers.ListField(child=serializers.DictField())
    alerts = serializers.SerializerMethodField()

    def get_alerts(self, obj):
        predicted_weather = obj.get('predicted_weather',[])
        alerts = []

        hot_threshold = 30
        cold_threshold = 10

        for forecast in predicted_weather:
            date = forecast.get('date')

            max_temp = forecast.get('predicted_temperature_max',0)
            min_temp = forecast.get('predicted_temperature_min',0)
            print(f"Processing forecast for {forecast['date']}: max={max_temp}, min={min_temp}")  # Debug

            if max_temp >= hot_threshold:
                alerts.append(f"On {date}, it is expected to be hot ({max_temp:.1f}°C). Remember to drink more water")
            if min_temp <= cold_threshold:
                alerts.append(f"On {date}, it is expected to be cold ({min_temp:.1f}°C). Stay warm and dress in layers")
        

        return alerts



