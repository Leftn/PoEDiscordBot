# Modified from: http://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python
import hashlib
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image

import config

def get_element_screenshot(element:WebElement, save_name):
    """
    This function takes a screenshot of the whole browser window and crops out everything but the selected web element

    :param element: selenium web element object
    :return: Image: PIL object of the specified web element
    """
    driver = element._parent
    driver.save_screenshot(f"images/{save_name}.png")
    x = element.location["x"]
    y = element.location["y"]
    w = element.size["width"]
    h = element.size["height"]
    if w and h:
        image = Image.open(open(f"images/{save_name}.png", "rb"))
        image = image.crop((int(x), int(y), int(x+w), int(y+h)))
        image.save(f"images/{save_name}.png")
        return f"images/{save_name}.png"
    else:
        return None

def get_element_box(driver):
    e = driver.find_element_by_class_name("item-box")
    if not e.size["width"] and not e.size["height"]: # Check if item-box is hidden
        e = driver.find_element_by_class_name("infocard")
    return e

def get_image(item):
    if config.browser == "chrome":
        options = Options()
        options.add_argument("--headless") #If you are for some reason not running the bot on a headless server
        driver = webdriver.Chrome(executable_path=config.driver_executable, chrome_options=options)
    elif config.browser == "phantomjs":
        driver = webdriver.PhantomJS()
    driver.set_window_size(config.browser_width,config.browser_height)
    item = quote(item) # urllib.parse: Converts special characters to html safe encodings e.g. ' ' --> %20
    driver.get(config.wiki.format(item))
    return get_element_screenshot(get_element_box(driver), hashlib.md5(item.encode("utf-8")).hexdigest())
