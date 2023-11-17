import requests

url = "http://api.weatherapi.com/v1/current.json?key=d73af82268fa4a64a3c200007231402&q=Orlando&aqi=no"
responses = requests.get(url)
weather_json = responses.json()

print(weather_json)

temp = weather_json.get("current").get("temp_f")
print(temp)
description = weather_json.get("current").get("condition").get("text")

print("Today's weather in Orlando is", description, "and", temp, "degrees")


# Example of City variable for dynamic input
city = "London"
url = (
    "http://api.weatherapi.com/v1/current.json?key=d73af82268fa4a64a3c200007231402&q="
    + city
    + "&aqi=no"
)
responses = requests.get(url)
weather_json = responses.json()
temp = weather_json.get("current").get("temp_f")
description = weather_json.get("current").get("condition").get("text")
print("Today's weather in", city, "is", description, "and", temp, "degrees")
