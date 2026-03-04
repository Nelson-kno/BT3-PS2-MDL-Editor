# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import shutil
from PySide2.QtCore import QCoreApplication

# Lista de 252 archivos
nameList = ["Huds.dbt",
                    "Colision.pmdl","Pmdl.pmdl","Face1.pmdf","Face2.pmdf","Face3.pmdf","Face4.pmdf","Face5.pmdf","Face6.pmdf","Face7.pmdf","Face8.pmdf",
                    "Tex.dbt","TexExtra.dbt",
                    "TexCara5.dbt","TexCara6.dbt","TexCara7.dbt","TexCara8.dbt",
                    "ParBasicos.dat","ParGolpes.dat","ParKiBlast.dat","ParMovimientos.dat",
                    "ParVoz.dat","ParExtraAnimacion.dat","ParExplocion2.dat","ParExplocion1.dat","ParExplocion0.dat",
                    "ParDesconocido.dat","ParCamaras.dat",
                    "PjApoyo1.anm","PjApoyo2.anm","PjApoyo3.anm","PjApoyo4.anm",
                    "PjMetamoruFusion.anm","PjPotaraFusion.anm","PjResultFusion.anm",
                    "PjPoseCr.anm",
                    "PjEspecial1.cman","PjEspecial2.cman","PjEspecial3.cman","PjEspecial4.cman",
                    "PjIntro.cman","PjGanador.cman","PjPerdedor.cman",
                    "PjTxtJaponesp.txt","PjTxtIngles.txt","PjTxtVacio.txt","PjTxtUcrania.txt","PjTxtEspañol.txt","PjTxtAleman.txt","PjTxtFrances.txt","PjTxtItaliano.txt","PjTxtCoreano.txt",
                    "PjAudioJp1.lps","PjAudioJp2.lps","PjAudioJp3.lps","PjAudioJp4.lps","PjAudioJp5.lps","PjAudioJp6.lps","PjAudioJp7.lps","PjAudioJp8.lps","PjAudioJp9.lps","PjAudioJp10.lps",
                    "PjAudioJp11.lps","PjAudioJp12.lps","PjAudioJp13.lps","PjAudioJp14.lps","PjAudioJp15.lps","PjAudioJp16.lps","PjAudioJp17.lps","PjAudioJp18.lps","PjAudioJp19.lps","PjAudioJp20.lps",
                    "PjAudioJp21.lps","PjAudioJp22.lps","PjAudioJp23.lps","PjAudioJp24.lps","PjAudioJp25.lps","PjAudioJp26.lps","PjAudioJp27.lps","PjAudioJp28.lps","PjAudioJp29.lps","PjAudioJp30.lps",
                    "PjAudioJp31.lps","PjAudioJp32.lps","PjAudioJp33.lps","PjAudioJp34.lps","PjAudioJp35.lps","PjAudioJp36.lps","PjAudioJp37.lps","PjAudioJp38.lps","PjAudioJp39.lps","PjAudioJp40.lps",
                    "PjAudioJp41.lps","PjAudioJp42.lps","PjAudioJp43.lps","PjAudioJp44.lps","PjAudioJp45.lps","PjAudioJp46.lps","PjAudioJp47.lps","PjAudioJp48.lps","PjAudioJp49.lps","PjAudioJp50.lps",
                    "PjAudioJp51.lps","PjAudioJp52.lps","PjAudioJp53.lps","PjAudioJp54.lps","PjAudioJp55.lps","PjAudioJp56.lps","PjAudioJp57.lps","PjAudioJp58.lps","PjAudioJp59.lps","PjAudioJp60.lps",
                    "PjAudioJp61.lps","PjAudioJp62.lps","PjAudioJp63.lps","PjAudioJp64.lps","PjAudioJp65.lps","PjAudioJp66.lps","PjAudioJp67.lps","PjAudioJp68.lps","PjAudioJp69.lps","PjAudioJp70.lps",
                    "PjAudioJp71.lps","PjAudioJp72.lps","PjAudioJp73.lps","PjAudioJp74.lps","PjAudioJp75.lps","PjAudioJp76.lps","PjAudioJp77.lps","PjAudioJp78.lps","PjAudioJp79.lps","PjAudioJp80.lps",
                    "PjAudioJp81.lps","PjAudioJp82.lps","PjAudioJp83.lps","PjAudioJp84.lps","PjAudioJp85.lps","PjAudioJp86.lps","PjAudioJp87.lps","PjAudioJp88.lps","PjAudioJp89.lps","PjAudioJp90.lps",
                    "PjAudioJp91.lps","PjAudioJp92.lps","PjAudioJp93.lps","PjAudioJp94.lps","PjAudioJp95.lps","PjAudioJp96.lps","PjAudioJp97.lps","PjAudioJp98.lps","PjAudioJp99.lps","PjAudioJp100.lps",
                    "PjAudioEn1.lps","PjAudioEn2.lps","PjAudioEn3.lps","PjAudioEn4.lps","PjAudioEn5.lps","PjAudioEn6.lps","PjAudioEn7.lps","PjAudioEn8.lps","PjAudioEn9.lps","PjAudioEn10.lps",
                    "PjAudioEn11.lps","PjAudioEn12.lps","PjAudioEn13.lps","PjAudioEn14.lps","PjAudioEn15.lps","PjAudioEn16.lps","PjAudioEn17.lps","PjAudioEn18.lps","PjAudioEn19.lps","PjAudioEn20.lps",
                    "PjAudioEn21.lps","PjAudioEn22.lps","PjAudioEn23.lps","PjAudioEn24.lps","PjAudioEn25.lps","PjAudioEn26.lps","PjAudioEn27.lps","PjAudioEn28.lps","PjAudioEn29.lps","PjAudioEn30.lps",
                    "PjAudioEn31.lps","PjAudioEn32.lps","PjAudioEn33.lps","PjAudioEn34.lps","PjAudioEn35.lps","PjAudioEn36.lps","PjAudioEn37.lps","PjAudioEn38.lps","PjAudioEn39.lps","PjAudioEn40.lps",
                    "PjAudioEn41.lps","PjAudioEn42.lps","PjAudioEn43.lps","PjAudioEn44.lps","PjAudioEn45.lps","PjAudioEn46.lps","PjAudioEn47.lps","PjAudioEn48.lps","PjAudioEn49.lps","PjAudioEn50.lps",
                    "PjAudioEn51.lps","PjAudioEn52.lps","PjAudioEn53.lps","PjAudioEn54.lps","PjAudioEn55.lps","PjAudioEn56.lps","PjAudioEn57.lps","PjAudioEn58.lps","PjAudioEn59.lps","PjAudioEn60.lps",
                    "PjAudioEn61.lps","PjAudioEn62.lps","PjAudioEn63.lps","PjAudioEn64.lps","PjAudioEn65.lps","PjAudioEn66.lps","PjAudioEn67.lps","PjAudioEn68.lps","PjAudioEn69.lps","PjAudioEn70.lps",
                    "PjAudioEn71.lps","PjAudioEn72.lps","PjAudioEn73.lps","PjAudioEn74.lps","PjAudioEn75.lps","PjAudioEn76.lps","PjAudioEn77.lps","PjAudioEn78.lps","PjAudioEn79.lps","PjAudioEn80.lps",
                    "PjAudioEn81.lps","PjAudioEn82.lps","PjAudioEn83.lps","PjAudioEn84.lps","PjAudioEn85.lps","PjAudioEn86.lps","PjAudioEn87.lps","PjAudioEn88.lps","PjAudioEn89.lps","PjAudioEn90.lps",
                    "PjAudioEn91.lps","PjAudioEn92.lps","PjAudioEn93.lps","PjAudioEn94.lps","PjAudioEn95.lps","PjAudioEn96.lps","PjAudioEn97.lps","PjAudioEn98.lps","PjAudioEn99.lps","PjAudioEn100.lps"]

class Unpacker:
    def extraer(self, ruta_archivo_completa):
        # 1. Obtener la ruta de la carpeta y el nombre del archivo sin extensión
        directorio_padre = os.path.dirname(ruta_archivo_completa)
        nombre_archivo = os.path.basename(ruta_archivo_completa)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        
        # 2. Definir la ruta de la nueva carpeta (donde mismo está el archivo)
        mydir = os.path.join(directorio_padre, nombre_sin_ext)

        # 3. Si la carpeta existe, la borra
        if os.path.exists(mydir):
            shutil.rmtree(mydir)
            #print(f"DEBUG: Carpeta antigua '{nombre_sin_ext}' eliminada.")
        
        os.makedirs(mydir)

        # 4. Leer archivo
        with open(ruta_archivo_completa, "rb") as f:
            archivo_bin = f.read()

        cont = 4
        for i in range(len(nameList)):
            QCoreApplication.processEvents()
            
            # Punteros Little Endian
            inn = int.from_bytes(archivo_bin[cont:cont+4], "little")
            fin = int.from_bytes(archivo_bin[cont+4:cont+8], "little")
            
            # Numerado y renombrado
            nombre_con_numero = f"{i:03d}_{nameList[i]}"
            ruta_final = os.path.join(mydir, nombre_con_numero)
            
            with open(ruta_final, "wb+") as f_out:
                f_out.write(archivo_bin[inn:fin])
            
            cont += 4
        
        return len(nameList), mydir