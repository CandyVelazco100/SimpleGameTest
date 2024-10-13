import pygame
import random

WIDTH, HEIGHT = 800, 600
IMAGE_SIZE = 60
BLACK = (0, 0, 0)
WINNER = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piedra, papel o tijeras")

# Cargar y escalar imágenes
rock_img = pygame.image.load("rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (IMAGE_SIZE, IMAGE_SIZE))
paper_img = pygame.image.load("paper.png").convert_alpha()
paper_img = pygame.transform.scale(paper_img, (IMAGE_SIZE, IMAGE_SIZE))
scissors_img = pygame.image.load("scissors.png").convert_alpha()
scissors_img = pygame.transform.scale(scissors_img, (IMAGE_SIZE, IMAGE_SIZE))

class Point:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.choice([-2, -1, 1, 2])
        self.image = self.get_image()

    def get_image(self):
        if self.kind == 'rock':
            return rock_img
        elif self.kind == 'paper':
            return paper_img
        elif self.kind == 'scissors':
            return scissors_img

    def move(self):
        # Mover el punto y verificar los límites
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= WIDTH - IMAGE_SIZE:
            self.speed_x = -self.speed_x  # Invertir dirección en x
        if self.y <= 0 or self.y >= HEIGHT - IMAGE_SIZE:
            self.speed_y = -self.speed_y  # Invertir dirección en y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, other):
        return pygame.Rect(self.x, self.y, IMAGE_SIZE, IMAGE_SIZE).colliderect(
            pygame.Rect(other.x, other.y, IMAGE_SIZE, IMAGE_SIZE)
        )

    def battle(self, other):
        if WINNER[self.kind] == other.kind:
            other.kind = self.kind
            other.image = other.get_image()  # Actualizar imagen
        elif WINNER[other.kind] == self.kind:
            self.kind = other.kind
            self.image = self.get_image()  # Actualizar imagen

class Game:
    def __init__(self, num_points):
        self.points = []

        kinds = ['rock', 'paper', 'scissors']
        points_per_kind = num_points // 3

        for kind in kinds:
            for _ in range(points_per_kind):
                x = random.randint(0, WIDTH - IMAGE_SIZE)
                y = random.randint(0, HEIGHT - IMAGE_SIZE)
                self.points.append(Point(x, y, kind))

    def update(self):
        for point in self.points:
            point.move()

        # Verificar colisiones y resolver batallas
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                if self.points[i].check_collision(self.points[j]):
                    self.points[i].battle(self.points[j])

    def draw(self, screen):
        screen.fill(BLACK)
        for point in self.points:
            point.draw(screen)

    def game_over(self):
        first_kind = self.points[0].kind
        return all(point.kind == first_kind for point in self.points)

# Inicializar el juego
num_points = 12
game = Game(num_points)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()
    game.draw(screen)

    if game.game_over():
        print("Game Over")
        print("Todos los puntos son iguales, fin del juego")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()