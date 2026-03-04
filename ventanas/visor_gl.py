# Copyright (C) 2026 Nelson kno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PySide2.QtOpenGL import QGLWidget
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QImage
from OpenGL.GL import *
from OpenGL.GLU import *

class Visor3D(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.subpartes_a_dibujar = []
        self.ids_texturas_subpartes = []
        self.diccionario_binarios = {}
        self.cache_gl_textures = {}
        
        self.mostrar_textura = False
        self.modo_completo = True 
        self.indice_seleccionado = -1 
        
        # Cámara 
        self.zoom = -60.0      
        self.rot_x = 18.5     
        self.rot_y = -178.5   
        self.pan_x = 0.0       
        self.pan_y = 0.0     
        self.last_mouse_pos = QPoint()

    def initializeGL(self):
        glClearColor(0.07, 0.07, 0.07, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        # Ajuste de luz 
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glScalef(1.0, -1.0, 1.0) # Inversión de eje Y necesaria
        
        self.dibujar_escena()

    def dibujar_escena(self):
        # Grid Fijo 
        glDisable(GL_LIGHTING); glDisable(GL_TEXTURE_2D)
        glBegin(GL_LINES); glColor3f(0.2, 0.2, 0.2)
        for i in range(-50, 51, 5):
            glVertex3f(i, 0, -50); glVertex3f(i, 0, 50)
            glVertex3f(-50, 0, i); glVertex3f(50, 0, i)
        glEnd(); glEnable(GL_LIGHTING)

        # Lógica de dibujo con resaltado de respaldo
        for i, p_list in enumerate(self.subpartes_a_dibujar):
            if not self.modo_completo and self.indice_seleccionado != -1 and i != self.indice_seleccionado:
                continue
            
            id_t = self.ids_texturas_subpartes[i] if i < len(self.ids_texturas_subpartes) else None
            self._renderizar_malla(p_list, id_t)

    def _renderizar_malla(self, puntos, id_txt):
        if self.mostrar_textura and id_txt:
            tex_id = self._cargar_textura_gl(id_txt)
            if tex_id:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glColor4f(1, 1, 1, 1)
            else: glDisable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor4f(0.8, 0.8, 0.8, 1.0)

        glBegin(GL_TRIANGLE_STRIP)
        for p in puntos:
            glNormal3fv(p[1])
            glTexCoord2f(p[2][0], p[2][1])
            glVertex3fv(p[0])
        glEnd()

    def _cargar_textura_gl(self, id_txt):
        if id_txt in self.cache_gl_textures: return self.cache_gl_textures[id_txt]
        if id_txt not in self.diccionario_binarios: return None
        try:
            img = QImage.fromData(self.diccionario_binarios[id_txt]).convertToFormat(QImage.Format_RGBA8888)
            # QUITADO el mirrored para que no se rote en Y y se vea igual que en el juego
            tid = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, img.constBits())
            self.cache_gl_textures[id_txt] = tid
            return tid
        except: return None

    # Controles de mouse
    def mouseMoveEvent(self, event):
        diff = event.pos() - self.last_mouse_pos
        self.last_mouse_pos = event.pos()
        if (event.buttons() == Qt.MidButton) and (event.modifiers() == Qt.ShiftModifier):
            self.pan_x += diff.x() * 0.05
            self.pan_y -= diff.y() * 0.05
        elif event.buttons() == Qt.MidButton:
            self.rot_y += diff.x() * 0.5
            self.rot_x += diff.y() * 0.5 
        self.update()

    def mousePressEvent(self, event): self.last_mouse_pos = event.pos()
    def wheelEvent(self, event): self.zoom += (event.angleDelta().y() / 120) * 5.0; self.update()
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        if h > 0: gluPerspective(45, w/h, 0.1, 5000.0)
        glMatrixMode(GL_MODELVIEW)