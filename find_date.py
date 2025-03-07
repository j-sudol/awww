
from bs4 import BeautifulSoup
import  requests
def beautiful_soup_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def date(url):
    soup = beautiful_soup_scrape(url)

    table = soup.find('table', attrs={'class': 'infobox vevent'})
    date = table.find('span', attrs={'class': 'bday dtstart published updated'}) if table else None
    print(date)

with open("links.txt","r") as f:
    links = f.readlines()
    for link in links:
        link = link.strip()
        date(link)
