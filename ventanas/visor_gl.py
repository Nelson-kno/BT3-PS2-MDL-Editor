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
        self.display_list = None  # Cache de geometría en GPU
        
        self.mostrar_textura = False
        self.modo_completo = True 
        self.indice_seleccionado = -1 
        
        # Cámara 
        self.zoom = -60.0      
        self.rot_x = 18.5     
        self.rot_y = -178.5   
        self.pan_x = 0.0       
        self.pan_y = 0.0     
        self.pan_z = 0.0
        self.last_mouse_pos = QPoint()

    def initializeGL(self):
        glClearColor(0.07, 0.07, 0.07, 1.0)
        glEnable(GL_DEPTH_TEST)

        glDepthFunc(GL_LEQUAL)           # Tipo de prueba de profundidad estándar

        #glEnable(GL_CULL_FACE)  # Optimización: no dibujar caras internas
        
        glShadeModel(GL_SMOOTH)
        glCullFace(GL_BACK)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def generar_display_list(self):
        """Graba la geometría en la GPU para que no pese al mover la cámara"""
        if self.display_list is not None:
            glDeleteLists(self.display_list, 1)
        
        self.display_list = glGenLists(1)
        glNewList(self.display_list, GL_COMPILE)
        
        for i, p_list in enumerate(self.subpartes_a_dibujar):
            if not self.modo_completo and self.indice_seleccionado != -1 and i != self.indice_seleccionado:
                continue
            
            id_t = self.ids_texturas_subpartes[i] if i < len(self.ids_texturas_subpartes) else None
            self._renderizar_malla(p_list, id_t)
            
        glEndList()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslated(0, 0, self.zoom)
        glRotatef(self.rot_x, 1.0, 0.0, 0.0)
        glRotatef(self.rot_y, 0.0, 1.0, 0.0)

        self.dibujar_ejes() 

        glTranslated(self.pan_x, self.pan_y, self.pan_z)
        glScalef(1.0, -1.0, 1.0) 

        # DIBUJO OPTIMIZADO
        glDisable(GL_LIGHTING); glDisable(GL_TEXTURE_2D)
        glBegin(GL_LINES); glColor3f(0.2, 0.2, 0.2)
        for i in range(-50, 51, 5):
            glVertex3f(i, 0, -50); glVertex3f(i, 0, 50)
            glVertex3f(-50, 0, i); glVertex3f(50, 0, i)
        glEnd(); glEnable(GL_LIGHTING)

        if self.display_list is not None:
            glCallList(self.display_list)
        

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
            tid = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, img.constBits())
            self.cache_gl_textures[id_txt] = tid
            return tid
        except: return None

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

    def mousePressEvent(self, event): 
        self.last_mouse_pos = event.pos()

    def wheelEvent(self, event): 
        self.zoom += (event.angleDelta().y() / 120) * 5.0; self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        if h > 0: gluPerspective(45, w/h, 0.1, 5000.0)
        glMatrixMode(GL_MODELVIEW)
    
    def limpiar_cache_texturas(self):
        if hasattr(self, 'cache_gl_textures') and self.cache_gl_textures:
            glDeleteTextures(list(self.cache_gl_textures.values()))
        
        if self.display_list is not None:
            glDeleteLists(self.display_list, 1)
            self.display_list = None

        self.cache_gl_textures = {}
        self.diccionario_binarios = {}
        self.subpartes_a_dibujar = []
        self.update()

    def centrar_camara(self, posicion, radio):
        self.pan_x = -posicion[0]
        self.pan_y = posicion[1]
        self.pan_z = -posicion[2]
        r_val = radio[3] if isinstance(radio, list) else radio
        distancia_aire = r_val * 3.5 if r_val > 0 else 15.0
        self.zoom = -posicion[2] - distancia_aire
        self.update()

    def dibujar_ejes(self):
        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(15, 0, 0) # X
        glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, 15, 0) # Y
        glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, 15) # Z
        glEnd()
        glLineWidth(1.0); glEnable(GL_LIGHTING)