import requests
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search


def beautiful_soup_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

# TIOBE Index URL
url = "https://www.tiobe.com/tiobe-index/"

soup = beautiful_soup_scrape(url)
table = soup.find("table", attrs={"class": "table table-striped table-top20"})
rows = table.find_all("tr")[1:]

data = []

for row in rows:
    columns = row.find_all("td")
    rank = columns[0].text.strip()
    name = columns[4].text.strip()

    img_tag = columns[3].find("img")
    img_link = "https://www.tiobe.com" + img_tag["src"] if img_tag else "Brak linku"

    usage = columns[5].text.strip()
    page_link = f"{url}{name.replace(' ', '-').replace('+', 'plus').replace('#', 'sharp').replace('/','-').lower()}/"

    wiki_link = ""
    date = ""

    data.append(
        {"Rank": rank, "Name": name, "Usage": usage, "Image": img_link, "Page Link": page_link, "Wiki Link": wiki_link,
         "Date": date})

df = pd.DataFrame(data)

js_url = "https://en.wikipedia.org/wiki/JavaScript"

for i, row in df.iterrows():
    query = f"{row['Name']} programming language site:en.wikipedia.org"
    for url in search(query, stop=1):
        df.at[i, "Wiki Link"] = url
        if row["Name"] == "JavaScript":
            df.at[i, "Wiki Link"] = js_url

def get_date(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', attrs={'class': 'infobox vevent'})
    date = table.find('span', attrs={'class': 'bday dtstart published updated'}).text
    return date

for i, row in df.iterrows():
    df.at[i, "Date"] = get_date(row["Wiki Link"])

for _, row in df.iterrows():
    name_sanitized = row["Name"].replace(' ', '-').replace('+', 'plus').replace('#', 'sharp').replace('/','-').lower()
    md_filename = f"{name_sanitized}.md"

    with open(md_filename, "w", encoding="utf-8") as file:
        file.write(f"![{row['Name']}]({row['Image']})\n\n")
        file.write(f"First appeared: {row['Date']}\n\n")
        file.write(f"[Rating history]({row['Page Link']})\n\n")
        file.write(f"[More information]({row['Wiki Link']})\n\n")

output_file = "list.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("## Top 20 Programming languages\n\n")
    f.write("| Rank | Rating | Name |\n")
    f.write("|------|-------|------|\n")

    for _, row in df.iterrows():
        name_sanitized = row["Name"].replace(' ', '-').replace('+', 'plus').replace('#', 'sharp').replace('/','-').lower()
        f.write(f"| {row['Rank']} | {row['Usage']} | [{row['Name']}]({name_sanitized}.md) |\n")

print("Markdown files generated successfully!")

