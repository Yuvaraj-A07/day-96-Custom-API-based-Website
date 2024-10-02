import requests
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# OpenWeatherMap API setup
API_KEY = 'your_openweathermap_api_key'
CITY = 'your_city'
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

# Email setup
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_email_password'
RECEIVER_EMAIL = 'receiver_email@gmail.com'

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

def get_weather():
    response = requests.get(URL)
    weather_data = response.json()

    weather_description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    wind_speed = weather_data['wind']['speed']

    report = (f"Today's Weather in {CITY}:\n"
              f"Temperature: {temp}°C\n"
              f"Feels Like: {feels_like}°C\n"
              f"Condition: {weather_description}\n"
              f"Wind Speed: {wind_speed} m/s")

    send_email("Daily Weather Report", report)

schedule.every().day.at("07:00").do(get_weather)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
