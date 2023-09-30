import asyncio
import os
import traceback
from multiprocessing.pool import ThreadPool

from deep_translator import GoogleTranslator

part_num = 1
base_path = ""


def read_list(file, list):
    for item in list:
        if file.endswith(item):
            return True
        else:
            return False


def check_files(root_dir, ext_in, ignore_list):
    result = []
    try:
        for folders in os.scandir(root_dir):
            if folders.is_dir():
                for files in os.scandir(folders.path):
                    file_name = files.name
                    if (
                        files.is_file()
                        and file_name.endswith(ext_in)
                        and not read_list(file_name, ignore_list)
                    ):
                        result.append(files)
        return result
    except:
        traceback.print_exc()


async def multi(param):
    await asyncio.sleep(0.01)
    subprocess = []
    pool = ThreadPool(processes=19)

    try:
        paralell_result = pool.apply_async(load_file)
        subprocess.append(paralell_result)
        paralell_list = [result.get(timeout=120) for result in subprocess]
        return paralell_list
    except:
        traceback.print_exc()


def file_output(path, ext_in, ext_out):
    try:
        return path.replace(ext_in, ext_out)
    except:
        traceback.print_exc()


def split_srt(input_file, ext_in, ext_out, max_phrases=50, max_chars=5000):
    try:
        with open(input_file.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        part_num = 1
        phrase_count = 0
        output_file = None

        base_name = input_file.path.replace(ext_in, "")

        for line in lines:
            if not output_file or (
                phrase_count == max_phrases and len(line) <= max_chars
            ):
                if output_file:
                    output_file.close()
                output_filename = f"{base_name}_{part_num}.tmp"
                output_file = open(output_filename, "w", encoding="utf-8")
                part_num += 1
                phrase_count = 0

            output_file.write(line)

            if line.strip() == "":
                phrase_count += 1

        if output_file:
            output_file.close()
    except:
        traceback.print_exc()
