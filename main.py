import folium
from folium.plugins import MarkerCluster
import csv
from selenium import webdriver
import time
import urllib

layerControl = 0
x = "C:\plotcoordinates\my_map.html"
refreshrate = 10
results = []
lat = 41.93368114  # TODO: put general coordinates (magari dal primo elemento del file; gestire errore se non ci sono elementi)
lon = 12.53232093
m = folium.Map(location=[lat, lon], zoom_start=12)
# Aggiungo i due cluster (plastica e non) alla mappa
PlasticaCluster = MarkerCluster(name="Plastica").add_to(m)
NoPlasticaCluster = MarkerCluster(name="No-Plastica").add_to(m)
m.save(x)  # salvo la mappa prima di impostare selenium

driver = webdriver.Firefox()
driver.get(x)

# TODO:  1. Leggo il file nuovamnete da zero? o posso leggere solo i nuovi elementi?
# TODO:  2. Se leggo nuovamente tutto il file, devo resettare il vettore result ad ogni iterazione
while True:
    N = len(results)
    csvfile = open("C:\plotcoordinates\coordinates.txt", 'r')
    # for line in (csvfile.readlines()[N:]):
    # print(line)
    # results.append(line)
    reader = csv.reader(csvfile.readlines()[N:], quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
    for row in reader:  # each row is a list
        results.append(row)
    print(results)
    csvfile.close()

    if len(results) > 0:
        for cords in results[N:]:
            if cords[0] == 1.0:
                folium.CircleMarker(location=[cords[1], cords[2]], radius=3, popup="{0},{1}".format(cords[1], cords[2]),
                                    color="red", icon=folium.Icon(icon_color='red')).add_to(PlasticaCluster)
            else:
                folium.CircleMarker(location=[cords[1], cords[2]], radius=3, popup="{0},{1}".format(cords[1], cords[2]),
                                    color="green", icon=folium.Icon(icon_color='green')).add_to(NoPlasticaCluster)

    # Aggiungo il controlLayer alla mappa
    if (layerControl == 0):
        folium.LayerControl().add_to(m)
        layerControl=1
    m.save(x)
    # results.clear()
    # Refresh time with Selenium
    time.sleep(refreshrate)
    driver.refresh()

# TODO: da ottimizzare la gestioner dell'array results.
# Invece di cancellare tutti gli elementi, bisogna mantenerli ed aggiungere solo quelli nuovi dal file
# si dovrebbe accedere solamente ai nuovi elementi del file in modo da risparmiare memoria e CPU clocks
