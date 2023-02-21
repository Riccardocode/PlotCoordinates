#read the coordinates from a file.
#each line of the file contains: 0 or 1 , lat, lon
#first value is zero if no materials have been detected and 1 if any of the listed material has been detected
#in this particular application, 0 is no plastic detected and 1 is plastic detected

import folium
from folium.plugins import MarkerCluster
import csv
from selenium import webdriver
import time

lat = 41.89
lon = 12.49
firstline=""
layerControl = 0
x = "C:\plotcoordinates\my_map.html"
refreshrate = 5
results = []
loadedCoords=[]
num_plastic=0
num_noPlastic=0
coordRepeated =0
#when IMU does not connect to GPS, it send the 0,0,0 coordinate
#zeroCoordinate flag is used to detect and remove the 0,0,0 coordinate
zeroCoordinate=0
try:
    with open("C:\\plotcoordinates\\coordinates.txt") as f:
        firstline = f.readline().rstrip()
        if(firstline!=""):
            c = firstline.split(',')
            lat = float(c[1])
            lon = float(c[2])
    print("Map initialized!")


    m = folium.Map(location=[lat, lon], zoom_start=19)
    # Aggiungo i due cluster (plastica e non) alla mappa


    NoPlasticaCluster = MarkerCluster(name="No-Plastica", maxClusterRadius=0.00000001, overlay=lambda zoom: zoom <= 18).add_to(m)
    PlasticaCluster = MarkerCluster(name="Plastica", maxClusterRadius=0.00000001, overlay=lambda zoom: zoom <= 18 ).add_to(m)

    # PlasticaCluster = MarkerCluster(name="Plastica", overlay=lambda zoom: zoom >= 17, radius=0.00000000001).add_to(m)
    # NoPlasticaCluster = MarkerCluster(name="No-Plastica", overlay=lambda zoom: zoom >= 17, radius=0.00000000001).add_to(m)
    m.save(x)  # salvo la mappa

    #Commentare le prossime due righe se si vuole disattivare l'aggiornamento automatico
    # (commentare anche un altra riga sotto)
    driver = webdriver.Firefox()            #allorazione del webdriver per il refresh automatico.
    driver.get(x)                           #prende la mappa e la aggiorna in automatico.

    while True:
        N = len(results)
        csvfile = open("C:\plotcoordinates\coordinates.txt", 'r')
        reader = csv.reader(csvfile.readlines()[N:])  # change contents to floats
        for row in reader:  # each row is a list
            if((row!="") or (row!="/n")):
                results.append(row)
        #print(results)
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
                                if float(cords[1]) >= -90 and float(cords[1]) <= 90 and \
                                        float(cords[2]) >= -180 and float(cords[2]) <= 180:
                                    coordRepeated = 0
                                    zeroCoordinate = 0
                                    #verifico che lat e lon non siano 0 (Imu usa coord 0 quando non si connette al GPS)
                                    if cords[1] == '0' and cords[2] == '0':
                                        zeroCoordinate=1
                                        print("Zero coordinate has been discarded: " + cords[0] + ',' + cords[1] + ',' +cords[2])
                                    #confronto che le coordinate non siano state gia' caricate nella mappa
                                    #per evitare la formazione di cluster.
                                    if len(loadedCoords) > 0 and zeroCoordinate == 0:
                                        for loadCoord in loadedCoords:
                                            if loadCoord[0] == cords[0] and loadCoord[1] == cords[1] and loadCoord[2] == cords[2]:
                                                coordRepeated = 1
                                                print("duplicated coordinates: " + cords[0] + ',' + cords[1] + ',' + cords[2])
                                    if zeroCoordinate == 0 and coordRepeated == 0 and int(cords[0]) == 1:
                                        num_plastic += 1
                                        folium.CircleMarker(location=[cords[1], cords[2]], radius=2,
                                                            popup="{0},{1}".format(cords[1], cords[2]),
                                                            color="red",
                                                            icon=folium.Icon(icon_color='red')).add_to(PlasticaCluster)
                                        loadedCoords.append([cords[0], cords[1], cords[2]])
                                    elif zeroCoordinate == 0 and coordRepeated == 0 and int(cords[0]) == 0:
                                        num_noPlastic+=1
                                        folium.CircleMarker(location=[cords[1], cords[2]], radius=2,
                                                            popup="{0},{1}".format(cords[1], cords[2]),
                                                            color="green",
                                                            icon=folium.Icon(icon_color='green')).\
                                                            add_to(NoPlasticaCluster)
                                        loadedCoords.append([cords[0], cords[1], cords[2]])


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
            print("Number of plastic is: ", num_plastic, "out of ", num_plastic+num_noPlastic, " coordinates processed")



        time.sleep(refreshrate)

        # refresh page automatico. commentare questa riga per disattivarlo (commentare anche altre due righe sopra)
        driver.refresh()
except FileNotFoundError:
    print("File Not Found")