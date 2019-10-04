#!/usr/bin/env python3

import pygame

from particula import Particula
from particula import Estado
from punto import Punto

from variables import SIMULACION_FONDO_COLOR
from variables import (PARTICULA_VECTOR_X_COLOR, PARTICULA_VECTOR_Y_COLOR,
	PARTICULA_VECTOR_X_GROSOR, PARTICULA_VECTOR_COLOR)
from vector_grafico import VectorGrafico

class Canvas:
	"""
		una subventana para renderizar lo que se quiera
		un canvas no sirve de nada hasta que se añade
		a una ventana.
	"""

	def __init__(self, tamano, origen):
		self.tamano = tamano
		self.origen = origen
		self.pantalla = None
		self.superficie = pygame.Surface(tamano)
		self.ratio_vertical = 0.60 #ajusta la proporción vertical
		self.ratio_horizontal = 0.5 #no es relevante al final
		self.background = SIMULACION_FONDO_COLOR
		self.particulas = {}

	def get_superficie(self):
		return self.superficie

	def add_particula(self, particula, id):
		particula.canvas = self
		self.particulas[id] = particula

	def update(self):
		"""
			renderiza el canvas, coloreando el fondo
			y renderizando en sí mismo a la superficie
			que tenga.
		"""
		self.superficie.fill(self.background)
		self.pantalla.blit(self.superficie, self.origen)
		for particula in self.particulas.values():
			if particula.tiempo_transcurrido < particula.tiempo_total:
				particula.simular()
			particula.trayectoria.render(self)
			pygame.draw.circle(self.superficie, particula.color, (int(particula.posicion.x), int(particula.posicion.y)), particula.radio, 0)
			if(particula.estado == Estado.TERMINADO):		#al terminar la simulación
				
				pos_x = pygame.mouse.get_pos()[0]
				if pos_x in particula.trayectoria.puntos.keys(): #cuando termina la simulación
					pos_y = particula.trayectoria.puntos[pos_x]
					#renderizando el punto
					pygame.draw.circle(self.superficie, (255, 255, 0), (pos_x, pos_y), 3, 0)
					#renderizado de los vectores componentes
					vector = particula.trayectoria.velocidades[pos_x]
					VectorGrafico(Punto(pos_x, pos_y), vector.get_vector_x()).render( #velocidad x
						superficie=self.superficie,
						color=PARTICULA_VECTOR_X_COLOR,
						grosor=PARTICULA_VECTOR_X_GROSOR)

					VectorGrafico(Punto(pos_x, pos_y), vector.get_vector_y()).render( #velocidad y
						superficie=self.superficie,
						color=PARTICULA_VECTOR_Y_COLOR,
						grosor=PARTICULA_VECTOR_X_GROSOR
					)

					VectorGrafico(Punto(pos_x, pos_y), vector).render(
						superficie=self.superficie,
						color=PARTICULA_VECTOR_COLOR,
						grosor=PARTICULA_VECTOR_X_GROSOR
					)
		
		#acomoda la pantalla para que se vea bien el tiro
		self.superficie.blit(pygame.transform.rotate(self.superficie, 180), (0, 0))
		self.superficie.blit(pygame.transform.flip(self.superficie, True, False), (0, 0))
	

	def get_tamano_lista(self):
		#muestra el tamano en forma de array []
		width, height = self.tamano
		return [width, height]



#----PRUEBAS
if __name__ == '__main__':
	from ventana import Ventana
	v = Ventana((600, 400))
	canvas = Canvas((600, 200), (0, 10))
	v.add_canvas(canvas, "0")
	v.run()

