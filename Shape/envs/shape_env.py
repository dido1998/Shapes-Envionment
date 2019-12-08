import gym
from gym import error, spaces, utils
from gym.utils import seeding
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QPoint, QSize, QRect, Qt
import math
import Shape.gen_shapes as gen_shapes
import numpy as np
from Shape.rendering import Renderer
import cv2

class config():
	def __init__(self, width, height):
		self.WIDTH = width
		self.HEIGHT = height

		self.N_CELLS = int(self.WIDTH / 10)

		self.CELL_WIDTH = 10
		self.CELL_HEIGHT = 10

		self.BIG_RADIUS = self.CELL_WIDTH * .75 / 2
		self.SMALL_RADIUS = self.CELL_WIDTH * .5 / 2

class ShapeEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.timesteps = 0
		self.renderer = None
		self.cfg = None
		self.num_agents = None

	def actual_init(self, width, height, num_agents, goal):
		self.cfg = config(width, height)
		self.num_agents = num_agents
		self.image = gen_shapes.sample_image(self.cfg)
		self.agent_positions = []
		for i in range(self.num_agents):
			pos_x = np.random.randint(self.cfg.WIDTH - 5)
			pos_y = np.random.randint(self.cfg.HEIGHT - 5)
			self.agent_positions.append([pos_x, pos_y])
		self.goal = goal

	def render(self,  mode='human', close=False):
		if self.renderer is None or self.renderer.window is None:
			
			self.renderer = Renderer()
		img = self.image.data[:, :, :3].copy()
		self.renderer.beginFrame(img)
		self.renderer.setLineColor(255, 255, 255)
		for i, p in enumerate(self.agent_positions):
			self.renderer.drawRect(i, p[0], p[1])
		self.renderer.endFrame()
		return self.renderer

	def step(self, actions):
		for action in actions:
			if action[1] == 1 and self.agent_positions[action[0]][0] + 6 < 30: 
				self.agent_positions[action[0]][0] += 1

			elif action[1] == 2 and self.agent_positions[action[0]][1] + 6 < 30:
				self.agent_positions[action[0]][1] += 1

			elif action[1] == 3 and self.agent_positions[action[0]][0] - 1 >= 0:
				self.agent_positions[action[0]][0] -= 1

			elif action[1] == 4 and self.agent_positions[action[0]][1] - 1 >= 0:
				self.agent_positions[action[0]][1] -= 1
		grid_positions = []
		for pos in self.agent_positions:
			grid_positions.append([math.floor(pos[0] / 10), math.floor(pos[1] / 10)])
		correct_postions = 0
		for i, pos in enumerate(grid_positions):
			if isinstance(self.goal, list):
				if self.image.colors[pos[1]][pos[0]] == self.goal[i]:
					correct_postions += 1
			else:
				if self.image.colors[pos[1]][pos[0]] == self.goal:
					correct_postions += 1

		reward = correct_postions / len(grid_positions)
		obs = []

		for pos in self.agent_positions:
			temp_obs = np.reshape(self.image.state[pos[0] : pos[0] + 5, pos[1] : pos[1] + 5], [1, -1])
			pos_array = np.array([[(pos[0] + 2.5)/100, (pos[1] + 2.5)/100]], dtype = np.float32)
			temp_obs = np.concatenate((temp_obs, pos_array), axis = 1)
			obs.append(temp_obs)
		self.timesteps += 1
		done = False
		if self.timesteps > 50  or reward == 1:
			done = True
		return obs, reward, done, None

	def reset(self):
		self.timesteps = 0
		self.image = gen_shapes.sample_image(self.cfg)
		self.agent_positions = []
		for i in range(self.num_agents):
			pos_x = np.random.randint(self.cfg.WIDTH - 5)
			pos_y = np.random.randint(self.cfg.HEIGHT - 5)
			self.agent_positions.append([pos_x, pos_y])
		obs = []
		for pos in self.agent_positions:
			temp_obs = np.reshape(self.image.state[pos[0] : pos[0] + 5, pos[1] : pos[1] + 5], [1, -1])
			pos_array = np.array([[(pos[0] + 2.5)/100, (pos[1] + 2.5)/100]], dtype = np.float32)
			temp_obs = np.concatenate((temp_obs, pos_array), axis = 1)
			obs.append(temp_obs)
		return obs


