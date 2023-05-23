import tkinter as tk
import random

# Window dimensions
WIDTH = 400
HEIGHT = 600

# Bird properties
BIRD_RADIUS = 20
BIRD_COLOR = "yellow"
BIRD_JUMP_VELOCITY = -8

# Pipe properties
PIPE_WIDTH = 80
PIPE_COLOR = "green"
PIPE_VELOCITY = 5
PIPE_GAP = 200
MIN_PIPE_HEIGHT = 50
MAX_PIPE_HEIGHT = HEIGHT - PIPE_GAP - MIN_PIPE_HEIGHT

# Gravity
GRAVITY = 0.5


class Bird:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_oval(50, 50, 50 + BIRD_RADIUS, 50 + BIRD_RADIUS, fill=BIRD_COLOR)
        self.x = WIDTH / 2 - BIRD_RADIUS / 2
        self.y = HEIGHT / 2 - BIRD_RADIUS / 2
        self.velocity = 0

    def jump(self, event=None):
        self.velocity = BIRD_JUMP_VELOCITY

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.canvas.coords(self.id, self.x, self.y, self.x + BIRD_RADIUS, self.y + BIRD_RADIUS)

    def is_colliding(self, pipe):
        bird_coords = self.canvas.coords(self.id)
        pipe_coords_top = self.canvas.coords(pipe.id_top)
        pipe_coords_bottom = self.canvas.coords(pipe.id_bottom)
        return bird_coords[0] < pipe_coords_top[2] and bird_coords[2] > pipe_coords_top[0] and \
               (bird_coords[1] < pipe_coords_top[3] or bird_coords[3] > pipe_coords_bottom[1])


class Pipe:
    def __init__(self, canvas, x, height):
        self.canvas = canvas
        self.id_top = canvas.create_rectangle(x, 0, x + PIPE_WIDTH, height, fill=PIPE_COLOR)
        self.id_bottom = canvas.create_rectangle(x, height + PIPE_GAP, x + PIPE_WIDTH, HEIGHT, fill=PIPE_COLOR)
        self.x = x

    def update(self):
        self.x -= PIPE_VELOCITY
        self.canvas.move(self.id_top, -PIPE_VELOCITY, 0)
        self.canvas.move(self.id_bottom, -PIPE_VELOCITY, 0)

    def is_offscreen(self):
        pipe_coords = self.canvas.coords(self.id_top)
        return pipe_coords[2] < 0


class Game:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.bird = Bird(self.canvas)
        self.pipes = []

        self.score = 0
        self.score_label = self.canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="white")
        self.game_over_text = None

        self.canvas.bind("<space>", self.bird.jump)
        self.master.bind("<space>", self.bird.jump)

        self.running = False

    def start(self):
        self.reset()
        self.running = True
        self.canvas.focus_set()
        self.add_pipe()
        self.update()

    def reset(self):
        self.bird.y = HEIGHT / 2 - BIRD_RADIUS / 2
        self.bird.velocity = 0
        self.pipes.clear()
        self.score = 0
        self.canvas.delete(self.game_over_text)

    def stop(self):
        self.running = False
        self.game_over_text = self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over",
                                                      font=("Arial", 24), fill="white")

    def update(self):
        if not self.running:
            return

        self.bird.update()

        for pipe in self.pipes:
            pipe.update()
            if self.bird.is_colliding(pipe):
                self.stop()

        self.pipes = [pipe for pipe in self.pipes if not pipe.is_offscreen()]

        if len(self.pipes) == 0 or WIDTH - self.pipes[-1].x >= PIPE_GAP:
            x = WIDTH + random.randint(100, 300)
            height = random.randint(MIN_PIPE_HEIGHT, MAX_PIPE_HEIGHT)
            self.add_pipe(x, height)

        self.canvas.itemconfig(self.score_label, text="Score: " + str(self.score))
        self.score += 1

        self.canvas.after(20, self.update)

    def add_pipe(self, x=None, height=None):
        if x is None:
            x = WIDTH
        if height is None:
            height = random.randint(MIN_PIPE_HEIGHT, MAX_PIPE_HEIGHT)
        self.pipes.append(Pipe(self.canvas, x, height))

    def game_over(self):
        self.stop()


root = tk.Tk()
root.title("Flappy Bird")
game = Game(root)
game.start()
root.mainloop()
