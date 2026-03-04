# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from txt.bmpGenerate import *
from txt.order import *
class OrderTex16col():
    def __init__(self,tex,paleta) -> None:
        
        texHor = int.from_bytes(tex[48:52], 'little')*2 #tamaño de tex Horizontal
        texVer = int.from_bytes(tex[52:56], 'little')*4 #tamaño de tex Vertical
        sinParr = tex[96:len(tex)-32] #sacando exedente solo tex
        paleta = paleta[96:-32]
        #with open("nuevaAppArch.unk","wb+") as f:
        #    f.write(sinParr)
        hx = sinParr.hex() #conversion a Hexadecimal
        bytescn0 = []
        for i in hx:
            #Agregar 0 a la izq y pasarlo a la lisca contenedor
            byt = bytes.fromhex(f'{0}{i}')  
            bytescn0.append(byt)

        bytesConCero = b''.join(bytescn0)

        a = self.tim_to_bmp(texHor,texVer,bytesConCero)

        Objdata = BmpGenerate(len(bytescn0),texHor,texVer,paleta)
        self.texBmp = Objdata.data+a #data de header + data de tex
        self.texHor = texHor
        self.texVer = texVer
        #with open('texGenerada2.bmp', 'wb+') as file:
        #    file.write(Objdata.data+a)

    def test(self,filaRepeat,filaEnt,espacio,alist,uvs):
        alistint = []
        alistintInv = []###
        for i in alist:
            alistint.append(i)
            alistintInv.append(i+1)###

        #print(f"lista def {alist}")
        tex = b''
        cont = 0
        cont2 = 0
        contB = 0
        for k in range(8):# iteramos por la columna 2 por el entrelazado entre la 1na y 2da
            if contB <= 1:
                state = False
            elif contB == 2 or contB == 3:
                state = True
                if contB == 3:
                    contB = -1
            contB += 1
            for iN in range(len(alistint)):
                cont += 1
                #extraer Bytes####
                objTex = DataFile(uvs,alistint[cont-1]-64,state)
                tex += objTex.tex#extraer Bytes####

                alistint[cont-1] = alistint[cont-1]-espacio
                if cont == len(alistint):
                    cont = 0
            #extra repetido para invertido
            if k %2 == 0:
                pass
            else:
                if state == True:
                    state2 = False
                else:
                    state2 = True
                #print(f"######## state2 {state2}")
                for iN in range(len(alistintInv)):
                    cont2 += 1
                    objTex = DataFile(uvs,alistintInv[cont2-1]-64,state2)#extraer Bytes####
                    tex += objTex.tex#extraer Bytes####
                    #print(f"funcion inv: {alistintInv[cont2-1]-64}")
                    alistintInv[cont2-1] = alistintInv[cont2-1]-espacio
                    if cont2 == len(alistintInv):
                        cont2 = 0
                    cont2 += 1
                    objTex = DataFile(uvs,alistintInv[cont2-1]-64,state2)#extraer Bytes####
                    tex += objTex.tex#extraer Bytes####
                    #print(f"funcion inv: {alistintInv[cont2-1]-64}")
                    alistintInv[cont2-1] = alistintInv[cont2-1]-espacio
                    if cont2 == len(alistintInv):
                        cont2 = 0
        return tex
            
    def tim_to_bmp(self,texHor,texVer,uvs):
        size = len(uvs)
        filaEnt = texHor // 16 #tex//16 "fila entrelazado"
        filaRepeat = (size//512)//filaEnt #size//512//filaEnt "fila Repeat"
        espacio = 64 * filaEnt
        newpatron = size//filaRepeat
        #print(f"tex med: H {texHor} x V {texVer}")
        #print(f"size {size}")
        #print(f"filaEnt {filaEnt} filaRepeat {filaRepeat} espacio {espacio} newpatron {newpatron}")

        tex = b''
        inn = size#newpatron
        alist = []

        offset = size
        for j in range((texHor//32)):#128x256
            
            if j%4 == 0:
                if j == 0:
                    pass
                else:
                    #print(f"lol {j} {inn + 24064+newpatron} offset {offset}")
                    offset -= 512
                    inn = offset
                    #inn += 24064+newpatron
            alist.insert(0,inn)
            inn -= newpatron

        #new var
        if texVer//128 == 0:
            vueltas = 1
        else:
            vueltas = texVer//128
        cont = alist[-1]//vueltas
        #print(f"alist {alist}")
        #print(f"cont {cont}")
        for i in range(vueltas):
            #print(f"listaaa {alist}")
            listaInt = alist[:]
            for j in range(8):####
                #print(f"alistNew {j+1} {listaInt}")
                tex += self.test(filaRepeat,filaEnt,espacio,listaInt,uvs)
                for ii in range(len(listaInt)):
                    listaInt[ii] = listaInt[ii]-64####"""
            for k in range(len(alist)):
                alist[k] = alist[k]-cont

        return tex

