# Copyright (C) 2026 Nelson kno

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide2.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QHeaderView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

class VentanaArbolHuesos(QDialog):
    def __init__(self, datos_modelo, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Jerarquía de Huesos - BT3 MDL")
        self.resize(400, 600)
        
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Jerarquía de Partes / Huesos"])
        layout.addWidget(self.tree)
        
        self.cargar_datos(datos_modelo)
        
    def cargar_datos(self, datos_modelo):
        self.tree.clear()
        
        # Esta lista simula tus "item1, item2, item3..." de forma dinámica
        stack_items = []
        
        # Ordenamos por Bone ID para procesar linealmente
        indices = sorted(datos_modelo.keys())
        
        for i in indices:
            data_p = datos_modelo[i]["parte_data"]
            bone_id_hex = data_p["bone_id"]
            conexion = data_p["conexion_parent"]
            tamano = data_p["tamano_parte"]
            
            # Crear el item actual
            nombre_item = f"{i}_ ID: {bone_id_hex}"
            item_actual = QTreeWidgetItem([nombre_item])
            
            # Aplicar color de icono según tamaño (tu lógica img_bone)
            if tamano == 64:
                item_actual.setForeground(0, Qt.red) # O usar QIcon si tienes los archivos
            elif tamano == 128:
                item_actual.setForeground(0, Qt.darkYellow)
            else:
                item_actual.setForeground(0, Qt.darkGreen)

            # LÓGICA DEL TRUCO (Jerarquía)
            if not stack_items:
                # Si la pila está vacía, es un elemento raíz
                self.tree.addTopLevelItem(item_actual)
            else:
                # El padre es el último que está en la cima de la pila
                stack_items[-1].addChild(item_actual)
            
            # Añadir este item a la pila para que sea posible padre del siguiente
            stack_items.append(item_actual)
            
            # REPLICAR COMPORTAMIENTO conexion_parent (Retroceder niveles)
            if conexion > 0:
                for _ in range(conexion):
                    if stack_items:
                        stack_items.pop()
        
        self.tree.expandAll()
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)