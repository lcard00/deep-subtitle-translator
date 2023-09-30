import os
import asyncio
import utils

root_dir = "/home/lcard00/.torrents/courses/[Udemy] - The Complete 2023 Web Development Bootcamp/"
ext_in, ext_out = "_en.srt", "_ptbr.srt"
ignore_list = ["external_links.txt"]

files = utils.check_files(root_dir, ext_in, ignore_list)
for file in files:
    utils.split_srt(file, ext_in, ext_out)
