import os

from dotenv import load_dotenv

import utils

load_dotenv()

root_dir = os.getenv("root_dir")
api_key = os.getenv("api_key")
region = os.getenv("region")
source = "en"
target = "pt"
ext_in, ext_out = "_en.srt", "_ptbr.srt"
ignore_list = ["external_links.txt"]

# translator types:
# 1 - Microsoft
# 2 - Google Translator
translator = 2

files = utils.check_files(root_dir, ext_in, ignore_list)
for file in files:
    utils.translate_and_save(
        translator, api_key, region, source, target, file, ext_in, ext_out
    )
