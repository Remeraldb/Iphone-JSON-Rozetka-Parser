from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

def scrape_iphones():

    webdriver_path = r'C:\ProgramData\chocolatey\lib\chromedriver\tools\chromedriver-win32\chromedriver.exe'
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)

    iphones_data = []

    visited_pages = set()

    page_num = 1

    while True:
        url = f'https://rozetka.com.ua/ua/mobile-phones/c80003/page={page_num};producer=apple/'

        driver.get(url)

        print("Visiting page:", driver.current_url)

        if driver.current_url in visited_pages:
            break

        visited_pages.add(driver.current_url)

        products = driver.find_elements(By.CLASS_NAME, 'goods-tile__inner')

        if not products:
            break

        for product in products:
            name = product.find_element(By.CLASS_NAME, 'goods-tile__title').text.strip()

            try:
                price = product.find_element(By.CLASS_NAME, 'goods-tile__price-value').text.strip()
            except:
                price = "Ціна не вказана"

            product_link = product.find_element(By.CLASS_NAME, 'goods-tile__picture').get_attribute('href')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(product_link)

            colors = get_colors(driver)

            try:
                characteristics_link = driver.find_element(By.LINK_TEXT, 'Характеристики')
                characteristics_link.click()
                time.sleep(1)
            except Exception as e:
                print("Характеристики link not found for product:", name)
                print(e)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            ram = get_characteristic(driver, "Оперативна пам'ять")
            memory = get_characteristic(driver, "Вбудована пам'ять")
            series = get_characteristic(driver, "Серія")
            camera = get_characteristic(driver, "Основна камера")
            display = get_characteristic(driver, "Частота оновлення екрана")
            processor = get_characteristic(driver, "Назва процесора")


            # Save the information about the product
            iphones_data.append({
                'Назва': name,
                'Ціна': price,
                "Оперативна пам'ять": ram,
                "Вбудована пам'ять": memory,
                "Серія": series,
                "Основна камера": camera,
                "Частота оновлення екрана": display,
                "Процесор": processor,
                "Кольори": colors
            })

            driver.close()

            driver.switch_to.window(driver.window_handles[0])

        page_num += 1

    driver.quit()

    return iphones_data

def get_colors(driver):
    try:
        colors_element = driver.find_element(By.CLASS_NAME, 'var-options__block_state_active')
        color_previews = colors_element.find_elements(By.CLASS_NAME, 'var-options__label_bold')
        colors = [color.text.strip() for color in color_previews]
        return colors
    except Exception as e:
        print("Failed to extract colors:", e)
        return []

def get_characteristic(driver, characteristic_name):
    try:

        xpath_label = f'''//dt[@class='characteristics-full__label']/span[text()="{characteristic_name}"]/parent::dt'''
        xpath_value = f"{xpath_label}/following-sibling::dd[1]"
        characteristic_element = driver.find_element(By.XPATH, xpath_value)

        if characteristic_element.find_elements(By.TAG_NAME, "a"):
            value = characteristic_element.find_element(By.TAG_NAME, "a").text.strip()
        elif characteristic_element.find_elements(By.TAG_NAME, "ul"):
            value = ', '.join([li.text.strip() for li in characteristic_element.find_elements(By.TAG_NAME, "li")])
        else:
            value = characteristic_element.text.strip()
        return value
    except Exception as e:
        print(f"Failed to extract {characteristic_name}: {e}")
        return "Не вказано"

def save_to_json(data):
    with open('iphones.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    iphones_data = scrape_iphones()
    save_to_json(iphones_data)
