import os, logging

browser_height = 2500
browser_width = 2500
excluded_titlecase_words = ["of", "and", "the", "to", "at", "for"]
driver_executable = ""
browser = "chrome"
client_id = ""
token_secret = ""
wiki = "https://pathofexile.gamepedia.com/{}"

log_level = logging.INFO
log_filename = os.path.join("logs","main.log")
log_maxsize = 1024 * 256
log_backup_count = 5