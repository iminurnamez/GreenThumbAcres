import os
import random
import itertools
import pygame
from pygame import Color

class Tool(object):
	def assign_image(self):
		self.image = pygame.image.load(os.path.join("Art", self.name + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.surface = pygame.Surface((self.Rect.width, self.Rect.height))
		self.surface.set_colorkey((157, 187, 97))
		
class Shovel(Tool):
	def __init__(self):
		self.name = "shovel"
		self.assign_image()
		self.in_use = False
class WateringCan(Tool):
	def __init__(self):
		self.name = "wateringcan"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant):
		thirst = plant.max_water - plant.water
		plant.water = plant.max_water
		player.water_usage += thirst
	
class SeedBag(Tool):
	def __init__(self):
		self.name = "seedbag"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue, current_plant_type):
		qty = random.randint(1, 4)
		player.seeds[plant.name] += qty 
		news_queue.append("Collected {0} {1} seeds.".format(qty,plant.name))
		current_plant_type = plant.__class__
		if not plant.perennial:
			for plot in plots:
				if plot.Rect.colliderect(plant.Rect):
					plot.empty = True
					plants.remove(plant)
		else:
			plant.growth = plant.stage5_step + 1
			plant.manured = False
		return current_plant_type

class SeedScoop(Tool):
	def __init__(self):
		self.name = "seedscoop"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue, current_plant_type):
		qty = random.randint(2, 4)
		player.seeds[plant.name] += qty 
		news_queue.append("Collected {0} {1} seeds.".format(qty,plant.name))
		current_plant_type = plant.__class__
		if not plant.perennial:
			for plot in plots:
				if plot.Rect.colliderect(plant.Rect):
					plot.empty = True
					plants.remove(plant)
		else:
			plant.growth = plant.stage5_step + 1
			plant.manured = False
		return current_plant_type
		
class SeedSieve(Tool):
	def __init__(self):
		self.name = "seedsieve"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue, current_plant_type):
		qty = random.randint(2, 5)
		player.seeds[plant.name] += qty 
		news_queue.append("Collected {0} {1} seeds.".format(qty,plant.name))
		current_plant_type = plant.__class__
		if not plant.perennial:
			for plot in plots:
				if plot.Rect.colliderect(plant.Rect):
					plot.empty = True
					plants.remove(plant)
		else:
			plant.growth = plant.stage5_step + 1
			plant.manured = False
		return current_plant_type
		
class Manure(Tool):
	def __init__(self):
		self.name = "manure"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant):
		if not plant.manured:
			player.manure_usage += 1
			plant.manured = True
		
class Basket(Tool):
	def __init__(self):
		self.name = "basket"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue):
		qty = random.randint(1, 4)
		player.crops[plant.name] += qty 
		player.crops_harvested[plant.name] += qty
		news_queue.append("Collected {0} {1}.".format(qty,plant.name))
		if not plant.perennial:
			for plot in plots:
				if plant.Rect.colliderect(plot.Rect):
					plot.empty = True
					plants.remove(plant)	
		else:
			plant.growth = plant.stage5_step + 1
			
class Crate(Tool):
	def __init__(self):
		self.name = "Crate"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue):
		qty = random.randint(2, 4)
		player.crops[plant.name] += qty 
		player.crops_harvested[plant.name] += qty
		news_queue.append("Collected {0} {1}.".format(qty,plant.name))
		if not plant.perennial:
			for plot in plots:
				if plant.Rect.colliderect(plot.Rect):
					plot.empty = True
					plants.remove(plant)	
		else:
			plant.growth = plant.stage5_step + 1
			
class Wheelbarrow(Tool):
	def __init__(self):
		self.name = "wheelbarrow"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant, plants, plots, news_queue):
		qty = random.randint(2, 5)
		player.crops[plant.name] += qty 
		player.crops_harvested[plant.name] += qty
		news_queue.append("Collected {0} {1}.".format(qty,plant.name))
		if not plant.perennial:
			for plot in plots:
				if plant.Rect.colliderect(plot.Rect):
					plot.empty = True
					plants.remove(plant)	
		else:
			plant.growth = plant.stage5_step + 1
			
			
class Fertilizer(Tool):
	def __init__(self):
		self.name = "fertilizer"
		self.assign_image()
		self.in_use = False
	def use(self, player, plant):
		sun_thirst = plant.max_solar - plant.solar_energy
		plant.solar_energy = plant.max_solar
		player.fertilizer_usage += sun_thirst


class Structure(object):
	pass
	
class Windmill(Structure):
	def __init__(self): 
		self.image = pygame.image.load(os.path.join("Art", "windmill.png")).convert()
		self.rect = self.image.get_rect(topleft = (10, 120))
		self.prop_image = pygame.image.load(os.path.join("Art", "propeller1.png")).convert()
		self.prop_rect = self.prop_image.get_rect(center = (self.rect.centerx, self.rect.top + 40))
		self.in_use = False
		self.angles = itertools.cycle([-22.5, -45, -67.5, 0])
	
	def update(self, surface, garden, player):
		if self.in_use:
			for plant in garden.plants:
				plant.water += 3
				player.water_usage += 3
			if garden.round_count % 10 == 0:
				self.prop_image = pygame.image.load(os.path.join("Art", "propeller1.png")).convert()
				self.prop_image = pygame.transform.rotate(self.prop_image, next(self.angles))
				self.prop_rect = self.prop_image.get_rect(center = (self.rect.centerx, self.rect.top + 40))
		self.prop_image.convert_alpha()
		self.prop_image.set_colorkey((157, 187, 97))
		surface.blit(self.image, self.rect)
		surface.blit(self.prop_image, self.prop_rect)
		
class Greenhouse(Structure):
	def __init__(self):
		self.growth = 0
		self.max_growth  =1000
		self.image = pygame.image.load(os.path.join("Art", "greenhouse.png")).convert()
		self.rect = self.image.get_rect(topleft = (40, 300))
	
	def update(self, surface):
		if self.growth < self.max_growth:
			self.growth += 1
		surface.blit(self.image, self.rect)
		pygame.draw.line(surface, Color("darkgreen"), (self.rect.left, self.rect.bottom + 5),
			(self.rect.left + (float(self.growth)/self.max_growth) * self.rect.width, self.rect.bottom + 5), 3)
	
	def give_seed(self, player):
		seed = random.choice(player.seeds.keys())
		player.seeds[seed] += 1
		self.growth = 0

class Pig(object):
	def __init__(self, pigpen):
		self.image = pygame.image.load(os.path.join("Art", "pigright.png")).convert()
		self.rect = self.image.get_rect(center = pigpen.rect.center)
		self.direction = "right"
		self.speed = 1
	
	def update(self, surface, pigpen, garden):
		directions = ["up", "down", "left", "right"]
		if garden.round_count % 2 == 0:
			if random.randint(1, 10) < 2:
				self.direction = random.choice(directions)
			if self.direction == "up" and self.rect.top < pigpen.rect.top + 10:
				self.direction = "down"
			elif self.direction == "down" and self.rect.bottom > pigpen.rect.bottom - 10:
				self.direction = "up"
			elif self.direction == "left" and self.rect.left < pigpen.rect.left + 12:
				self.direction = "right"
			elif self.direction == "right" and self.rect.right > pigpen.rect.right - 10:
				self.direction = "left"
			if self.direction == "up":
				self.rect.centery -= self.speed
			elif self.direction == "down":
				self.rect.centery += self.speed
			elif self.direction == "left":
				self.rect.centerx -= self.speed
			elif self.direction == "right":
				self.rect.centerx += self.speed
		self.image = pygame.image.load(os.path.join("Art", "pig" + self.direction + ".png")).convert()
		#self.image.convert_alpha()
		self.image.set_colorkey((157, 187, 97))
		surface.blit(self.image, self.rect)
			
class Pigpen(Structure):
	def __init__(self):
		self.image = pygame.image.load(os.path.join("Art", "pigpen.png")).convert()
		self.rect = self.image.get_rect(topleft = (10, 450))
		self.pigs = []
	
	def update(self, surface, garden):
		surface.blit(self.image, self.rect)
		for pig in self.pigs:
			pig.update(surface, self, garden)