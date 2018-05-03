# Modified from: http://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python
from io import BytesIO
from base64 import b64decode
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

import config


def get_element_screenshot(element:WebElement):
    driver = element._parent
    ActionChains(driver).move_to_element(element).perform()
    src_base64 = driver.get_screenshot_as_base64()
    src_png = b64decode(src_base64)
    x = element.location["x"]
    y = element.location["y"]
    w = element.size["width"]
    h = element.size["height"]
    image = Image.open(BytesIO(src_png))
    image = image.crop((int(x), int(y), int(x+w), int(y+h)))
    return image

def get_image(item):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=config.chromedriver,options=options)
    driver.set_window_size(config.browser_width,config.browser_height)
    item = quote(item)
    driver.get(f"https://pathofexile.gamepedia.com/{item}")
    try:
        e = driver.find_element_by_class_name("item-box")
        return get_element_screenshot(e)
    except Exception as e:
        return None

