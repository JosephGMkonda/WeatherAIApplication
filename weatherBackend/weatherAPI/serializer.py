from rest_framework import serializers




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
