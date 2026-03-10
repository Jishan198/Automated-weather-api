from rest_framework import serializers
from .models import DailyWeatherStats

class DailyWeatherStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWeatherStats
        fields = '__all__'