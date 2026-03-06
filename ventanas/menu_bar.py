# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide2.QtWidgets import QMenuBar, QAction, QMessageBox

class MenuPrincipal(QMenuBar):
    def __init__(self, parent=None):
        super(MenuPrincipal, self).__init__(parent)
        self.init_menu()

    def init_menu(self):
        # --- ARCHIVO ---
        menu_archivo = self.addMenu("Archivo")
        self.accion_abrir = QAction("Abrir Archivo (.unk) (.pak)", self)
        self.accion_salir = QAction("Salir", self)
        menu_archivo.addAction(self.accion_abrir)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.accion_salir)

        # --- UTILIDADES ---
        menu_utilidades = self.addMenu("Utilidades")
        self.accion_importar_anm = QAction("Importar (.anm) y Convertir Animaciones (.json)", self)
        self.accion_ver_jerarquia = QAction("Ver Jerarquía de Huesos (Tree)", self)

        menu_utilidades.addAction(self.accion_importar_anm)

        menu_utilidades.addSeparator() # Una línea para separar animaciones de modelos
        menu_utilidades.addAction(self.accion_ver_jerarquia)

        # --- INFORMACIÓN ---
        menu_info = self.addMenu("Información")
        self.accion_ayuda = QAction("Ayuda", self)
        menu_info.addAction(self.accion_ayuda)
        

        

    def mostrar_ayuda(self):
        QMessageBox.information(self, "Ayuda", "BT3 PS2 MDL Editor\nBy: Nelson Kno.")