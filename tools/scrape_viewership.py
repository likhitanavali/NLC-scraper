from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

data = pd.read_excel("CIFF Likhita Worksheet.xlsx", sheet_name="PRIMARY WORKSHEET")
c = 0
done = 0
for i in range(0, len(data)):
    try:
        url = data['thumbnail href'][i]
        response = requests.get(url)
        # create a BeautifulSoup object from the response content
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tag = soup.find('div')
        text = div_tag.get_text()
        pattern = r"(?<=National Viewership: )[\d,]+"
        match = re.search(pattern, text)
        if match:
            number = match.group(0)
            number = number.strip().replace(",",'')
            data['viewership'].loc[i] = int(number)
            done += 1
    except Exception as e:
        c += 1

print("Number of non updated rows = ", c)
print("Number of updated rows = ", done)
data.to_excel("CIFF Likhita Worksheet.xlsx", sheet_name="PRIMARY WORKSHEET", index=False)