# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from txt.orderTex16 import *
from txt.dato_parr_a import *
class ExportarBmp():
    def __init__(self,url, url2):
        print(url)
        print(url2)
        #print(url2.split("/"))
        nameT = url2.split("/")
        nameT = url2.replace(f"{nameT[-1]}","")
        #print(url2.replace(f"{name[-1]}",""))
        name = url.replace("Mdl.mdl","Tex.dbt")
        with open(f"{name}","rb+") as f:
            file = f.read()
            f.close()

        objParrA = DatosParrA(file)

        #cantText = int.from_bytes(file[12:14], "little")
        #print(f"cantidad de txt: {cantText}")

        self.listId1txt = []
        cont = 32
        idcont = 5
        for i in range(objParrA.DatoParrA[f"cantT"]):
            parrA = file[cont:cont+64]
            OffsetIn = int.from_bytes(parrA[0:4], 'little')*4
            tamTxtV = int.from_bytes(file[OffsetIn+48:OffsetIn+52], 'little')*2
            tamTxtH = int.from_bytes(file[OffsetIn+52:OffsetIn+56], 'little')*4
            #sumar para obtener las ids
            idValue1 = int.from_bytes(parrA[32:36], 'little')
            idValue2 = int.from_bytes(parrA[48:52], 'little')
            suma = idValue1+idValue2
            res = (suma).to_bytes(4, byteorder='little')
            idValue = res.hex().upper()

            if tamTxtV <= 256 and tamTxtH <= 128:
                Id3 = (idcont+536870912).to_bytes(4, byteorder='little').hex().upper()
                #print("igual a 128x128")
            else:
                #print("mayor a 128x128")
                Id3 = (idcont+536870912+1).to_bytes(4, byteorder='little').hex().upper()

            self.listId1txt.append(f"{idValue}{Id3}")

            cont += 64
            idcont += 32
        #print(objParrA.DatoParrA[f'inicioT {1}'])
        print(file[0:16].hex())
        for t in range(len(self.listId1txt)):
           self.test(objParrA, nameT, t, file)
    
    def test(self, objParrA, nameT, t, file):
        print(f"nameT: {nameT} t: {t}")
        print(f"{nameT}{self.listId1txt[t]}.bmp")
        #Escribir Bmp
        img = OrderTex16col(file[objParrA.DatoParrA[f'inicioT {t+1}']:objParrA.DatoParrA[f'inicioP {t+1}']], file[objParrA.DatoParrA[f'inicioP {t+1}']:objParrA.DatoParrA[f'finP {t+1}']])
        with open(f'{nameT}{self.listId1txt[t]}.bmp', 'wb+') as file:
            file.write(img.texBmp)
            file.close()
