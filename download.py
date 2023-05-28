import os
import re
import pysrt
import scraper_constants
import zipfile

raw_data_path = ''

raw_data_path2 = ''

def clean_title(raw_title):
    clean_title = (raw_title + '.')[:-1]
    clean_title = clean_title.strip()
    clean_title = clean_title.replace('\\', scraper_constants.BACKSLASH)
    clean_title = clean_title.replace('/', scraper_constants.SLASH)
    clean_title = clean_title.replace(':', scraper_constants.COLON)
    clean_title = clean_title.replace('*', scraper_constants.STAR)
    clean_title = clean_title.replace('<', scraper_constants.LESS_THAN)
    clean_title = clean_title.replace('>', scraper_constants.GREATER_THAN)
    clean_title = clean_title.replace('?', scraper_constants.QUESTION_MARK)
    clean_title = clean_title.replace('|', scraper_constants.PIPE)
    return clean_title

def clean_script(raw_script):
    clean_script = re.sub(r'\s+', ' ', raw_script).strip()
    clean_script = clean_script.replace('\\', '')
    clean_script = clean_script.replace('<i>', '')
    clean_script = clean_script.replace('</i>', '')
    clean_script = clean_script.replace('♪', '')
    clean_script = clean_script.replace("’", "'")
    clean_script = clean_script.replace("‘", "'")
    clean_script = clean_script.replace("“", '"')
    clean_script = clean_script.replace("”", '"')
    clean_script = clean_script.replace("…", "...")
    clean_script = clean_script.replace("‐", "-")
    clean_script = clean_script.replace("—", "-")
    clean_script = clean_script.replace('ě', 'e')
    clean_script = clean_script.replace('ş', 's')
    clean_script = clean_script.replace('â', 'a')
    clean_script = clean_script.replace('â€™', "'")
    clean_script = clean_script.replace('â™ª', "")
    clean_script = clean_script.replace('\u014d', '')
    clean_script = clean_script.replace('\u2010', '')
    clean_script = clean_script.replace('\u0153', '')
    clean_script = clean_script.replace('\u0161', '')
    clean_script = clean_script.replace('\u0413', '')
    clean_script = clean_script.replace('\u0130', '')
    clean_script = clean_script.replace('\u016b', '')
    clean_script = clean_script.replace('\u016d', '')
    clean_script = clean_script.replace('\u0110', '')
    clean_script = clean_script.replace('\u0441', '')
    clean_script = clean_script.replace('\u0101', '')
    clean_script = clean_script.replace('\u0111', '')
    clean_script = clean_script.replace('\u202d', '')
    return clean_script

def ensure_script_file_path(path_elements):
    if path_elements is not None and len(path_elements) > 0:
        current_path = ''
        for path_element in path_elements:
            if current_path == '':
                current_path = path_element
            else:
                current_path = '/'.join([current_path, path_element])
            if not os.path.exists(current_path):
                os.mkdir(current_path)

def save_script_file(file_name, script):
    if not os.path.isfile(file_name):
        with open(file_name, 'w+', encoding='ISO-8859-1') as handle:
        #with open(file_name, 'w+', encoding='utf-8') as handle:
            handle.write(script)
            handle.close()
    else:
        print('save_script_file(): File exists so skipping save: ' + file_name)

def extract_script(fn):
    subs = pysrt.open(fn)
    text = ''
    for line in subs:
        text = text + " " + line.text
    return text

def extract(titles):
    for fn in titles:
        try:
            if fn.endswith(".zip"):
                with zipfile.ZipFile(raw_data_path + "/" + fn, 'r') as fnextract:
                    fnextract.extractall(raw_data_path2 + "/" + fn)
            temp = fn.split("(")
            title = temp[0].replace(".", " ")
            year, rem = temp[1].split(")")
            if rem.startswith(".tv"):
                season = int(rem.split(".")[2][1:])
                title = clean_title(title)
                path_elements = ["test", "tv-series", title + '_' + year, str(season)]
                ensure_script_file_path(path_elements)
                ep_path = '/'.join(path_elements)
                ep_list = os.listdir(raw_data_path2 + "/" + fn)
                if len(ep_list) != 0:
                    for ep in ep_list:
                        try:
                            ep_file = os.listdir(raw_data_path2 + "/" + fn + "/" + ep)[0]
                            try:
                                raw_script = extract_script(raw_data_path2 + "/" + fn + "/" + ep + "/" + ep_file)
                            except Exception as e:
                                print("Error out at extract_script() - " + raw_data_path2 + "/" + fn + "/" + ep + ", errors out with exception - " + str(e))
                            script = clean_script(raw_script)
                            ep_no = ''.join(filter(str.isdigit, ep))
                            ep_filename = ep_no + ". " + ep + '.txt'
                            save_script_file('/'.join([ep_path, ep_filename]), script)
                        except Exception as e:
                            print("Could not read file - " + raw_data_path2 + "/" + fn + "/" + ep + ", errors out with exception - " + str(e))
            elif rem.startswith('.eng'):
                title = clean_title(title)
                path_elements = ["test", "movies"]
                ensure_script_file_path(path_elements)
                movie_path = '/'.join(path_elements)
                file_list = os.listdir(raw_data_path2 + "/" + fn)
                if len(file_list) != 0:
                    for file in file_list:
                        try:
                            if file.endswith(".srt"):
                                try:
                                    raw_script = extract_script(raw_data_path2 + "/" + fn + "/" + file)
                                except Exception as e:
                                    print("Error out at extract_script() - " + raw_data_path2 + "/" + fn + "/" + file + ", errors out with exception - " + str(e))
                                script = clean_script(raw_script)
                                movie_filename = title + '_' + year + '.txt'
                                save_script_file('/'.join([movie_path, movie_filename]), script)
                                break
                        except Exception as e:
                            print("Could not read file - " + raw_data_path2 + "/" + fn + "/" + file + ", errors out with exception - " + str(e))
        except Exception as e:
            print("Folder name " + fn + " is not of correct format, errors out with exception - " + str(e))

def main():
    titles = os.listdir(raw_data_path)
    extract(titles)

if __name__ == "__main__":
    main()