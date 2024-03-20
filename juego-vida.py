import pygame
import numpy as np
import time

pygame.init()

whidth, height = 1000, 1000
screen = pygame.display.set_mode((whidth, height))

bg = 25, 25, 25
screen.fill(bg)

# Cantidad de las cledas en  X, Y
celdasX, celdasY = 25,25

# Ancho y alto de cada celda(Dimensiones de la celda)
whidthCell = whidth / celdasX
heightCell = height / celdasY

# Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((celdasX, celdasY))

# Registramos eventos ratón para flagear celdas
ev = pygame.event.get()

# Control de la ejecución del juego
pauseExect = False

# Automata de juego de la vida
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

## BLucle de ejecucion
while True:
   # Copia del estado del juego
   newGameState = np.copy(gameState)
   # Limpiamos la pantalla
   screen.fill(bg)
   time.sleep(0.1)

   # Determina si deve pausar o añadir nuevas celdas
   for event in pygame.event.get():
      # Detiene o continua la ejecución del juego
      if event.type == pygame.KEYDOWN:
         pauseExect = not pauseExect

      # Detecta si se ha presionado el ratón
      mouseClick = pygame.mouse.get_pressed()
      if sum(mouseClick) > 0:
         posX, posY = pygame.mouse.get_pos()
         celX, celY = int(np.floor(posX / whidthCell)), int(np.floor(posY / heightCell))
         newGameState[celX, celY] = not mouseClick[2]

   for y in range(0, celdasY):
      for x in range(0, celdasX):
         if not pauseExect:
            # Caclulamos el número de vecinios cercanos
            neighbors = gameState[(x-1) % celdasX, (y-1) % celdasY] + \
                        gameState[(x) % celdasX,   (y-1) % celdasY] + \
                        gameState[(x+1) % celdasX, (y-1) % celdasY] + \
                        gameState[(x-1) % celdasX, (y) % celdasY]   + \
                        gameState[(x+1) % celdasX, (y) % celdasY]   + \
                        gameState[(x-1) % celdasX, (y+1) % celdasY] + \
                        gameState[(x) % celdasX,   (y+1) % celdasY] + \
                        gameState[(x+1) % celdasX, (y+1) % celdasY]
            # Regla 1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
            if gameState[x, y] == 0 and neighbors == 3:
               newGameState[x, y] = 1
            # Regla 2: Una célula viva con 2 o más de 3 vecinas vivas, "muere".
            elif gameState[x, y] == 1 and (neighbors < 2 or neighbors > 3):
               newGameState[x, y] = 0

            # Creamos el poligono de cada celda a dibujar
            poly = [
                     ((x) * whidthCell, (y) * heightCell),
                     ((x+1) * whidthCell, (y) * heightCell),
                     ((x+1) * whidthCell, (y+1) * heightCell),
                     ((x) * whidthCell, (y+1) * heightCell)
                  ]
            # Dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
               pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
               pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
   # Actualizamos el estado del juego
   gameState = np.copy(newGameState)
   pygame.display.flip()
