import os
import json
os.system("cls" if os.name == "nt" else "clear")
log_level ={"File name": "", "ERROR": 0, "WARN": 0, "TRACE": 0, "DEBUG":0}
log_file_folder = os.getcwd()
files = os.listdir(log_file_folder)
log_files = [file for file in files if file.lower().endswith(".log")]
log_files_path =[]

def save_analysis(log_file_folder, detect):
    saved_log_analysis ="log_analysis.json"
    analysis_file = os.path.join(log_file_folder, saved_log_analysis)
    if not os.path.exists(analysis_file) or os.path.getsize(analysis_file) == 0:
        with open(analysis_file, "w") as log_file:
            data = [ ]
            json.dump(data, log_file)
            pass
    with open(analysis_file, "r") as log_file:
        data = json.load(log_file)
        data.append(detect.copy())
    with open(analysis_file, "w") as log_file:
        json.dump(data, log_file, indent=4)
        print(f"Analysis saved to {os.path.basename(analysis_file)}")


for log_file in log_files:
    log_files_path.append(os.path.join(log_file_folder, log_file))

for log_file in log_files_path:
    if os.path.exists(log_file):
        log_level["File name"] = os.path.basename(log_file)
        with open(log_file, "r") as logs:
            log_contents = logs.readlines()
        for line in log_contents:
            for level in log_level:
                if level != "File name":
                    if level in line.upper():
                        log_level[level] += 1        
        save_analysis(log_file_folder, log_level)
        for words, count in log_level.items():
            print(f"{words}: {count}")
        for level in log_level:
            if level == "File name":
                log_level[level] = ""
            else:
                log_level[level] = 0






