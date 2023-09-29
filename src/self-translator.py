import os
import asyncio
import pysubs2
import tracceback
from deep_translator import GoogleTranslator
from concurrent.futures import TrheadPoolExecutor

root_directory = "/home/lcard00/.torrents/courses/[Udemy] - The Complete 2023 Web Development Bootcamp/"
ext_in, ext_out = "_en.srt", "_ptbr.srt"
