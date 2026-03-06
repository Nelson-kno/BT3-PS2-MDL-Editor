# Copyright (C) 2026 Nelson kno

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

class ProcesadorJerarquia:
    def __init__(self, datos_modelo):
        self.datos = datos_modelo

    def imprimir_consola(self):
        print("\n" + "="*50)
        print("SISTEMA DE JERARQUÍA BT3 - REPORTE DE CONSOLA")
        print("="*50)
        
        stack_ids = []
        indices = sorted(self.datos.keys())
        
        for i in indices:
            p_data = self.datos[i]["parte_data"]
            bone_id = p_data["bone_id"]
            conexion = p_data["conexion_parent"]
            
            # 1. Determinar quién es el padre actual en el stack
            if not stack_ids:
                padre_id = "ROOT"
            else:
                padre_id = stack_ids[-1]
            
            # 2. Calcular profundidad visual (sangría)
            nivel = len(stack_ids)
            sangria = "  " * nivel
            
            # 3. Imprimir el hueso con su relación
            print(f"{sangria}ID: {bone_id} | Padre: {padre_id} | Conexion: {conexion}")
            
            # 4. APLICAR EL TRUCO (Stack Management)
            stack_ids.append(bone_id)
            
            if conexion > 0:
                for _ in range(conexion):
                    if stack_ids:
                        stack_ids.pop()
        
        print("="*50 + "\n")