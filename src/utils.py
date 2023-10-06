import os
import time
import traceback
from multiprocessing.pool import ThreadPool

from deep_translator import GoogleTranslator, MicrosoftTranslator

part_num = 1
_api_key = ""
_region = ""
_source = ""
_target = ""
_translator = 1


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


def file_output(path, ext_in, ext_out):
    try:
        return path.replace(ext_in, ext_out)
    except:
        traceback.print_exc()


def base_path(base_path, ext_in=None):
    try:
        result = base_path.path.replace(ext_in, "")
    except:
        traceback.print_exc()

    return result


def split_srt(input_file, ext_in, ext_out, max_phrases=50, max_chars=5000):
    try:
        with open(input_file.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        global part_num
        part_num = 1
        phrase_count = 0
        output_file = None

        base_name = base_path(input_file, ext_in)

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

        if input_file:
            output_file.close()
    except:
        traceback.print_exc()


def do_it(input_file, max_phrase=50, max_chars=5000):
    time.sleep(0.500)
    translator = ""

    if _translator == 1:
        translator = MicrosoftTranslator(
            api_key=_api_key,
            region=_region,
            source=_source,
            target=_target,
        )
    elif _translator == 2:
        translator = GoogleTranslator(source=_source, target=_target)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            translated = translator.translate_batch(f.readlines())
            os.remove(f.name)
        return translated

    except:
        traceback.print_exc()


def list_files(file, ext_in):
    base_name = base_path(file, ext_in)
    temp_files = []

    for i in range(1, part_num):
        file_out = str(f"{base_name}_{i}.tmp")

        with open(file_out, "r", encoding="utf8") as f:
            if type(f) is not None:
                temp_files.append(f.name)

    return temp_files


def translate_and_save(
    translator,
    api_key,
    region,
    source,
    target,
    input_file,
    ext_in="_en.srt",
    ext_out="_ptbr.srt",
):
    try:
        global _api_key
        global _region
        global _source
        global _target
        global _translator

        _api_key = api_key
        _region = region
        _source = source
        _target = target
        _translator = translator

        pool = ThreadPool(processes=10)

        base_name = base_path(input_file, ext_in)
        translated_filename = base_name + ext_out

        if not os.path.exists(translated_filename):
            split_srt(input_file, ext_in, ext_out)
            temp_files = list_files(input_file, ext_in)

            translated_parts = pool.map(do_it, temp_files)

            with open(translated_filename, "w", encoding="utf-8") as f:
                if translated_parts:
                    for translated_part in translated_parts:
                        formatted_translation = "\n".join(translated_part)
                        f.write(formatted_translation)
                        f.write("\n\n")
            f.close()

    except:
        traceback.print_exc()
