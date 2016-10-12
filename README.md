Six Degrees of Kevin Bacon

In this project, I built and visualized a social network of movie actors: 
the graph nodes represent individual actors, and two actors are connected by an edge in the graph 
if they co-starred at least one movie together from an IMDB top 100 movies list - with no edge between them otherwise.  
To do this, I applied my knowledge of HTML parsing with BeautifulSoup and JSON processing, 
and gained experienced with a widely-used graph visualization package, GraphViz, through this project.

Pyton packages used:
- urllib
- bs4 (BeautifulSoup) 
- re
- json
- pydot
- time
- itertools 

Package:
- GraphViz installed through macports 

In this project, I wrote four functions to accomplish the task: 
    step1_fetch_top_100_movies()
    step2_extract_movie_info()
    step3_get_metadata_using_omdb()
    step4_select_top5_actors()
The code is found in mycode.py
