# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

class DataId():
    def __init__(self, archT):
        cantText = int.from_bytes(archT[12:14], "little")
        #print(f"cant text Data id {cantText}")
        self.listId1txt = []
        cont = 32
        idcont = 5
        for i in range(cantText):
            #iteramos por cada parrA
            parrA = archT[cont:cont+64]
            #tipo paleta 16 o 256 colores actual
            tipoPal = int.from_bytes(parrA[12:16], 'little')
            #offset inicio textura actual
            OffsetIn = int.from_bytes(parrA[0:4], 'little')*4
            #condicionale para cada tipo de paleta
            if tipoPal == 192:#16 colores
                tamTxtV = int.from_bytes(archT[OffsetIn+48:OffsetIn+52], 'little')*2
                tamTxtH = int.from_bytes(archT[OffsetIn+52:OffsetIn+56], 'little')*4
            else:#256 colores
                tamTxtV = int.from_bytes(archT[OffsetIn+48:OffsetIn+52], 'little')*2
                tamTxtH = int.from_bytes(archT[OffsetIn+52:OffsetIn+56], 'little')*2
            
            #sumar para obtener las ids
            idValue1 = int.from_bytes(parrA[32:36], 'little')
            idValue2 = int.from_bytes(parrA[48:52], 'little')
            suma = idValue1+idValue2
            res = (suma).to_bytes(4, byteorder='little')
            idValue = res.hex().upper()
           
            if tamTxtV <= 256 and tamTxtH <= 128 and tipoPal == 192:
                Id3 = (idcont+536870912).to_bytes(4, byteorder='little').hex().upper()
                #print("igual a 128x128 o inferior, 16 col")
            elif tipoPal == 192:
                #print("mayor a 128x128,16 col")
                Id3 = (idcont+536870912+1).to_bytes(4, byteorder='little').hex().upper()
            #-4 de 256 colores
            elif tamTxtV == 64 and tamTxtH == 64 or tamTxtV == 128 and tamTxtH == 128 or tamTxtV == 256 and tamTxtH == 128 or tamTxtV == 512 and tamTxtH == 128 and tipoPal == 1152:
                Id3 = (idcont+536870912 -4).to_bytes(4, byteorder='little').hex().upper()
                #print("256 colores se resta 4")
            #-3 de 256 colores
            else:
                Id3 = (idcont+536870912 -3).to_bytes(4, byteorder='little').hex().upper()
                #print("256 colores se resta 3")

            ### Nuevo Parametro para saltar 4 espacios de color por las tex de 256 ###
            if tipoPal == 1152:
                idcont += 96 #128 como abajo sumamos 32 deja de ser 128 a 96 ("128-32 = 96")


            #self.listId2txt.append(self.Id3)
            self.listId1txt.append(f"{idValue}{Id3}")

            cont += 64
            idcont += 32
