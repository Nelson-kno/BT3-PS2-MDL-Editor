# Copyright (C) 2026 Nelson kno

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import sys
import os
import struct
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

from ventanas.vent_mdl import VentanaMDL
from ventanas.menu_bar import MenuPrincipal
from mdl.unpacker import Unpacker
from txt.orderTex16 import OrderTex16col
from txt.dato_parr_a import DatosParrA
from txt.dataId import DataId
from mdl.lector_mdl import DataPart
from anm.lector_anm import AnmLectura

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        version = "v0.2.0-alpha"
        super().__init__()
        self.setWindowTitle(f"BT3 PS2 MDL Editor {version}")
        self.setGeometry(100, 100, 1200, 800)
        
        if os.path.exists("styleapp.css"):
            with open("styleapp.css", "r") as f:
                self.setStyleSheet(f.read())

        self.pmdl_bytes = None
        self.dato_mdl = None
        self.archivo_tex = None
        self.texturas_dict_en_memoria = {}
        self.init_ui()

    def init_ui(self):
        self.menu = MenuPrincipal(self)
        self.setMenuBar(self.menu)
        self.menu.accion_abrir.triggered.connect(self.abrir_archivo)
        self.vent_mdl = VentanaMDL()
        self.setCentralWidget(self.vent_mdl)
        
        self.vent_mdl.cmbx_render.currentIndexChanged.connect(self.cambiar_modo_render)
        self.vent_mdl.lista_partes.itemClicked.connect(lambda item: self.mostrar_subpartes(self.vent_mdl.lista_partes.row(item)))
        self.vent_mdl.lista_subpartes.currentRowChanged.connect(self.lista_subparte_clicked)
        self.vent_mdl.btn_ver_mdl_completo.clicked.connect(self.ver_modelo_completo)
        self.menu.accion_importar_anm.triggered.connect(self.descomprimir_anm_a_json)
        self.menu.accion_ver_jerarquia.triggered.connect(self.abrir_ventana_arbol)

    def cambiar_modo_render(self, indice):
        if self.vent_mdl.visor:
            self.vent_mdl.visor.mostrar_textura = (indice == 1)
            # Regenerar la lista porque el estado de textura cambió
            self.vent_mdl.visor.generar_display_list()
            self.vent_mdl.visor.update()

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Abrir", "", "Archivos (*.unk *.pak *.mdl)")
        if not ruta: return
        try:
            self.vent_mdl.visor.limpiar_cache_texturas()
            self.texturas_dict_en_memoria = {}
            
            unpacker = Unpacker()
            _, ruta_carpeta = unpacker.extraer(ruta)
            
            ruta_pmdl = os.path.join(ruta_carpeta, "002_Pmdl.pmdl")
            if os.path.exists(ruta_pmdl):
                with open(ruta_pmdl, "rb") as f:
                    self.pmdl_bytes = f.read()
                self.dato_mdl = DataPart(self.pmdl_bytes)
                ids_huesos = list(self.dato_mdl.datos_modelo.keys())
                vacias = [self.dato_mdl.datos_modelo[bid]["parte_data"]["tamano_parte"] <= 128 for bid in ids_huesos]
                self.vent_mdl.cargar_ids(ids_huesos, vacias)

            ruta_tex = os.path.join(ruta_carpeta, "011_Tex.dbt")
            if os.path.exists(ruta_tex):
                with open(ruta_tex, 'rb') as f:
                    self.archivo_tex = f.read()
                    self.data_id, self.parrA = DataId(self.archivo_tex), DatosParrA(self.archivo_tex)
                    self.texturas_dict_en_memoria = self.ext_txts()
                    self.vent_mdl.visor.diccionario_binarios = self.texturas_dict_en_memoria
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def mostrar_subpartes(self, fila):
        if not self.dato_mdl or fila < 0: return
        item = self.vent_mdl.lista_partes.item(fila)
        bone_id = item.text().replace("Bone ID: ", "")
        self.info_actual = self.dato_mdl.datos_modelo[bone_id]
        
        p_data = self.info_actual["parte_data"]
        self.vent_mdl.visor.centrar_camara(p_data.get("posicion", [0, 0, 0, 0]), p_data.get("radios_diagonal", [0, 0, 0, 0]))
        self.vent_mdl.cargar_subpartes(self.info_actual["subpartes_data"])

        p_bytes = self.pmdl_bytes[p_data["inicio"]:p_data["fin"]]
        self.vent_mdl.visor.modo_completo = False
        self.vent_mdl.visor.subpartes_a_dibujar = self._geometria_desde_bytes(self.info_actual, p_bytes)
        self.vent_mdl.visor.ids_texturas_subpartes = [s["id_texture"] for s in self.info_actual["subpartes_data"].values()]
        self.vent_mdl.visor.indice_seleccionado = -1
        
        self.vent_mdl.visor.generar_display_list() # <--- REGENERAR
        self.vent_mdl.visor.update()

    def ver_modelo_completo(self):
        if not self.dato_mdl: return
        todas, texs = [], []
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')

        for info in self.dato_mdl.datos_modelo.values():
            p_data = info["parte_data"]
            centro = p_data.get("centro_malla", [0, 0, 0, 0])
            radio_w = p_data.get("radios_diagonal", [0, 0, 0, 0])[3]
            min_x, max_x = min(min_x, centro[0] - radio_w), max(max_x, centro[0] + radio_w)
            min_y, max_y = min(min_y, centro[1] - radio_w), max(max_y, centro[1] + radio_w)
            min_z, max_z = min(min_z, centro[2] - radio_w), max(max_z, centro[2] + radio_w)

            p_bytes = self.pmdl_bytes[p_data["inicio"]:p_data["fin"]]
            todas.extend(self._geometria_desde_bytes(info, p_bytes))
            texs.extend([s["id_texture"] for s in info["subpartes_data"].values()])
        
        centro_final = [(min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2]
        radio_total = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2
        
        self.vent_mdl.visor.centrar_camara(centro_final, [0, 0, 0, radio_total])
        self.vent_mdl.visor.modo_completo = True
        self.vent_mdl.visor.subpartes_a_dibujar = todas
        self.vent_mdl.visor.ids_texturas_subpartes = texs
        self.vent_mdl.visor.indice_seleccionado = -1
        
        self.vent_mdl.visor.generar_display_list() # <--- REGENERAR
        self.vent_mdl.visor.update()

    def lista_subparte_clicked(self, fila):
        if fila < 0 or not hasattr(self, 'info_actual'): return
        self.vent_mdl.visor.indice_seleccionado = fila
        
        # Al seleccionar subparte, regeneramos para que se oculte el resto
        self.vent_mdl.visor.generar_display_list() 
        self.vent_mdl.visor.update()
        
        try:
            sub_key = list(self.info_actual["subpartes_data"].keys())[fila]
            id_txt = self.info_actual["subpartes_data"][sub_key]["id_texture"]
            if id_txt in self.texturas_dict_en_memoria:
                pix = QPixmap()
                pix.loadFromData(self.texturas_dict_en_memoria[id_txt])
                self.vent_mdl.label_textura.setPixmap(pix.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except: pass

    def _geometria_desde_bytes(self, info, parte_bytes):
        geometria = []
        for s_info in info["subpartes_data"].values():
            bloque = parte_bytes[s_info["inicio"]:s_info["fin"]]
            puntos = []
            for j in range(0, len(bloque), 48):
                if j + 40 <= len(bloque):
                    xyz = struct.unpack('<fff', bloque[j:j+12])
                    norm = struct.unpack('<fff', bloque[j+16:j+28])
                    uv = struct.unpack('<ff', bloque[j+32:j+40])
                    puntos.append((xyz, norm, uv))
            if puntos: geometria.append(puntos)
        return geometria

    def ext_txts(self):
        d = {}
        for t in range(len(self.data_id.listId1txt)):
            try:
                i_t, i_p, f_p = self.parrA.DatoParrA[f'inicioT {t}'], self.parrA.DatoParrA[f'inicioP {t}'], self.parrA.DatoParrA[f'finP {t}']
                img = OrderTex16col(self.archivo_tex[i_t:i_p], self.archivo_tex[i_p:f_p])
                d[self.data_id.listId1txt[t]] = img.texBmp
            except: continue
        return d

    def descomprimir_anm_a_json(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Animaciones .anm", "", "Animaciones (*.anm)")
        if files:
            for f in files: AnmLectura(f)
            QMessageBox.information(self, "Proceso Completado", f"Se procesaron {len(files)} archivos.")

    def abrir_ventana_arbol(self):
        if hasattr(self, 'dato_mdl') and self.dato_mdl:
            from ventanas.visor_huesos import VentanaArbolHuesos
            dialogo = VentanaArbolHuesos(self.dato_mdl.datos_modelo, self)
            dialogo.exec_()
        else:
            QMessageBox.warning(self, "Aviso", "Cargue un modelo primero.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = VentanaPrincipal(); v.show()
    sys.exit(app.exec_())