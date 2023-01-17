#read the coordinates from a file.
#each line of the file contains: 0 or 1 , lat, lon
#first value is zero if no materials have been detected and 1 if any of the listed material has been detected
#in this particular application, 0 is no plastic detected and 1 is plastic detected

import folium
from folium.plugins import MarkerCluster
import csv
from selenium import webdriver
import time

layerControl = 0
x = "C:\plotcoordinates\my_map.html"
refreshrate = 8
results = []
try:
    with open("C:\\plotcoordinates\\coordinates.txt") as f:
        firstline = f.readline().rstrip()
        c = firstline.split(',')
        lat = float(c[1])
        lon = float(c[2])
    print(firstline)


    m = folium.Map(location=[lat, lon], zoom_start=19)
    # Aggiungo i due cluster (plastica e non) alla mappa
    PlasticaCluster = MarkerCluster(name="Plastica", maxClusterRadius=0.00000001).add_to(m)
    NoPlasticaCluster = MarkerCluster(name="No-Plastica", maxClusterRadius=0.00000001).add_to(m)
    m.save(x)  # salvo la mappa

    #Commentare le prossime due righe se si vuole disattivare l'aggiornamento automatico (commentare anche un altra riga sotto)
    driver = webdriver.Firefox()            #allorazione del webdriver per il refresh automatico.
    driver.get(x)                           #prende la mappa e la aggiorna in automatico.

    while True:
        N = len(results)
        csvfile = open("C:\plotcoordinates\coordinates.txt", 'r')
        reader = csv.reader(csvfile.readlines()[N:])  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)
        print(results)
        csvfile.close()

        if len(results) > 0:
            for cords in results[N:]:

                #here starts the validation: for each line the 3 values are being validated
                if len(cords) == 3:
                    if cords[0].isdigit():
                        contadigits = 0
                        for c in cords[1]:
                            if c.isdigit():
                                contadigits += 1
                        contapunti = cords[1].count(".")
                        if contapunti + contadigits == len(cords[1]):
                            contadigits = 0
                            for c in cords[2]:
                                if c.isdigit():
                                    contadigits += 1
                            contapunti = cords[2].count(".")
                            if contapunti + contadigits == len(cords[2]):
                                if float(cords[1]) >= -90 and float(cords[1]) <= 90 and float(cords[2]) >= -180 and float(cords[2]) <= 180:
                                    if int(cords[0]) == 1:
                                        folium.CircleMarker(location=[cords[1], cords[2]], radius=3,
                                                            popup="{0},{1}".format(cords[1], cords[2]),
                                                            color="red", icon=folium.Icon(icon_color='red')).add_to(PlasticaCluster)
                                    elif int(cords[0]) == 0:
                                        folium.CircleMarker(location=[cords[1], cords[2]], radius=3,
                                                            popup="{0},{1}".format(cords[1], cords[2]),
                                                            color="green", icon=folium.Icon(icon_color='green')).add_to(NoPlasticaCluster)
                                    else:
                                        print("coordinates discarded")
                                else:
                                    print("coordinates discarded")
                            else: print("coordinates discarded")
                        else: print("coordinates discarded")

                    else:
                        print("coordinates discarded")
                else:
                    print("coordinates discarded")

        # Aggiungo il controlLayer alla mappa
        if (layerControl == 0):
            folium.LayerControl().add_to(m)
            layerControl = 1
        m.location = [cords[1], cords[2]]
        #m.fit_bounds(m.get_bounds(), padding=(30, 30))
        m.save(x)



        time.sleep(refreshrate)


        driver.refresh()    # refresh page automatico. commentare questa riga per disattivarlo (commentare anche altre due righe sopra)
except FileNotFoundError:
    print("File Not Found")