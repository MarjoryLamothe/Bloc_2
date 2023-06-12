from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (without opening browser window)
service = Service('/Users/lamothemarjory/Desktop/Scrap booking/chromedriver')  # Path to your ChromeDriver executable
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the website
url = 'https://weather.com/fr-FR/weather/today/l/f473c567d6a4bfa69fc4923cbbe38d6c77d37bb78c83ea75d0b5a89ac02632f1'
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Get the page source after the JavaScript content has loaded
page_source = driver.page_source

# Create a Beautiful Soup object
soup = BeautifulSoup(page_source, 'html.parser')

# Extract the weather data using Beautiful Soup
temperature = soup.select_one('span.TodayDetailsCard--feelsLikeTempValue--2icPt').get_text()
humidity = soup.select_one('div.WeatherDetailsListItem--wxData--kK35q').get_text()
wind_speed = soup.select_one('span.Wind--windWrapper--3Ly7c').get_text()

# Close the Selenium WebDriver
driver.quit()

# Create a pandas DataFrame
data = {
    'Temperature': [temperature],
    'Humidity': [humidity],
    'Wind Speed': [wind_speed]
}

df = pd.DataFrame(data)

# Save the data as a CSV file
df.to_csv('weather_data.csv', index=False)
