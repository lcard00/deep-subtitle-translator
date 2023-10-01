from dotenv import load_dotenv
import os
import utils

load_dotenv()

root_dir = "/home/lcard00/.torrents/courses/[Udemy] - The Complete 2023 Web Development Bootcamp/"
ext_in, ext_out = "_en.srt", "_ptbr.srt"
ignore_list = ["external_links.txt"]

api_key = os.getenv("api_key")
region = os.getenv("region")
source = "en"
target = "pt"


files = utils.check_files(root_dir, ext_in, ignore_list)
for file in files:
    utils.translate_and_save(api_key, region, source, target, file, ext_in, ext_out)
