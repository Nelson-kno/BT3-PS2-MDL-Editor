import struct
import math
import json
import os

class AnmLectura:
    def __init__(self, filepath):
        self.filepath = filepath
        self.nombre_archivo = os.path.basename(filepath)
        
        with open(filepath, "rb") as f:
            file = f.read()
        
        self.endianess = "little"
        if file[2:3] == b'00':
            endianess = 'big'
        else:
            endianess = 'little'
        
        nombre_real = [
        "NULL", "PRG_RESERVE", "RESERVE", "WAIST", "TAIL1", "TAIL2", "TAIL3", "TAIL4",
        "HIP_R", "THIGH_R", "SHANK_R", "HEEL_R", "HIP_L", "THIGH_L", "SHANK_L", "HEEL_L",
        "BELLY", "CHEST", "CLAVICLE_R", "SHOULDER_R", "ELBOW_R", "WRIST_R", "THUMB_R",
        "FOREFINGER1_R", "FOREFINGER2_R", "MIDDLE_FINGER1_R", "MIDDLE_FINGER2_R", 
        "MEDICINAL_FINGER1_R", "MEDICINAL_FINGER2_R", "LITTLE_FINGER1_R", "LITTLE_FINGER2_R", 
        "EFFECT_R", "CLAVICLE_L", "SHOULDER_L", "ELBOW_L", "WRIST_L", "THUMB_L", 
        "FOREFINGER1_L", "FOREFINGER2_L", "MIDDLE_FINGER1_L", "MIDDLE_FINGER2_L", 
        "MEDICINAL_FINGER1_L", "MEDICINAL_FINGER2_L", "LITTLE_FINGER1_L", "LITTLE_FINGER2_L", 
        "EFFECT_L", "NECK", "HEAD", "FACE", "CHIN", "HAIR", "ALPHA", "THROW", "CAMERA", 
        "UTILITY", "OPTION01", "OPTION02", "OPTION03", "OPTION04", "OPTION05", "OPTION06", 
        "OPTION07", "OPTION08", "OPTION09", "EQUIPMENT01", "EQUIPMENT02", "BIND_EQUIPMENT01", 
        "BIND_EQUIPMENT02", "UNKNOWN068", "UNKNOWN069", "UNKNOWN070"
        ]
        tiempo_general = int.from_bytes(file[2:4], endianess)
        frame_inicio = 6
        #self.anim_dict = {}
        self.anim_dict =   {
                            "metadata": {
                                "frame_fin": tiempo_general,  # Guardamos el tiempo que atrapaste
                                "nombre_archivo": self.nombre_archivo,    # Guardamos el nombre del archivo que procesaste
                                "endianess": endianess        # Guardamos la endianess detectada
                            },
                            "huesos": {} # Aquí irán todos los huesos que procesas en el loop
                            }

        for bone in range(71):
            boneNameHex = f'{bone:02X}'
            offset = int.from_bytes(file[frame_inicio:frame_inicio+2], endianess) * 4
            frame_inicio += 2
            indice = int(bone)

            #bone_name_real = nombre_real[bone]
            bone_name_real = "{:03d}_{}".format(bone, nombre_real[bone])

            if offset == 0:
                self.anim_dict["huesos"][indice] = {
                                                    "bone_id": boneNameHex,
                                                    "bone_name": bone_name_real,
                                                    "status": False,
                                                    "frames": []
                                                    }
                continue

            frCount, typeAnm, locList, timeList, rotList = self.datos_anm_bone(file, endianess, offset)

            # --- CORRECCIÓN: Inicializar el hueso UNA VEZ fuera del bucle de frames ---
            self.anim_dict["huesos"][indice] = {
                                                "bone_id": boneNameHex,
                                                "bone_name": bone_name_real,
                                                "status": True,
                                                "cantidad_frame": frCount,
                                                "tipo_animacion": typeAnm,
                                                "frames": []
                                                }

            for key_frame in range(frCount):
                # Determinar posición (location)
                if typeAnm == 0:
                    current_loc = locList[key_frame]
                else:
                    current_loc = (0.0, 0.0, 0.0)

                # --- Cálculo de Quaternion ---
                zsQuat = rotList[key_frame]
                axis_to_calculate = zsQuat >> 60
                
                quaternion = []
                for i in range(3):
                    value = (zsQuat >> i * 20) & 0xfffff
                    quaternion.append(float((float(value) / 1048575.0 - 0.5) * 1.4142135))
                quaternion.append(0.0)

                axis_sum = 0.0
                for i in range(3):
                    axis_sum += math.pow(quaternion[i], 2)
                
                axis_sum = max(0.0, 1.0 - axis_sum) # Evitar raíces negativas por precisión
                
                if axis_to_calculate < 3:
                    for i in range(3, axis_to_calculate, -1):
                        quaternion[i] = quaternion[i - 1]
                
                quaternion[axis_to_calculate] = math.sqrt(axis_sum)

                # Reordenamiento específico de formato
                val_temp = quaternion[2]
                quaternion[2] = quaternion[1] * -1.0
                quaternion[1] = val_temp

                # --- GUARDAR CADA FRAME ---
                # Ahora se añaden a la lista sin borrar el frame anterior
                self.anim_dict["huesos"][bone]["frames"].append({
                    "time_frame": timeList[key_frame],
                    "quaternion": [quaternion[3], quaternion[0], quaternion[1], quaternion[2]], # W, X, Y, Z
                    "location": current_loc
                })
                

        # Guardar resultado final
        self.guardar_json()

    def guardar_json(self):
        try:
            ruta_limpia = os.path.splitext(self.nombre_archivo)[0]
            directorio = os.path.dirname(self.filepath)
            nombre_salida = os.path.join(directorio, f"{ruta_limpia}.json")
            
            with open(nombre_salida, "w", encoding='utf-8') as f:
                json.dump(self.anim_dict, f, indent=4, ensure_ascii=False)
            print(f"Archivo guardado: {nombre_salida}")
        except Exception as e:
            print(f"Error al guardar el JSON: {e}")

    def datos_anm_bone(self, file, endianess, offset):
        tipo_anm = int.from_bytes(file[offset:offset+2], endianess)
        frame_cantidad = int.from_bytes(file[offset+2:offset+4], endianess)
   
        if tipo_anm == 1:
            rot_list, key_frame_list = self.tipo_rotacion(file, endianess, frame_cantidad, offset)
            loc_list = []
        else:
            loc_list, key_frame_list, rot_list = self.tipo_mov_rotacion(file, endianess, frame_cantidad, offset)

        return frame_cantidad, tipo_anm, loc_list, key_frame_list, rot_list
    
    def tipo_rotacion(self, file, endianess, frCount, offset):
        ptr_rot = offset + 4
        ptr_time = ptr_rot + (frCount * 8)
        rotList = []
        keyFrameList = []
        for i in range(frCount):
            rotList.append(int.from_bytes(file[ptr_rot:ptr_rot+8], endianess))
            keyFrameList.append(int.from_bytes(file[ptr_time:ptr_time+2], endianess))
            ptr_rot += 8
            ptr_time += 2
        return rotList, keyFrameList
    
    def tipo_mov_rotacion(self, file, endianess, frCount, offset):
        ptr = offset + 4
        rotList = []
        locList = []
        keyframeList = []
        for i in range(frCount):
            x = struct.unpack('f', file[ptr:ptr+4])[0]
            z = struct.unpack('f', file[ptr+4:ptr+8])[0] * -1.0
            y = struct.unpack('f', file[ptr+8:ptr+12])[0]
            locList.append((x, y, z))
            keyframeList.append(int.from_bytes(file[ptr+12:ptr+16], endianess))
            rotList.append(int.from_bytes(file[ptr+16:ptr+24], endianess))
            ptr += 24
        return locList, keyframeList, rotList