import agentpy as ap
import numpy as np
class CleaningRobot(ap.Agent):

#Funcion setup para brindarle fucniones iniciales a el agente del limpeiza 
    def setup(self):
        self.M = self.model.M
        self.N = self.model.M
        self.dirty_percentage = self.model.dirty_percentage
        self.max_time = self.model.max_time

        self.total_cells = self.M * self.N
        self.dirty_cells = int(self.dirty_percentage * self.total_cells)
        self.clean_cells = 0
        self.current_position = (1, 1)
        self.moves = 0

    # Verificar si una posición dada está sucia
    def is_dirty(self, position):
        return position in self.model.dirty_positions

    # Limpiar la celda actual si está sucia
    def clean(self):
        if self.is_dirty(self.current_position):
            self.model.dirty_positions.remove(self.current_position)
            self.clean_cells += 1

# Realizar un movimiento aleatorio dentro del ambiente
    def move(self):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        dx, dy = self.model.random.choice(moves)
        new_position = (self.current_position[0] + dx, self.current_position[1] + dy)

        # Verificar si el movimiento es válido dentro del ambientee

        if 1 <= new_position[0] <= self.M and 1 <= new_position[1] <= self.N:
            self.current_position = new_position
            self.moves += 1

    def step(self):
        # Terminar la simulación si se alcanza el tiempo máximo o se terminaron la celdas sucias
        if self.model.time >= self.max_time:
            self.model.end()
        else:
            self.clean()
            self.move()
            self.model.time += 1 # Incrementar el tiempo de la simulación

class CleaningModel(ap.Model):

    def setup(self):
        # Inicialización de parámetros del modelo
        self.Agentes = 100
        self.M = 100
        self.N = 100
        self.dirty_percentage = 0.2
        self.max_time = 400000
        self.time = 0

        # Inicialización de celdas sucias aleatorias

        self.dirty_positions = set()
        while len(self.dirty_positions) < int(self.dirty_percentage * self.M * self.N):
            x = self.random.randint(1, self.M)
            y = self.random.randint(1, self.N)
            self.dirty_positions.add((x, y))

        self.cleaning_robots = ap.AgentList(self, self.Agentes, CleaningRobot)
        self.results_printed = False  # Variable de control para los resultados

    def step(self):
        if self.time >= self.max_time or len(self.dirty_positions) == 0:
            self.end()
        else:
            self.time += 1
            self.cleaning_robots.step()

    # Imprimime los resultados al finalizar la simulación
    def end(self):
        if not self.results_printed:
            for robot in self.cleaning_robots:
                percentage_cleaned = (robot.clean_cells / robot.total_cells) * (100/ self.dirty_percentage)
                total_moves = robot.moves
                print("\n")
                print("Porcentaje limpio: {:.2f}".format(percentage_cleaned), "%")
                print("Total de movimeintos:", total_moves)
                print("Tiempo:", self.time)
            self.results_printed = True
        self.stop()  # Detiene la simulacion


# Se crea una nueva instancia del modelo de limpieza, utilizando la clase CleaningModel
model = CleaningModel()
model.run()

