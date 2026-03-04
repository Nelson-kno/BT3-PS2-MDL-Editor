# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QListWidgetItem, QPushButton,QComboBox
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt
from .visor_gl import Visor3D


class VentanaMDL(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Layout principal horizontal
        layout_princ = QHBoxLayout(self)
        
        # Panel de control izquierdo
        self.layout_izq = QVBoxLayout() # Ahora es un atributo de la clase
        
        self.lista_partes = QListWidget()
        self.lista_subpartes = QListWidget()
        
        # Agregamos los elementos al panel de control izquierdo
        self.layout_izq.addWidget(QLabel("IDs de Huesos:"))
        self.layout_izq.addWidget(self.lista_partes)
        self.layout_izq.addWidget(QLabel("Subpartes:"))
        self.layout_izq.addWidget(self.lista_subpartes)

        # Botón "Mostrar Modelo Completo"
        self.btn_ver_mdl_completo = QPushButton("Mostrar Modelo Completo")
        self.layout_izq.addWidget(self.btn_ver_mdl_completo) # Lo agregamos al panel de control izquierdo
        
        # Selector de modo de render: sólido / textura
        
        self.cmbx_render = QComboBox()
        self.cmbx_render.addItems(["Sólido", "Textura"])
        self.layout_izq.addWidget(self.cmbx_render) # Lo agregamos al panel de control izquierdo
        
        
        # Visor OpenGL
        self.visor = Visor3D()
        # Contenedor central que agrupa visor 3D
        self.layout_centro = QHBoxLayout()
        self.layout_centro.addWidget(self.visor) # Lo agregamos al panel central
     

        # panel de textura a la derecha del visor
        self.layout_derecho = QVBoxLayout()
        self.label_textura = QLabel()
        self.label_textura.setStyleSheet("border: 1px solid #444;")
        self.layout_derecho.addWidget(self.label_textura) # Lo agregamos al panel derecho

        # agregamos los layouts al layout principal
        layout_princ.addLayout(self.layout_izq, 1) # Lo agregamos al panel principal
        layout_princ.addLayout(self.layout_centro, 3) # # Lo agregamos al panel principal
        layout_princ.addLayout(self.layout_derecho, 1) # Lo agregamos al panel principal
        

    def cargar_ids(self, lista_ids, lista_vacias):
        self.lista_partes.clear()
        for i, bid in enumerate(lista_ids):
            item = QListWidgetItem(f"Bone ID: {bid}")
            if i < len(lista_vacias) and lista_vacias[i]:
                item.setForeground(QColor("red"))
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.lista_partes.addItem(item)

    def cargar_subpartes(self, subpart_dict):
        self.lista_subpartes.clear()
        # Simplemente contamos cuántos elementos hay en el diccionario
        for i in range(len(subpart_dict)):
            txt = f"Subparte {i}"
            self.lista_subpartes.addItem(txt)