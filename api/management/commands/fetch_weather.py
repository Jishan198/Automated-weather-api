import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import DailyWeatherStats

class Command(BaseCommand):
    help = 'Fetches daily weather data from Open-Meteo and updates the MySQL database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching weather data...')
        
        # 1. Extract
        url = "https://api.open-meteo.com/v1/forecast?latitude=17.3850&longitude=78.4867&daily=temperature_2m_max,temperature_2m_min&timezone=Asia/Kolkata"
        response = requests.get(url)
        data = response.json()

        dates = data['daily']['time']
        max_temps = data['daily']['temperature_2m_max']
        min_temps = data['daily']['temperature_2m_min']

        # 2 & 3. Transform and Load
        for i in range(len(dates)):
            # Convert string date to a proper Python date object
            record_date = datetime.strptime(dates[i], '%Y-%m-%d').date()
            
            # update_or_create prevents duplicate entries if the script runs twice
            DailyWeatherStats.objects.update_or_create(
                record_date=record_date,
                defaults={
                    'max_temp': max_temps[i],
                    'min_temp': min_temps[i]
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated weather data!'))