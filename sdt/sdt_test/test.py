import requests

r = requests.get('http://esgf-node.ipsl.upmc.fr/esg-search/search?source_id=NorESM2-LM&grid_label=gn&type=File&limit=5&'
                 'fields=*&format=application%2Fsolr%2Bxml&offset=0',
                 verify=True, timeout=300)
print(r)
print(r.text)
