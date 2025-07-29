import os

import pygame

from ..geometry import Point, Line, Circle, Trail
from ..types import Position, Time
from .renderer import Renderer


class PyGameRenderer(Renderer):
	def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float, ppu: float) -> None:
		self.xmin, self.ymax, self.ppu = xmin, ymax, ppu
		self.screen = pygame.display.set_mode(((xmax - xmin)*ppu, (ymax - ymin)*ppu))
		self.point_layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		self.line_layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		self.trail_layer = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		pygame.init()
		pygame.display.set_caption('Levers')
		self.clock = pygame.time.Clock()

	def run(self, fps: float) -> None:
		delay = pygame.time.get_ticks()
		done = False
		while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
			self.next_frame((pygame.time.get_ticks() - delay) / 1000)
			self.clock.tick(fps)
		pygame.quit()

	def capture(self, fps: float, frames: int, path: str) -> None:
		os.makedirs(path, exist_ok=True)
		for frame in range(frames):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return
			self.next_frame(frame/fps)
			pygame.image.save(self.screen, os.path.join(path, f'{frame}.png'))
		pygame.quit()

	def next_frame(self, t: Time) -> None:
		self.screen.fill('black')
		self.point_layer.fill((0, 0, 0, 0))
		self.line_layer.fill((0, 0, 0, 0))
		self.trail_layer.fill((0, 0, 0, 0))
		self.draw_grid(self.screen)
		self.draw_all(t)
		self.screen.blit(self.trail_layer, (0, 0))
		self.screen.blit(self.line_layer, (0, 0))
		self.screen.blit(self.point_layer, (0, 0))
		pygame.display.flip()

	def draw_point(self, point: Point) -> None:
		if point.style.visible == False:
			return
		pygame.draw.circle(
			self.point_layer,
			pygame.Color(point.style.color),
			self.screen_coords(point.x, point.y),
			point.style.width/2
		)

	def draw_line(self, line: Line) -> None:
		if line.style.visible == False:
			return
		pygame.draw.line(
			self.line_layer,
			pygame.Color(line.style.color),
			self.screen_coords(line.p1.x, line.p1.y),
			self.screen_coords(line.p2.x, line.p2.y),
			line.style.width
		)

	def draw_circle(self, circle: Circle) -> None:
		if circle.style.visible == False:
			return
		pygame.draw.circle(
			self.line_layer,
			pygame.Color(circle.style.color),
			self.screen_coords(circle.center.x, circle.center.y),
			circle.radius*self.ppu,
			circle.style.width
		)

	def draw_trail(self, trail: Trail) -> None:
		if trail.line_style.visible:
			pygame.draw.lines(
				self.trail_layer,
				pygame.Color(trail.line_style.color),
				False,
				tuple(self.screen_coords(*c) for c in zip(*trail.history.values())),
				trail.line_style.width
			)
		if trail.point_style.visible:
			for c in zip(*trail.history.values()):
				pygame.draw.circle(
					self.trail_layer,
					pygame.Color(trail.point_style.color),
					self.screen_coords(*c),
					trail.point_style.width/2
				)

	def draw_grid(self, surface: pygame.Surface) -> None:
		screen_x, screen_y = self.screen.get_size()
		for i in range(0, screen_y, self.ppu):
			pygame.draw.line(surface, pygame.Color('#202020'), (0, i), (screen_x, i), 1)
		for i in range(0, screen_x, self.ppu):
			pygame.draw.line(surface, pygame.Color('#202020'), (i, 0), (i, screen_y), 1)

	def screen_coords(self, x: float, y: float) -> Position:
		screen_x = self.ppu * (x - self.xmin)
		screen_y = self.ppu * (self.ymax - y)
		return (screen_x, screen_y)
