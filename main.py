from vale import predict
from math import degrees
import numpy as np
import pandas as pd

pd.set_option('display.float_format', '{:.10f}'.format)

poset = []
with open("kayit.txt", "r") as dosya:
    icerik = dosya.read()
parcalar = icerik.split("AHRS2")

for i in parcalar[1:]:
    altparca = i.split(":")
    poset.append(altparca[1].split(",")[0])
    poset.append(altparca[2].split(",")[0])
    poset.append(altparca[3].split(",")[0])
    poset.append(altparca[4].split(",")[0])
    poset.append(altparca[5].split(",")[0])
    poset.append(altparca[6])
    


temiz_liste = [s.replace("}", "").replace(" ", "") for s in poset]

arr = np.array(temiz_liste)
arr = arr.reshape(223,6).astype(float)

for i in range(223):
    arr[i][0] = degrees(arr[i][0])
    arr[i][1] = degrees(arr[i][1])
    arr[i][4] = float(arr[i][4]) / 10**7 
    arr[i][5] = float(arr[i][5]) / 10**7
    
hatalar = [] #hata_enlem, hata_boylam, hata_irtifa
for i in range(223):
    index = i
    yatis = arr[index][0] 
    dikilme = arr[index][1] 
    yonelme = arr[index][2] 
    irtifa = arr[index][3] 
    enlem = arr[index][4] 
    boylam = arr[index][5] 



    y_enlem, y_boylam, y_irtifa = predict(enlem, boylam, irtifa, dikilme, yonelme, yatis, 10, zaman=0.75)
    #print("gerçek enlem:",arr[index+1][4],"gerçek boylam:",arr[index+1][5],"gerçek irtifa:",arr[index+1][3] )
    #print("tahmin enlem:",y_enlem,"tahmin boylam:",y_boylam,"tahmin irtifa:",irtifa)
    try:
        hatalar.append(abs(y_enlem-arr[index+1][4]))
        hatalar.append(abs(y_boylam-arr[index+1][5]))
        hatalar.append(abs(y_irtifa-arr[index+1][3]))
    except IndexError:
        pass
arr2 = np.array(hatalar).reshape(222,3)

df = pd.DataFrame(arr2, columns=['enlem_hata', 'boylam_hata', 'irtifa_hata'])
print(df.head(3))
print(df.describe())
