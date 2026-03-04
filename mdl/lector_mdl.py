# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import json

class DataSubPart:
    def __init__(self, parte):
        sep = b'\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00\x17'
        cantSubPart = parte.count(sep) 
        index = 190

        self.datos = {}
        for i in range(cantSubPart):
            id_txt = parte[index-66:index-58].hex().upper()
            id_smb = parte[index-50:index-42].hex().upper()
            tam_sub_parte = int.from_bytes(parte[index:index+1], 'little')*16 
            cant_ver = int.from_bytes(parte[index:index+1], 'little')//3
            #self.cantVert.append(cant_ver)

            inicio_sub_parte = index+2
            fin_sub_parte = inicio_sub_parte+tam_sub_parte
            index += tam_sub_parte + 92
         
            self.datos[f"sub_parte_{i}"] = {
                "id_texture": id_txt,
                "sombra_id": id_smb,
                "inicio": inicio_sub_parte,
                "fin": fin_sub_parte,
                "cantidad_vertices": cant_ver,
                "tamano_subparte": tam_sub_parte
            }
    
class DataPart:
    def __init__(self, file):
        # Diccionario principal que contendrá toda la información del modelo, organizado por Bone ID
        self.datos_modelo = {}
        # Lista de Bone IDs para llenar el ListWidget en orden de aparición en el archivo
        self.bone_ids_list = []
        
        # Leemos el offset de inicio desde la posición 108
        inicio = int.from_bytes(file[108:112], "little")
        
        while True:
            # 1. Extraer datos básicos de la "Parte"
            tamano_parte = int.from_bytes(file[inicio:inicio+4], "little")
            conexion_parent = int.from_bytes(file[inicio+4:inicio+6], "little")
            
            # Verificamos si es el fin del esqueleto (01 00 en bytes 6:8)
            # Como mencionaste en tu nota: "si es igual a 01 00 termina todo"
            fin_bone = int.from_bytes(file[inicio+6:inicio+8], "little")
            if fin_bone == 1:
                break
            
            # ID del hueso (bytes 10:12)
            bone_id = file[inicio+10:inicio+11].hex().upper()
            
            # 2. Creamos la estructura para este Bone ID
            self.datos_modelo[bone_id] = {
                "parte_data": {
                    "inicio": inicio,
                    "fin": inicio + tamano_parte,
                    "tamano_parte": tamano_parte,
                    "conexion_parent": conexion_parent,
                    "bone_id": bone_id
                },
                "subpartes_data": {} # Aquí guardaremos lo que devuelva DataSubPart
            }

            # 3. Procesar Subpartes
            # Si el tamaño es mayor a 64, significa que tiene datos de malla/textura
            #if tamano_parte > 64:
            if tamano_parte > 128:
                parte_bytes = file[inicio : inicio + tamano_parte]
                
                # Llamamos a tu clase DataSubPart
                sub_proc = DataSubPart(parte_bytes)
                
                # Guardamos su diccionario .datos directamente
                self.datos_modelo[bone_id]["subpartes_data"] = sub_proc.datos

            # 4. AVANZAR el puntero al siguiente bloque
            # Esto es lo que evita el bucle infinito que tenías antes
            inicio += tamano_parte
        
        self.exportar_a_json("modelo_salida.json")
        
    def exportar_a_json(self, nombre_archivo):
        # Ahora usamos 'self.datos_modelo' directamente
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(self.datos_modelo, f, indent=4)
        #print(f"¡Hecho! JSON guardado como: {nombre_archivo}")