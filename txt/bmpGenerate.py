# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

class BmpGenerate:
    def __init__(self,tamTex,tamH,tamV,pal):      
        self.data = self.parrBmp(tamTex,tamH,tamV,self.paleta_txs(pal))

    def parrBmp(self,tamTex,tamH,tamV,pal):
        #print(tamTex+1074)
        #Dato Bmp
        typeBMP        = b'BM'                                            #(2 byte) Tipo de archivo 'BM' |ASCII
        tamBmp         = (tamTex + 1078).to_bytes(4, byteorder='little')  #(4 byte) Tamaño del archivo BMP |UNSIGNED INT
        reservado1     = b'\x00\x00'                                      #(2 byte) Reservado1 Todo ceros |BYTES
        reservado2     = b'\x00\x00'                                      #(2 byte) Reservado2 Todo ceros |BYTES
        comTexBMP      = (1078).to_bytes(4, byteorder='little')           #(4 byte) Comienzo mapa de bits(tex) |UNSIGNED INT
        #Parrafo 1 BMP
        tamParrSig     = (40).to_bytes(4, byteorder='little')             #(4 byte) #Numero de bytes que ocupa esta estructura (el parrafo 1)|UNSIGNED INT
        anchoBMP       = (tamH).to_bytes(4, byteorder='little')           #(4 byte) #tamaño Horizontal Textura |UNSIGNED INT
        altoBMP        = (tamV).to_bytes(4, byteorder='little')           #(4 byte) #tamaño Vertical Textura |UNSIGNED INT
        planosBMP      = b'\x01\x00'                                      #(2 byte) Numero de planos de color (siempre 1) |UNSIGNED INT
        saltoBytesBMP  =	b'\x08\x00'                                   #(2 byte)	Bits por pixel (1,4,8,24) |UNSIGNED Short
        comprencionBmp = b'\x00\x00\x00\x00'                              #(4 byte) comprension utilizada (=0)Sin comprencion,(=1)comprension RLE4,(=2)Comprencion RLE8 |UNSIGNED INT
        tamTexBmp      = (tamTex).to_bytes(4, byteorder='little')         #(4 byte) tamaño tex en bytes |UNSIGNED INT
        resXpixel      = b'\xd4\x0e\x00\x00'                              #(4 byte) Pixels por metro. Resolución horizontal |UNSIGNED INT
        resYpixel      = b'\xd4\x0e\x00\x00'                              #(4 byte) Pixels por metro. Resolución vertical |UNSIGNED INT
        numIndCol      = b'\x00\x01\x00\x00'                              #(4 byte) Número de índides de color utilizados. |Si biBitCount=24 no importa |UNSIGNED INT
        importCol      = b'\x10\x00\x00\x00'                              #(4 byte) Colores importantes (=0 todos) |UNSIGNED INT
        #Parrafo 2 BMP Relleno
        if len(pal) == 64:
            #print("16 colores")
            relleno = b'\x00\x00\x00\xff'                                 #(960 byte) Relleno de 960 bytes repetidos |BYTES
            for i in range(239):
                relleno += b'\x00\x00\x00\xff'
        else:
            relleno = b''
        parr = typeBMP+tamBmp+reservado1+reservado2+comTexBMP+tamParrSig+anchoBMP+altoBMP+planosBMP+saltoBytesBMP+comprencionBmp+tamTexBmp+resXpixel+resYpixel+numIndCol+importCol+pal+relleno
        #print(bytes.fromhex('000000FF'))
        return parr

        # Referencia técnica para la construcción del encabezado BMP:
        # Fuente: Universidad de Valladolid (UVA)
        # URL: https://www.ele.uva.es/~jesman/BigSeti/seti1/PRACTICAS/PE20012002/BMP_prac.txt
        
    def paleta_txs(self,dato):
        if len(dato) == 64:
            #print("16 colores")
            palBytes = self.color_16(dato)
        else:
            #print("256 colores")
            palBytes = self.color_256(dato)
        return palBytes

    def color_16(self,dato): #conversion paleta 16 colores ps2 a bmp
        palList = []
        cont = 0
        for i in range(16):
            inv = dato[cont+2:cont+3]+dato[cont+1:cont+2]+dato[cont:cont+1]+dato[cont+3:cont+4]
            palList.append(inv)
            cont += 4

        palBytes = b''.join(palList)
        return palBytes
    def color_256(self,dato): #conversion paleta 256 colores ps2 a bmp
        def pal(cont,cant,dato):
            cont = cont
            byts = b''
            lista = []
            for i in range(cant):
                #lista += [cont+2,cont+1,cont,cont+3]
                byts += dato[cont+2:cont+3]+dato[cont+1:cont+2]+dato[cont:cont+1]+dato[cont+3:cont+4]
                cont += 4
            #print(lista)
            return byts
            
        palList = b''
        cont = 0
        for ii in range(4):
            for i in range(7):
                #print(cont)
                if i in [0,2,5]:
                    palList += pal(cont,8,dato)
                    cont += 64
                elif i in [1,4]:
                    palList += pal(cont,8,dato)
                    cont -= 32
                elif i == 3:
                    palList += pal(cont,16,dato)
                    cont += 96
                elif i == 6:
                    palList += pal(cont,8,dato)
                    cont += 32
        return palList