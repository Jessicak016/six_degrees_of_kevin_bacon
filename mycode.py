import urllib
from urllib.parse import urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup
import os, re, json
import pydot
import itertools
import csv
import time
from itertools import islice

def main():
    step1_fetch_top_100_movies()
    step2_extract_movie_info()
    step3_get_metadata_using_omdb()
    step4_select_top5_actors()

######
def step1_fetch_top_100_movies():
    if os.path.exists('step1.html'):
        return
    response = urllib.request.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100')
    html_doc = response.read()
    html = html_doc.decode("utf-8")

    with open('step1.html', 'w') as outfile:
        outfile.write(html)

#######
def step2_extract_movie_info():
    if os.path.exists('step2.txt'):
        return

    with open('step1.html', 'r') as infile:
        html = infile.read()

    soup = BeautifulSoup(html, "html.parser")

    movie_rows = soup.find_all("h3")
    del movie_rows[-1]
    del movie_rows[-1]

    movie_list = []  # movie_list ==> list of dictionaries
    for row in movie_rows:
        movie = {}  # Initialize dictionary
        for title in row.find_all("a"):
            t = title.get_text()
            movie['Title'] = t
        for span in row.find_all("span", {"class": "lister-item-index unbold text-primary"}):
            f = span.get_text()
            rank_match = re.search(r"\d+(?=\.)", f)
            movie['Rank'] = rank_match.group()
        for tag in row.find_all("a"):
            idx = tag.get('href')
            id_match = re.search(r"(?<=\/title\/).+(?=\/\?)", idx)
            movie['IMDB_ID'] = id_match.group()

        if movie:
            movie_list.append(movie)

    with open('step2.txt', 'w') as outfile:
        data_writer = csv.DictWriter(outfile,
                        fieldnames=['IMDB_ID', 'Rank', 'Title'],
                        extrasaction='ignore',
                        delimiter='\t', quotechar='"')
        data_writer.writeheader()
        data_writer.writerows(movie_list)


######
def step3_get_metadata_using_omdb():

    if os.path.exists('step3.txt'):
        return

    with open('step2.txt', 'r') as infile:
        movie_reader = csv.DictReader(infile, delimiter='\t', quotechar='"')
        id_url = "http://www.omdbapi.com/?i="
        out = [] #list of dictionaries
        count = 0
        total = 100
        for movie in movie_reader:
            idw = movie['IMDB_ID']
            complete_url = id_url + idw
            response = urllib.request.urlopen(complete_url)
            html_doc = response.read()
            html = html_doc.decode("utf-8")
            if html:
                out.append(html)

            count += 1
            print('{0:3}/{1}'.format(count, total), end='\r')

            time.sleep(5)

    # 3. Store each JSON in that list as a line in step3.txt
    with open('step3.txt', 'w') as outfile:
        json_strings = '\n'.join(out)
        outfile.write(json_strings)

def step4_select_top5_actors():
    if os.path.exists('step4.json'):
        return
    with open('step3.txt', 'r') as infile:
        data = []
        for line in infile:
            movie = json.loads(line)
            outputDict = {}
            outputDict['Title'] = movie['Title']
            actors_list = movie['Actors'].split(", ")
            outputDict['Actors'] = actors_list
            data.append(outputDict)
    # 3. Write a json file containing a list of dictionaries with keys Title and Actors
    with open('step4.json', 'w') as outfile:
        outfile.write(json.dumps(data))

def step5_create_graphviz_dot_file():
    with open('step4.json', 'r') as infile:
        movie_data = json.loads(infile.read())
        graph = pydot.Dot(graph_type='graph', charset='utf8')

        count = 0
        for movie in movie_data:
            actors = movie['Actors']
            actor_pairs = itertools.combinations(actors, 2)
            for pair in actor_pairs:
                edge = pydot.Edge(pair[0], pair[1])
                graph.add_edge(edge)
                count += 1
        print('Added {0} edges to the graph'.format(count))
        print('Writing graph file ...')
        graph.write('actors_graph_output.dot')




if __name__=='__main__':
    main()
