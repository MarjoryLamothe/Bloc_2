import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_hotel_details(driver, url):
    driver.get(url)
    time.sleep(5)

    # Scroll to the map section to load the coordinates
    map_element = driver.find_element(By.CSS_SELECTOR, 'div.map_static_zoom')
    actions = ActionChains(driver)
    actions.move_to_element(map_element).perform()
    time.sleep(2)

    # Wait for the coordinates to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bui-button.map_static_zoom')))

    # Extract the page source after scrolling
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    coordinates = soup.select_one('span..hp_address_subtitle.js-hp_address_subtitle.jq_tooltip')['data-bbox']
    description = soup.select_one('div.property_description_content').text.strip()

    return {
        'coordinates': coordinates,
        'description': description,
    }


def scrape_booking():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service('/Users/lamothemarjory/Desktop/Scrap booking/chromedriver'), options=options)

    url = 'https://www.booking.com/city/fr/besancon.fr.html?aid=1610684&label=besancon-INxe9lsYXBwbJ2WRKpVNVgS553287993755%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-302082361864%3Alp9056017%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YfqnDqqG8nt10AsofPfvtt0&sid=bc443f56682bc19f8b2cb71157cfab72&inac=0&lang=fr&soz=1&lang_click=other&cdl=en-us&lang_changed=1'

    driver.get(url)
    time.sleep(5)

    # Scroll to the end of the page to load all the hotels
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)

        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    # Extract the page source after scrolling
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    hotel_tags = soup.select('div.sr_item.sr_item_new')[:10]

    data = []

    for hotel in hotel_tags:
        name = hotel.select_one('div.fcab3ed991 a23c043802').get_text()
        url = hotel.select_one('a.e13098a59f')['href']
        score = hotel.select_one('div.b5cd09854e.d10a6220b4').get_text()

        hotel_details = scrape_hotel_details(driver, url)

        data.append({
            'Name': name,
            'URL': url,
            'Score': score,
            'Coordinates': hotel_details['coordinates'],
            'Description': hotel_details['description'],
        })

    driver.quit()

    return data


if __name__ == '__main__':
    hotels = scrape_booking()

    df = pd.DataFrame(hotels)
    df.to_csv('hotels.csv', index=False)
    print('Data written to hotels.csv')
