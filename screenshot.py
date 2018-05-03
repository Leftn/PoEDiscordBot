# Modified from: http://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python

import os
from subprocess import Popen, PIPE

from selenium import webdriver

import config

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height):
    driver = webdriver.PhantomJS()
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(service_log_path="/var/log/phantomjs/ghostdriver.log")
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    driver.save_screenshot(screen_path)


def do_crop(params):
    command = [
        "convert",
        params["screen_path"],
        "-crop", "%sx%s+0+0" % (params["width"], params["height"]),
        params["crop_path"]
    ]
    execute_command(" ".join(command))

def get_screen_shot(**kwargs):
    url = kwargs["url"]
    width = int(kwargs.get("width", config.browser_width)) # screen width to capture
    height = int(kwargs.get("height", config.browser_height)) # screen height to capture
    filename = kwargs.get("filename", "screen.png") # file name e.g. screen.png
    path = kwargs.get("path", ROOT) # directory path to store screen

    crop = kwargs.get("crop", False) # crop the captured screen
    crop_width = int(kwargs.get("crop_width", width)) # the width of crop screen
    crop_height = int(kwargs.get("crop_height", height)) # the height of crop screen
    crop_replace = kwargs.get("crop_replace", False) # does crop image replace original screen capture?


    screen_path = abspath(path, filename)
    crop_path = screen_path


    do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, "crop_"+filename)
        params = {
            "width": crop_width, "height": crop_height, "crop_path":crop_path, "screen_path":screen_path
        }
        do_crop(params)
    return screen_path, crop_path


if __name__ == "__main__":
    """
        Requirements:
        Install NodeJS
        Using Node"s package manager install phantomjs: npm -g install phantomjs
        install selenium (in your virtualenv, if you are using that)
        install imageMagick
        add phantomjs to system path (on windows)
    """

    url = "http://stackoverflow.com/questions/1197172/how-can-i-take-a-screenshot-image-of-a-website-using-python"
    screen_path, crop_path = get_screen_shot(
        url=url, filename="sof.png",
        crop=True, crop_replace=False
    )