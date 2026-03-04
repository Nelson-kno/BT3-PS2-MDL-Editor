# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

class DataFile:
    def __init__(self,uvs,cont,state):
        lista = []
        tex = b''
        index = 0
        for i in range(4):# pasamos por las 4 columnas
            texInt = b''
            listaInt = []################################################################################
            for j in range(8):# extraemos los bytes de cada columna saltando 8 bytes
                #print(f"jota {j} index {index}")
                texInt += uvs[index+cont:index+cont+1]
                #print(f"test: {index+cont}")
                listaInt.append(index+cont)#################################################################
                index += 8
            index = 0
            index += (2*(i+1)) # 2 4 6
            if state == True:#metodo de invertir
                sep = len(texInt)//2
                texInt = texInt[4:8] + texInt[0:4]
                #print(listaInt)#########################
                #print(listaInt[4:8]+listaInt[0:4])
                listaInt = listaInt[4:8]+listaInt[0:4]
            lista.append(state)###############################################  
            lista.append(listaInt)
            tex += texInt#agregar columa de tex
        #print(len(tex))
        #print(lista)
        #return tex
        self.tex = tex