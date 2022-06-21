import os
import re
import pysrt
import scraper_constants

raw_data_path = ''

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
        #with open(file_name, 'w+', encoding='ISO-8859-1') as handle:
        with open(file_name, 'w+', encoding='utf-8') as handle:
            handle.write(script)
            handle.close()
    else:
        print('save_script_file(): File exists so skipping save: ' + file_name)

def extract_script(fn):
    '''
    # read file line by line
    file = open(fn, "r")
    lines = file.readlines()
    file.close()

    text = ''
    for line in lines:
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line.rstrip('\n')
        text = text.lstrip()
    return text'''
    subs = pysrt.open(fn)
    text = ''
    for line in subs:
        text += line.text
    return text

def extract(titles):
    for fn in titles:
        try:
            temp = fn.split("(")
            title = temp[0].replace(".", " ")
            year, season = temp[1].split(")")
            season = int(season.split(".")[2][1:])
            title = clean_title(title)
            path_elements = ["test", "tv-series", title + '_' + year, str(season)]
            ensure_script_file_path(path_elements)
            ep_path = '/'.join(path_elements)
            ep_list = os.listdir(raw_data_path + "/" + fn)
            for ep in ep_list:
                try:
                    ep_file = os.listdir(raw_data_path + "/" + fn + "/" + ep)[0]
                    raw_script = extract_script(raw_data_path + "/" + fn + "/" + ep + "/" + ep_file)
                    script = clean_script(raw_script)
                    ep_filename = ep + '.txt'
                    save_script_file('/'.join([ep_path, ep_filename]), script)
                except Exception as e:
                    print("Could not read file - " + raw_data_path + "/" + fn + "/" + ep + ", errors out with exception - " + str(e))
        except Exception as e:
            print("Folder name " + fn + " is not of correct format, errors out with exception - " + str(e))

def main():
    titles = os.listdir(raw_data_path)
    extract(titles)

if __name__ == "__main__":
    main()