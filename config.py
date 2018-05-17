import os, logging

browser_height = 2500
browser_width = 2500
excluded_titlecase_words = ["of", "and", "the", "to", "at", "for"]
driver_executable = ""
browser = "chrome"
client_id = "306257817734742017"
token_secret = "MzA2MjU3ODE3NzM0NzQyMDE3.Dd5i3g.R9E_pT5wEMOWTa7QBU3z8ebfRNc"
wiki = "https://pathofexile.gamepedia.com/{}"

log_level = logging.INFO
log_filename = os.path.join("logs","main.log")
log_maxsize = 1024 * 256
log_backup_count = 5