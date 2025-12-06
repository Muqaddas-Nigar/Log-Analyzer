import os
import json
from pathlib import Path
import logging
os.system("cls" if os.name == "nt" else "clear")
script_log = (Path(__file__).parent.resolve()/'script.log')
script_log.touch()
logging.basicConfig(
    filename=script_log,
    filemode='a',
    level=logging.DEBUG,
    style="{",
    format="{asctime} - {levelname} - {message}"
    )
# logging.disable(logging.DEBUG)

class LogFolderNotFoundError(Exception):
    pass


def save_analysis(log_info, json_file):
    try:
        with open(json_file, 'r') as j_file:
            data = json.load(j_file)
            data.append(log_info)
        with open(json_file, 'w') as j_file:
            json.dump(data, j_file, indent=4)
    except FileNotFoundError:
        logging.error("Analysis can't be saved: JSON file not found")
        raise FileNotFoundError



def analyze_file(log_file):
    log_info = {"ERROR": 0, "WARN": 0, "TRACE": 0, "DEBUG": 0, "CRITICAL": 0, "INFO": 0}
    try:
        empty_line = 0
        
        with open(log_file) as log:
            data = log.readlines()
    except FileNotFoundError:
        logging.error(f'File not found {log_file.name}')
        raise FileNotFoundError
    else:
        print(f'Total Lines:{len(data)}')
        for line in data:
            if line == '\n':
                empty_line += 1
            else:
                for key in log_info.keys():
                    if key in line or key.lower() in line:
                        log_info[key] += 1
        return log_info


def data_json():
    json_file = Path(__file__).parent.resolve()/'analysis.json'
    try:
        with open(json_file, 'w') as j_file:
            json.dump([], j_file, indent=4)
    except FileNotFoundError:
        json_file.touch()
        with open(json_file, 'w') as j_file:
            json.dump([], j_file, indent=4)
        logging.info('Json file created')
    return json_file
        

def get_files():
    log_folder = Path(__file__).parent.resolve()/'Log folder'
    if not log_folder.exists():
        logging.error('No log folder found')
        raise LogFolderNotFoundError
    log_files = list(log_folder.glob('*.log'))
    # skip empty files
    log_files = [file for file in log_files if file.stat().st_size != 0]
    # raise error if no log file is found
    if not log_files:
        logging.error(f'No log file found')
        raise FileNotFoundError
    return log_files


def main():
    logging.info('Program start')
    files = get_files()
    json_file = data_json()
    for file in files:
        print(f'Analyzing file:{file.name}')
        logging.info(f'Analyzing file: {file.name}')
        print(f'Size: {file.stat().st_size/1024:.0f}KB')
        log_info = analyze_file(file)
        save_analysis(log_info, json_file)
    logging.info("program end")

if __name__ == "__main__":
    main()


