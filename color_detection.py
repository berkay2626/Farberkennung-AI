import cv2
import numpy as np
import pandas as pd
import argparse

#EIN BILD VOM NUTZER BEKOMMEN
'''
VERWENDUNG VON Argparse-Bibliothek, um einen Argument-parser zu erstellen
Wir können direkt an der Eingabeaufforderung einen Bildpfad angeben
'''
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Lesen des Bildes mit opencv
img = cv2.imread(img_path)

#deklarieren von variablen (koordinaten durch maus klick)
clicked = False
r = g = b = xpos = ypos = 0


#LESEN DES CSV file's MIT PANDAS + NAMEN GEBEN FÜR JEDE SPALTE
'''
Die Pandas-Bibliothek ist sehr nützlich, wenn wir verschiedene Operationen
an Datendateien wie CSV (Comma-Seperated Values) ausführen müssen. pd.read_csv()
liest die CSV-Datei und lädt sie in den Pandas DataFrame.
Wir haben jeder Spalte einen Namen für den einfachen Zugriff zugewiesen.
'''
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#Berechnen der Entfernung, um den Farbnamen zu erhalten
#Funktion zur Berechnung des Mindestabstands zu allen Farben
#und zur Ermittlung der am besten passenden Farbe
'''
Wir haben die Werte r, g und b.
Jetzt benötigen wir eine weitere Funktion
die uns den Farbnamen aus den RGB-Werten zurückgibt.
Um den Farbnamen zu erhalten, berechnen wir einen Abstand (d)
der uns sagt wie nah wir an der Farbe sind
und wählen den mit dem Mindestabstand aus.

Die Entfernung wird nach folgender Formel berechnet:
d = abs (Rot - ithRedColor) + (Grün - ithGreenColor) + (Blau - ithBlueColor)
'''
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#funktion um x,y koordinaten von maus doppel klick zu bekommen
'''
Es werden die RGB-Werte des Pixels berechnet,
auf das wir doppelklicken. Die Funktionsparameter haben den Ereignisnamen
(x, y) -Koordinaten der Mausposition usw. In der Funktion prüfen wir,
ob das Ereignis doppelklickt, berechnen und
setzen die Werte für r, g, b zusammen mit x, y Positionen der Maus.
'''
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Ein Maus-Rückrufereignis in einem Fenster festlegen
'''
Zuerst haben wir ein Fenster erstellt,
in dem das Eingabebild angezeigt wird.
Dann setzen wir eine Rückruffunktion,
die aufgerufen wird, wenn ein Mausereignis eintritt.
'''
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)
'''
Mit diesen Zeilen haben wir unser Fenster als "Bild" bezeichnet
und eine Rückruffunktion festgelegt, die die draw_function () aufruft,
wenn ein Mausereignis auftritt.
'''

#DAS BILD IM FENSTER ANZEIGEN
'''
Jedes Mal, wenn ein Doppelklickereignis auftritt,
werden der Farbname und die RGB-Werte im Fenster aktualisiert.
Mit der Funktion cv2.imshow () zeichnen wir das Bild in das Fenster.
Wenn der Benutzer auf das Fenster doppelklickt,
zeichnen wir ein Rechteck und erhalten den Farbnamen,
um mit den Funktionen cv2.rectangle und cv2.putText ()
Text in das Fenster zu zeichnen.
'''
while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #erstellen eines text string um (Name der Farbe + RGB-Farbmodell werte) anzuzeigen
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #für sehr helle farben wird der text in einer schwarzen farbe angezeigt
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #den loop unterbrechen wenn der nutzer 'esc' drückt
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
