import random

weather_events = ["clear", "clear", "clear", "clear", "clear", "cloudy",
		"cloudy", "cloudy", "partlycloudy", "partlycloudy", "partlycloudy",
		"showers", "showers", "showers", "rain", "rain", "rain"]

def make_weather(days, weather_events):
	weather_dict = {}
	i = 1
	while i < days + 1:
		duration = random.randint(1, 5)
		forecast = random.choice(weather_events)
		if forecast == "rain" and duration > 4:
			duration = 3
		for j in range(duration):
			weather_dict[i] = forecast
			i += 1
	return weather_dict
	


def weather_check(garden):
	if garden.weather[garden.day_count] == "clear":
		garden.daily_sun = 5
		garden.daily_water = 0
		garden.daily_evap = 2
	
	elif garden.weather[garden.day_count] == "partlycloudy":
		garden.daily_sun = 4
		garden.daily_water = 0
		garden.daily_evap = 1
		
	elif garden.weather[garden.day_count] == "cloudy":
		garden.daily_sun = 2
		garden.daily_water = 0
		garden.daily_evap = 0
		
	elif garden.weather[garden.day_count] == "showers":
		garden.daily_sun = 0
		garden.daily_water = 5
		garden.daily_evap = 0	
		
	elif garden.weather[garden.day_count] == "rain":
		garden.daily_sun = 0
		garden.daily_water = 10
		garden.daily_evap = 0
	