from bs4 import BeautifulSoup
from requests import get
import csv
import sys

date = sys.argv[1]
url = 'https://www.imdb.com/search/title?release_date='+date+'&sort=num_votes,desc&page=1'

response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

movie_containers = html_soup.find_all('div', {"class": "lister-item mode-advanced"})
first_movie =movie_containers[0]
first_year = first_movie.h3.find('span', {"class": "lister-item-year text-muted unbold"})
first_mscore = first_movie.find('span', {"class": "metascore  favorable"})
first_votes = first_movie.find('span', attrs = {'name':'nv'})
csv_file = open("csv.csv", 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Names', 'Years', 'Imdb Ratings', 'Metascore', "votes"])
for container in movie_containers:
    name = container.h3.a.text.encode('utf-8')

    year = container.h3.find("span", {"class": "lister-item-year text-muted unbold"}).text.encode('utf-8')

    imdb = float(container.strong.text.encode('utf-8'))

    m_score = container.find("span", {"class": "metascore  favorable"})
    if m_score is not None:
        m_score = m_score.text
    if m_score is not None:
        vote = container.find("span", attrs = {"name" : "nv"})['data-value'].encode('utf-8')
    csv_writer.writerow([name, year, imdb, m_score, vote])


csv_file.close()
