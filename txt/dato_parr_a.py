# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

class DatosParrA():
    def __init__(self, archT):#, archTP, archTC1, archTC2, archTC3, archTC4):
        cant = int.from_bytes(archT[0:1], "little")
        #self.cantN = cant
        self.DatoParrA = {}
        cont   = 32
        contT  = 0
        contS  = 0
        contTD = 0
        stado = False
        for i in range(cant):
            parrA = archT[cont:cont+64]
            inTex = int.from_bytes(parrA[0:4], "little")*4
            inPal = int.from_bytes(parrA[4:8], "little")*4
            tamTex = int.from_bytes(parrA[8:12], "little")#*4
            tamPal = int.from_bytes(parrA[12:16], "little")
            color = (tamPal-128)//4   #tam pal == a 192 si es de 16 colores restamos relleno queda 64 bytes dividido 4 nos da la cantidad de colores
            posParA = int.from_bytes(parrA[36:40], "little")
            if parrA[12:16] == b'\x00\x00\x00\x00':
                #print(f"Sombra {i} inTex {inTex}")
                name = f"Sombra {contS+1}"
                stado = True
                #self.listWidgetSmbs.addItem(f"{name}")
                self.DatoParrA[f"inicioS {contS+1}"] = inTex
                self.DatoParrA[f"finS {contS+1}"] = inTex + tamTex + tamPal #//4##mmm
                self.DatoParrA[f"colorS {contS+1}"] = 256 ###
                self.DatoParrA[f"inParrAS {contS+1}"] = contS
                contS += 1
                #print(f"inTex {inTex} tamTex {tamTex} tamPal {tamPal}")
            elif parrA[12:16] != b'\x00\x00\x00\x00' and stado == False:
                #print(f"Textura {i} inicioT {inTex}")
                name = f"Textura {contT}"
                #self.listWidgetTex.addItem(f"{name}")
                self.DatoParrA[f"inicioT {contT}"] = inTex
                self.DatoParrA[f"inicioP {contT}"] = inPal
                self.DatoParrA[f"finP {contT}"] = inPal + tamPal
                self.DatoParrA[f"tamTex {contT}"] = tamTex
                self.DatoParrA[f"tamPal {contT}"] = tamPal
                self.DatoParrA[f"colorT {contT}"] = color ###
                self.DatoParrA[f"inParrAT {contT}"] = contT

                self.DatoParrA[f"posParA {contT}"] = posParA

                contT += 1
            else:
                #print(f"Tex duplicada {i} inicioTD {inTex}")
                name = f"Textura duplicada {contTD+1}"
                #self.listWidgetTexDupl.addItem(f"{name}")
                self.DatoParrA[f"inicioTD {contTD+1}"] = inTex
                self.DatoParrA[f"inicioPD {contTD+1}"] = inPal
                self.DatoParrA[f"finPD {contTD+1}"] = inPal + tamPal
                self.DatoParrA[f"tamTexD {contTD+1}"] = tamTex
                self.DatoParrA[f"tamPalD {contTD+1}"] = tamPal
                self.DatoParrA[f"colorTD {contTD+1}"] = color ###
                self.DatoParrA[f"inParrATD {contTD+1}"] = contTD

                self.DatoParrA[f"posParAD {contTD+1}"] = posParA

                contTD += 1
            cont += 64
        
        self.DatoParrA[f"cantT"] = contT
        self.DatoParrA[f"cantS"] = contS
        self.DatoParrA[f"cantTD"] = contTD
        

        