import sys
import os
import random
from random import randint
import time
import itertools
import pickle
import pygame
from pygame.locals import *
from pygame import Color
import climate
import garden_tools
import garden_player
import garden_levels
import gardens

pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode((1080, 740))
SURF = DISPLAYSURF.convert_alpha()
SURF.set_colorkey((157, 187, 97))
pygame.display.set_caption("Garden")
FPS = 60
fpsClock = pygame.time.Clock()
SCREENWIDTH = 1080
HALFWIDTH = SCREENWIDTH / 2
SCREENHEIGHT = 740
HALFHEIGHT = SCREENHEIGHT / 2
text12 = pygame.font.Font("freesansbold.ttf", 12)
text14 = pygame.font.Font("freesansbold.ttf", 14)
text16 = pygame.font.Font("freesansbold.ttf", 16)
text18 = pygame.font.Font("freesansbold.ttf", 18)
text20 = pygame.font.Font("freesansbold.ttf", 20)
text24 = pygame.font.Font("freesansbold.ttf", 24)
text32 = pygame.font.Font("freesansbold.ttf", 32)
text48 = pygame.font.Font("freesansbold.ttf", 48)
text64 = pygame.font.Font("freesansbold.ttf", 64)
		
def show_mouse_cursor(surface, current_tool):
	if current_tool == None:
		return False
	mousex, mousey = pygame.mouse.get_pos()
	if mousey > SCREENHEIGHT - 85:
		pygame.mouse.set_visible(True)
		current_tool.in_use = False
	else:
		pygame.mouse.set_visible(False)
		mouse_icon = current_tool.image
		mouse_rect = mouse_icon.get_rect(center = (mousex, mousey))
		mouse_surf = pygame.Surface((mouse_rect.width, mouse_rect.height))
		mouse_surf.convert_alpha()
		mouse_surf.set_colorkey((157, 187, 97))
		mouse_surf.blit(mouse_icon, (0, 0))		
		surface.blit(mouse_surf, mouse_rect)

def warning_window(surface):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(300, 120, 400, 400)
	text = text24.render("Are you sure?", True, Color("black"))
	text_rect = text.get_rect(center = window.center)
	yes = text20.render("Yes", True, Color("blue"), Color("lightgray"))
	yes_rect = yes.get_rect(bottomleft = (window.left + 80, window.bottom - 50))
	no = text20.render("No", True, Color("red"), Color("lightgray"))
	no_rect = yes.get_rect(bottomright = (window.right - 80, window.bottom - 50))
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if yes_rect.collidepoint(x, y):
					return True
				elif no_rect.collidepoint(x, y):
					return False
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		surface.blit(text, text_rect)
		surface.blit(yes, yes_rect)
		surface.blit(no, no_rect)
		pygame.display.update()
		fpsClock.tick(FPS)
		
def hud(surface, screenwidth, screenheight, line_color, left_color, right_color, x):
	pygame.draw.line(surface, line_color, (0, screenheight - 82), (screenwidth, screenheight - 82), 3)
	pygame.draw.line(surface, line_color, (251, screenheight - 82), (251, screenheight), 3)
	pygame.draw.line(surface, line_color, (x + 19, screenheight - 82), (x + 19, screenheight), 3)
	pygame.draw.rect(surface, left_color, (0, screenheight - 80, 250, 80))
	pygame.draw.rect(surface, right_color, (x + 22,	screenheight - 79, screenwidth - x + 22, 79))

def print_news(surface, garden):	
	vert = SCREENHEIGHT - 70
	while len(garden.news_queue) > 3:
		garden.news_queue = garden.news_queue[1:]
	for item in garden.news_queue:
		item_text = text14.render(item, True, Color("black"))
		item_text_rect = item_text.get_rect(topleft=(20, vert))
		surface.blit(item_text, item_text_rect)
		vert += item_text_rect.height + 5

def show_economy(surface, garden, player):
	day = text16.render("Day: {0}".format(garden.day_count), True, Color("black"))
	econ = text16.render("Economy: ", True, Color("black"))
	day_rect = day.get_rect(topleft = (20, 10))
	econ_rect = econ.get_rect(topleft = (20, day_rect.bottom + 10))
	econ_text = text16.render("{0}".format(garden.business_climate), True, garden.business_climates[garden.business_climate][3])
	econ_text_rect = econ_text.get_rect(topleft = (econ_rect.right, econ_rect.top))
	cash = text16.render("Cash: ", True, Color("black"))
	cash_rect = cash.get_rect(topleft = (20, econ_text_rect.bottom + 10))
	if player.cash >= 0:
		cash_num = text16.render("{0:.2f}".format(player.cash), True, Color("forestgreen"))
	else:
		cash_num = text16.render("${0:.2f}".format(player.cash), True, Color("maroon"))
	cash_num_rect = cash_num.get_rect(topleft = (cash_rect.right + 5, cash_rect.top))
	for item in [(day, day_rect),(econ, econ_rect),(econ_text, econ_text_rect),(cash, cash_rect),(cash_num, cash_num_rect)]:
		surface.blit(item[0], item[1])

def show_weather(surface, horiz, garden):
		for i in range(7):
			weather_icon = pygame.image.load(os.path.join("Art", garden.weather[garden.day_count + i] + ".png")).convert()
			weather_icon_rect = weather_icon.get_rect(topleft = (horiz, 10))
			surface.blit(weather_icon, weather_icon_rect)
			horiz += weather_icon_rect.width + 10

def show_graph(surface, screenwidth, garden, base, xscale, yscale, line_thickness):
	window = surface.get_rect()
	for crop in garden.crops:
		crop.graph_active = True
	while xscale * garden.day_count > screenwidth:
		xscale -= 1
	vert = base + 20
	horiz = window.left + 50
	for crop in garden.crops:
		crop.graph_text = text16.render(crop.caps_name, True, crop.color, Color("black"))
		crop.graph_text_rect = crop.graph_text.get_rect(topleft = (horiz, vert))
		vert += crop.graph_text_rect.height + 10
		if vert + crop.graph_text_rect.height + 10 > window.bottom - 30:
			vert = base + 20
			horiz += 100
	
	exit = text20.render("Exit", True, Color("blue"), Color("lightgray"))
	exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 20))
	instruct1 = text16.render("Click on a crop's name to toggle that line on the graph.", True, Color("white"))
	instruct1_rect = instruct1.get_rect(topleft = (exit_rect.right + 20, base + 50))
	instruct2 = text16.render("Use the arrow keys to expand or compress the graph.", True, Color("white"))
	instruct2_rect = instruct2.get_rect(topleft = (instruct1_rect.left, instruct1_rect.bottom + 20))
	all_off = text16.render("Hide All", True, Color("blue"), Color("lightgray"))
	all_off_rect = all_off.get_rect(bottomleft = (window.left + 200, window.bottom - 10))
	expandingx = False
	expandingy = False
	compressingx = False
	compressingy = False
	
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					return False
				elif all_off_rect.collidepoint(x, y):
					for crop in garden.crops:
						crop.graph_active = False
				for crop in garden.crops:
					if crop.graph_text_rect.collidepoint(x, y):
						crop.graph_active = not crop.graph_active
			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					expandingx = True
				elif event.key == K_UP:
					expandingy = True
				elif event.key == K_LEFT:
					compressingx = True
				elif event.key == K_DOWN:
					compressingy = True
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					expandingx = False
				elif event.key == K_UP:
					expandingy = False
				elif event.key == K_LEFT:
					compressingx = False
				elif event.key == K_DOWN:
					compressingy = False
		if expandingx:
			xscale += 1
		elif expandingy:
			yscale += .2
		elif compressingx and xscale > 0:
			xscale -= 1
		elif compressingy and yscale > 0:
			yscale -= .2
		
		surface.fill(Color("black"))
		for crop in garden.crops:
			if crop.graph_active:
				try:
					crop.points = [(point[0] * xscale, base - int(point[1] * yscale)) for point in garden.graph_data if point[2] == crop.color]
					pygame.draw.lines(surface, crop.color, False, crop.points, line_thickness)
				except ValueError:
					pass
		for crop in garden.crops:
			surface.blit(crop.graph_text, crop.graph_text_rect)
		for elem in [(exit, exit_rect),(instruct1, instruct1_rect),(instruct2, instruct2_rect),(all_off, all_off_rect)]:
			surface.blit(elem[0], elem[1])
		pygame.draw.line(surface, Color("white"), (window.left, base), (window.right, base))
		pygame.display.update()
		fpsClock.tick(FPS)

def make_funds(garden):
	for key in gardens.Fund.fund_goods:
		fund = gardens.Fund(key, garden)
		garden.funds.append(fund)

def contract_check(garden, player, surface, clock, frame_rate, big_font, med_font, small_font):
	for contract in player.contracts:
		if contract.day_due == garden.day_count:
			contract.call_due(garden, player, surface, clock, frame_rate, big_font, med_font, small_font)

def show_fund_graph(surface, screenwidth, garden, base, xscale, yscale, line_thickness):
	window = surface.get_rect()
	for fund in garden.funds:
		fund.graph_active = True
	while xscale * garden.day_count > screenwidth:
		xscale -= 1
	vert = base + 20
	horiz = window.left + 50
	for fund in garden.funds:
		fund.graph_active = True
		fund.graph_text = text16.render(fund.name, True, fund.color, Color("black"))
		fund.graph_text_rect = fund.graph_text.get_rect(topleft = (horiz, vert))
		vert += fund.graph_text_rect.height + 10
		if vert + fund.graph_text_rect.height + 10 > window.bottom - 50:
			vert = base + 20
			horiz += 80
	
	exit = text20.render("Exit", True, Color("blue"), Color("lightgray"))
	exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 20))
	instruct1 = text16.render("Click on a fund's name to toggle that line on the graph.", True, Color("white"))
	instruct1_rect = instruct1.get_rect(topleft = (exit_rect.right + 20, base + 50))
	instruct2 = text16.render("Use the arrow keys to expand or compress the graph.", True, Color("white"))
	instruct2_rect = instruct2.get_rect(topleft = (instruct1_rect.left, instruct1_rect.bottom + 20))
	all_off = text20.render("Hide All", True, Color("blue"), Color("lightgray"))
	all_off_rect = all_off.get_rect(bottomleft = (80, window.bottom - 20))
	expandingx = False
	expandingy = False
	compressingx = False
	compressingy = False
	
	while True:
		surface.fill(Color("black"))
		for fund in garden.funds:
			if fund.graph_active:
				try:
					fund.points = [(point[0] * xscale, base - int(point[1] * yscale)) for point in garden.fund_graph_data if point[2] == fund.color]
					pygame.draw.lines(surface, fund.color, False, fund.points, line_thickness)
				except ValueError:
					pass
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					return False
				elif all_off_rect.collidepoint(x, y):
					for fund in garden.funds:
						fund.graph_active = False
				else:
					for fund in garden.funds:
						if fund.graph_text_rect.collidepoint(x, y):
							fund.graph_active = not fund.graph_active
			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					expandingx = True
				elif event.key == K_UP:
					expandingy = True
				elif event.key == K_LEFT:
					compressingx = True
				elif event.key == K_DOWN:
					compressingy = True
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					expandingx = False
				elif event.key == K_UP:
					expandingy = False
				elif event.key == K_LEFT:
					compressingx = False
				elif event.key == K_DOWN:
					compressingy = False
		if expandingx:
			xscale += 1
		elif expandingy:
			yscale += .2
		elif compressingx and xscale > 0:
			xscale -= 1
		elif compressingy and yscale > 0:
			yscale -= .2
		for fund in garden.funds:
			surface.blit(fund.graph_text, fund.graph_text_rect)
		surface.blit(exit, exit_rect)
		surface.blit(instruct1, instruct1_rect)
		surface.blit(instruct2, instruct2_rect)
		surface.blit(all_off, all_off_rect)
		pygame.draw.line(surface, Color("white"), (window.left, base), (window.right, base))
		pygame.display.update()
		fpsClock.tick(FPS)

			
def finance_screen(surface, screenwidth, left, top, width, height, player, garden):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(left, top, width, height)
	revenue = text16.render("Revenues", True, Color("white"), Color("black"))
	revenue_rect = revenue.get_rect(topleft = (window.left + 10, window.top + 10))
	sales = text14.render("Crop Sales", True, Color("white"), Color("black"))
	sales_rect = sales.get_rect(topleft = (revenue_rect.left + 10, revenue_rect.bottom + 10))
	sales2 = text14.render("Contract Sales", True, Color("white"), Color("black"))
	sales2_rect = sales2.get_rect(topleft = (sales_rect.left, sales_rect.bottom + 5))
	expend = text16.render("Expenses", True, Color("white"), Color("black"))
	expend_rect = expend.get_rect(topleft = (window.left + 10, sales2_rect.bottom + 10))
	water = text14.render("Water", True, Color("white"), Color("black"))
	water_rect = water.get_rect(topleft = (expend_rect.left + 10, expend_rect.bottom + 5))
	manure = text14.render("Manure", True, Color("white"), Color("black"))
	manure_rect = manure.get_rect(topleft = (water_rect.left, water_rect.bottom + 5))
	fert = text14.render("Fertilizer", True, Color("white"), Color("black"))
	fert_rect = fert.get_rect(topleft = (water_rect.left, manure_rect.bottom + 5))
	seed = text14.render("Seeds", True, Color("white"), Color("black"))
	seed_rect = seed.get_rect(topleft = (water_rect.left, fert_rect.bottom + 5))
	equip = text14.render("Equipment", True, Color("white"), Color("black"))
	equip_rect = equip.get_rect(topleft = (water_rect.left, seed_rect.bottom + 5))
	penalties = text14.render("Contract Penalties", True, Color("white"), Color("black"))
	penalties_rect = penalties.get_rect(topleft = (water_rect.left, equip_rect.bottom + 5))
	profit = text14.render("Operating Profit", True, Color("white"), Color("black"))
	profit_rect = profit.get_rect(topleft = (water_rect.left - 10, penalties_rect.bottom + 10))
	fsales = text14.render("Index Fund Sales", True, Color("white"), Color("black"))
	fsales_rect = fsales.get_rect(topleft = (window.left + 15, profit_rect.bottom + 5))	
	fpurch = text14.render("Index Fund Purchases", True, Color("white"), Color("black"))
	fpurch_rect = fpurch.get_rect(topleft = (window.left + 15, fsales_rect.bottom + 5))
	fprofit = text14.render("Index Fund Profits", True, Color("white"), Color("black"))
	fprofit_rect = fprofit.get_rect(topleft = (window.left + 10, fpurch_rect.bottom + 5))
	asset = text16.render("Assets", True, Color("white"), Color("black"))
	asset_rect = asset.get_rect(topleft = (expend_rect.left, fprofit_rect.bottom + 10))
	cash = text14.render("Cash", True, Color("white"), Color("black"))
	cash_rect = cash.get_rect(topleft = (asset_rect.left + 10, asset_rect.bottom + 5))
	crop_text = text14.render("Crops", True, Color("white"), Color("black"))
	crop_text_rect = crop_text.get_rect(topleft = (cash_rect.left, cash_rect.bottom + 5))
	share_text = text14.render("Index Funds", True, Color("white"), Color("black"))
	share_text_rect = share_text.get_rect(topleft = (cash_rect.left, crop_text_rect.bottom + 5))
	liab = text14.render("Liabilities", True, Color("white"), Color("black"))
	liab_rect = liab.get_rect(topleft = (expend_rect.left, share_text_rect.bottom + 10))
	contract_liab = text14.render("Contracts", True, Color("white"), Color("black"))
	contract_liab_rect = contract_liab.get_rect(topleft = (liab_rect.left + 10, liab_rect.bottom + 5))
	net = text14.render("Net Worth", True, Color("white"), Color("black"))
	net_rect = net.get_rect(topleft = (water_rect.left -10, contract_liab_rect.bottom + 10))
	
	exit = text20.render("EXIT", True, Color("blue"), Color("lightgray"))
	exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 10))
	contract_text = text16.render("View Contracts", True, Color("blue"), Color("lightgray"))
	contract_text_rect = contract_text.get_rect(bottomright = (exit_rect.left - 20, exit_rect.top - 20))
	fund_text = text16.render("Index Funds", True, Color("blue"), Color("lightgray"))
	fund_rect = fund_text.get_rect(bottomleft = (exit_rect.right + 20, exit_rect.top - 20))
	crop_total = 0
	for key in garden.prices:
		if key in ["water", "manure", "fertilizer"]:
			pass
		else:
			crop_total += garden.prices[key] * player.crops[key]
	
	contracts_total = 0
	for contract in player.contracts:
		contracts_total += contract.price * contract.amount * .1
	while True:
		funds_total = 0
		for fund in garden.funds:
			funds_total += player.fund_shares[fund.name] * fund.price
		sales_num = text14.render("{0:.2f}".format(player.tot_crop_sales), True, Color("darkgreen"), Color("black"))
		sales_num_rect = sales_num.get_rect(topright = (window.left + 350, sales_rect.top)) 
		sales2_num = text14.render("{0:.2f}".format(player.tot_contract_sales), True, Color("darkgreen"), Color("black"))
		sales2_num_rect = sales2_num.get_rect(topright = (sales_num_rect.right, sales2_rect.top))
		
		water_num = text14.render("{0:.2f}".format(player.tot_water_usage), True, Color("red"), Color("black"))
		water_num_rect = water_num.get_rect(topright = (sales_num_rect.right, water_rect.top)) 
		manure_num = text14.render("{0:.2f}".format(player.tot_manure_usage), True, Color("red"), Color("black"))
		manure_num_rect = manure_num.get_rect(topright = (sales_num_rect.right, manure_rect.top)) 
		fert_num = text14.render("{0:.2f}".format(player.tot_fertilizer_usage), True, Color("red"), Color("black"))
		fert_num_rect = fert_num.get_rect(topright = (sales_num_rect.right, fert_rect.top)) 
		seed_num = text14.render("{0:.2f}".format(player.tot_seed_usage), True, Color("red"), Color("black"))
		seed_num_rect = seed_num.get_rect(topright = (sales_num_rect.right, seed_rect.top)) 
		equip_num = text14.render("{0:.2f}".format(player.tot_equip_usage), True, Color("red"), Color("black"))
		equip_num_rect = equip_num.get_rect(topright = (sales_num_rect.right, equip_rect.top)) 
		penalties_num = text14.render("{0:.2f}".format(player.tot_contract_penalties), True, Color("red"), Color("black"))
		penalties_num_rect = penalties_num.get_rect(topright = (sales_num_rect.right, penalties_rect.top))
		tot_profit = player.tot_crop_sales + player.tot_contract_sales + -player.tot_water_usage +\
					-player.tot_manure_usage + -player.tot_fertilizer_usage + -player.tot_seed_usage +\
					-player.tot_equip_usage
		if tot_profit < 0:
			profit_num = text14.render("{0:.2f}".format(tot_profit), True, Color("red"), Color("black"))
		else:
			profit_num = text14.render("{0:.2f}".format(tot_profit), True, Color("darkgreen"), Color("black"))
		profit_num_rect = profit_num.get_rect(topright = (sales_num_rect.right, profit_rect.top))
		fsales_num = text14.render("{0:.2f}".format(player.fund_sales), True, Color("darkgreen"), Color("black"))
		fsales_num_rect = fsales_num.get_rect(topright = (window.left + 350, fsales_rect.top)) 
		fpurch_num = text14.render("{0:.2f}".format(player.fund_purchases), True, Color("red"), Color("black"))
		fpurch_num_rect = fpurch_num.get_rect(topright = (window.left + 350, fpurch_rect.top)) 
		if player.fund_sales >= player.fund_purchases:
			fprofit_num = text14.render("{0:.2f}".format(player.fund_sales - player.fund_purchases), True, Color("darkgreen"), Color("black"))
		else:
			fprofit_num = text14.render("{0:.2f}".format(player.fund_purchases - player.fund_sales), True, Color("red"), Color("black"))
		fprofit_num_rect = fprofit_num.get_rect(topright = (window.left + 350, fprofit_rect.top))
		if player.cash < 0:
			cash_num = text14.render("{0:.2f}".format(player.cash), True, Color("red"), Color("black"))
		else:
			cash_num = text14.render("{0:.2f}".format(player.cash), True, Color("darkgreen"), Color("black"))
		cash_num_rect = cash_num.get_rect(topright = (sales_num_rect.right, cash_rect.top))
		crop_num = text14.render("{0:.2f}".format(crop_total), True, Color("darkgreen"), Color("black"))
		crop_num_rect = crop_num.get_rect(topright = (sales_num_rect.right, crop_text_rect.top))
		funds_num = text14.render("{0:.2f}".format(funds_total), True, Color("darkgreen"), Color("black"))
		funds_num_rect = funds_num.get_rect(topright = (sales_num_rect.right, share_text_rect.top))
		contracts_num = text14.render("{0:.2f}".format(contracts_total), True, Color("red"), Color("black"))
		contracts_num_rect = contracts_num.get_rect(topright = (sales_num_rect.right, contract_liab_rect.top))
		net_total = player.cash + crop_total + funds_total - contracts_total
		if net_total < 0:
			net_num = text14.render("{0:.2f}".format(net_total), True, Color("red"), Color("black"))
		else:
			net_num = text14.render("{0:.2f}".format(net_total), True, Color("darkgreen"), Color("black"))
		net_num_rect = net_num.get_rect(topright = (sales_num_rect.right, net_rect.top))
		blit_rects = [(revenue, revenue_rect), (sales, sales_rect), (sales2, sales2_rect), (fsales, fsales_rect),
			(fpurch, fpurch_rect), (fprofit, fprofit_rect),(expend, expend_rect), (water, water_rect), (manure, manure_rect),
			(fert, fert_rect), (seed, seed_rect), (equip, equip_rect), (penalties, penalties_rect),
			(sales_num, sales_num_rect), (sales2_num, sales2_num_rect), (fsales_num, fsales_num_rect),
			(fpurch_num, fpurch_num_rect), (fprofit_num, fprofit_num_rect), (water_num, water_num_rect),
			(manure_num, manure_num_rect), (fert_num, fert_num_rect), (seed_num, seed_num_rect),
			(equip_num, equip_num_rect), (penalties_num, penalties_num_rect), (profit, profit_rect),
			(contract_text, contract_text_rect), (fund_text, fund_rect), (profit_num, profit_num_rect),
			(cash, cash_rect), (asset, asset_rect), (crop_text, crop_text_rect), (share_text, share_text_rect),
			(liab, liab_rect), (contract_liab, contract_liab_rect), (net, net_rect),(cash_num, cash_num_rect),
			(crop_num, crop_num_rect), (funds_num, funds_num_rect), (contracts_num, contracts_num_rect), (net_num, net_num_rect)] 
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					return False
				
				elif contract_text_rect.collidepoint(x, y):
					contracting = True
					while contracting:
						title = text24.render("Open Contracts", True, Color("black"))
						title_rect = title.get_rect(midtop = (window.centerx, window.top + 10))
						leave = text18.render("Exit", True, Color("blue"), Color("lightgray"))
						leave_rect = leave.get_rect(midbottom = (window.centerx, window.bottom - 10))
						vert = title_rect.bottom + 50
						blitters = [(title, title_rect), (leave, leave_rect)]
						for item in player.contracts:
							item.text = text18.render("{0} {1} @  ${2:.2f} in {3} days".format(item.amount,
													item.crop, item.price, item.day_due - garden.day_count),
													True, Color("black"), Color("white"))
							item.rect = item.text.get_rect(topleft = (window.left + 50, vert))
							blitters.append((item.text, item.rect))
							vert += item.rect.height + 20
						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN:
								x, y = event.pos
								if leave_rect.collidepoint(x, y):
									contracting = False
						
						pygame.draw.rect(surface, Color("white"), window) 
						pygame.draw.rect(surface, Color("gray"), window, 5)
						for item in blitters:
							surface.blit(item[0], item[1])
						pygame.display.update()
						fpsClock.tick(FPS)
				
				elif fund_rect.collidepoint(x, y):
					title = text24.render("Index Funds", True, Color("black"))
					title_rect = title.get_rect(midtop = (window.centerx, window.top + 10))
					price_text = text16.render("Current Price", True, Color("black"), Color("white"))
					price_text_rect = price_text.get_rect(topleft = (window.left + 135, title_rect.bottom + 20))
					shares_text = text16.render("Shares Held", True, Color("black"), Color("white"))
					shares_text_rect = shares_text.get_rect(topleft = (price_text_rect.right + 20, title_rect.bottom + 20))
					leave = text18.render("Exit", True, Color("blue"), Color("lightgray"))
					leave_rect = leave.get_rect(midbottom = (window.centerx, window.bottom - 10))
					pricehist = text18.render("View Price History", True, Color("blue"), Color("lightgray"))
					pricehist_rect = pricehist.get_rect(bottomleft = (window.left + 50, leave_rect.top - 20)) 
					blitters = [(title, title_rect), (leave, leave_rect), (shares_text, shares_text_rect),
								(pricehist, pricehist_rect), (price_text, price_text_rect)]
					funding = True
					while funding:
						vert = shares_text_rect.bottom + 10
						for fund in garden.funds:
							fund.name_text = text18.render("{0}".format(fund.name), True, Color("black"))
							fund.name_text_rect = fund.name_text.get_rect(topleft = (window.left + 50, vert))
							fund.price_num = text18.render("{0:.2f}".format(fund.price), True, Color("black"), Color("white"))
							fund.price_num_rect = fund.price_num.get_rect(topright = (price_text_rect.right - 20, fund.name_text_rect.top))
							fund.held = text18.render("{0}".format(player.fund_shares[fund.name]), True, Color("black"), Color("white"))
							fund.held_rect = fund.held.get_rect(topright = (shares_text_rect.right - 40, vert))
							fund.sell_all = text18.render("Sell All", True, Color("blue"), Color("lightgray"))
							fund.sell_all_rect = fund.sell_all.get_rect(topright = (window.right -10, fund.name_text_rect.top))
							fund.sell = text18.render("Sell", True, Color("blue"), Color("lightgray"))
							fund.sell_rect = fund.sell.get_rect(topright = (fund.sell_all_rect.left - 10, fund.name_text_rect.top))
							fund.buy5 = text18.render("Buy 5", True, Color("blue"), Color("lightgray"))
							fund.buy5_rect = fund.buy5.get_rect(topright = (fund.sell_rect.left - 10, fund.name_text_rect.top))
							fund.buy = text18.render("Buy", True, Color("blue"), Color("lightgray"))
							fund.buy_rect = fund.buy.get_rect(topright = (fund.buy5_rect.left - 10, fund.name_text_rect.top))
							vert += fund.name_text_rect.height + 20
						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN:
								x, y = event.pos
								if leave_rect.collidepoint(x, y):
									funding = False
								elif pricehist_rect.collidepoint(x, y):
									show_fund_graph(DISPLAYSURF, SCREENWIDTH, garden, 600, 20, 3, 2)
								for fund in garden.funds:
									if fund.buy_rect.collidepoint(x, y):
										if player.cash >= fund.price:
											player.fund_shares[fund.name] += 1
											player.cash -= fund.price
											player.fund_purchases += fund.price
									elif fund.buy5_rect.collidepoint(x, y):
										if player.cash >= fund.price * 5:
											player.fund_shares[fund.name] += 5
											player.cash -= fund.price * 5
											player.fund_purchases += fund.price * 5
									elif fund.sell_rect.collidepoint(x, y) and player.fund_shares[fund.name] > 0:
										player.fund_shares[fund.name] -= 1
										player.cash += fund.price
										player.fund_sales += fund.price
									elif fund.sell_all_rect.collidepoint(x, y) and player.fund_shares[fund.name] > 0:
										player.cash += player.fund_shares[fund.name] * fund.price
										player.fund_sales += player.fund_shares[fund.name] * fund.price
										player.fund_shares[fund.name] = 0
										
						pygame.draw.rect(surface, Color("white"), window) 
						pygame.draw.rect(surface, Color("gray"), window, 5)
						for item in blitters:
							surface.blit(item[0], item[1])
						for fund in garden.funds:
							for elem in [(fund.name_text, fund.name_text_rect), (fund.price_num, fund.price_num_rect),
								(fund.held, fund.held_rect), (fund.buy, fund.buy_rect), (fund.buy5, fund.buy5_rect)]:
								surface.blit(elem[0], elem[1])
							if player.fund_shares[fund.name] > 0:
								surface.blit(fund.sell_all, fund.sell_all_rect)
								surface.blit(fund.sell, fund.sell_rect)
						pygame.display.update()
						fpsClock.tick(FPS)
						
		pygame.draw.rect(surface, Color("black"), window) 
		pygame.draw.rect(surface, Color("gray"), window, 5)
		for rect in blit_rects:
			surface.blit(rect[0], rect[1])
		surface.blit(exit, exit_rect)
		pygame.display.update()
		fpsClock.tick(FPS)
		
		
def seed_screen(surface, left, top, width, height, player, garden, current_plant_type):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(left, top, width, height)
	seed_text = text18.render("Seed", True, Color("black"), Color("white"))
	seed_rect = seed_text.get_rect(topleft = (window.left + 50, window.top + 10))
	price_text = text18.render("Price", True, Color("black"), Color("white"))
	price_rect = price_text.get_rect(topleft = (190 + window.left, window.top + 10))
	inventory_text = text18.render("Invty", True, Color("black"), Color("white"))
	inventory_rect = inventory_text.get_rect(topleft = (290 + window.left, window.top + 10))	
	cash_text = text18.render("Cash:", True, Color("black"), Color("white"))
	cash_rect = cash_text.get_rect(bottomleft = (window.left + 10, window.bottom - 10))
	exit_text = text18.render("EXIT", True, Color("blue"), Color("lightgray"))
	exit_rect = exit_text.get_rect(midbottom = (window.width / 2 + left, window.height - 20 + top))
	
	seeding = True
	while seeding:
		if player.cash < 0:
			cash_amount = text18.render("{0:.2f}".format(player.cash), True, Color("maroon"), Color("white"))
		else:
			cash_amount = text18.render("{0:.2f}".format(player.cash), True, Color("forestgreen"), Color("white"))
		amount_rect = cash_amount.get_rect(topleft = (cash_rect.right + 5, cash_rect.top))
		
		vert = seed_rect.height + 30
		for crop in garden.crops:
			crop.name_text = text14.render(crop.caps_name, True, Color("black"), Color("white"))
			crop.name_rect = crop.name_text.get_rect(topleft = (window.left + 50, window.top + vert))
			crop.price_text = text14.render("{0:.2f}".format(garden.seed_prices[crop.name]), True, Color("black"), Color("white"))
			crop.price_rect = crop.price_text.get_rect(topleft = (190 + window.left, window.top + vert))
			crop.inv_text = text14.render(str(player.seeds[crop.name]), True, Color("black"))
			crop.inv_rect = crop.inv_text.get_rect(topleft = (310 + window.left, vert + window.top))
			if player.cash >= garden.seed_prices[crop.name]:
				crop.buy_text = text14.render("Buy", True, Color("forestgreen"), Color("lightgray"))
			else:
				crop.buy_text = text14.render("Buy", True, Color("maroon"), Color("lightgray"))
			
			crop.buy_rect = crop.buy_text.get_rect(topleft = (400 + window.left, vert + window.top))
			if player.seeds[crop.name] > 0:
				crop.select_text = text14.render("Select", True, Color("forestgreen"), Color("lightgray"))
			else:
				crop.select_text = text14.render("Select", True, Color("maroon"), Color("lightgray"))
			crop.select_rect = crop.select_text.get_rect(topleft = (crop.buy_rect.right + 20, crop.buy_rect.top))
			vert += crop.name_rect.height + 10
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					return current_plant_type
				for crop in garden.crops:
					if crop.buy_rect.collidepoint(x, y) and player.cash >= garden.seed_prices[crop.name]:
						player.seeds[crop.name] += 1
						player.cash -= garden.seed_prices[crop.name]
						player.tot_seed_usage += garden.seed_prices[crop.name]
						current_plant_type = crop.__class__
					elif crop.select_rect.collidepoint(x, y) and player.seeds[crop.name] > 0:
						current_plant_type = crop.__class__
						return current_plant_type
						
		pygame.draw.rect(surface, Color("white"), window) 
		pygame.draw.rect(surface, Color("gray"), window, 5)
		blit_list = [(seed_text, seed_rect), (price_text, price_rect), (inventory_text, inventory_rect),
			(cash_text, cash_rect), (cash_amount, amount_rect),	(exit_text, exit_rect)]
		for item in blit_list:
			surface.blit(item[0], item[1])
		for crop in garden.crops:
			for elem in [(crop.name_text, crop.name_rect),(crop.price_text, crop.price_rect),(crop.inv_text, crop.inv_rect),
					(crop.buy_text, crop.buy_rect),	(crop.select_text, crop.select_rect)]:
				surface.blit(elem[0], elem[1])
		pygame.display.update()
		fpsClock.tick(FPS)
	
def market_screen(surface, screenwidth, left, top, width, height, player, garden):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(left, top, width, height)
	crop_text = text16.render("Crop", True, Color("black"), Color("white"))
	crop_rect = crop_text.get_rect(topleft = (window.left + 50, window.top + 10))
	price_text = text16.render("Price", True, Color("black"), Color("white"))
	price_rect = price_text.get_rect(topleft = (190 + window.left, window.top + 10))
	inventory_text = text16.render("Invty", True, Color("black"), Color("white"))
	inventory_rect = inventory_text.get_rect(topleft = (290 + window.left, window.top + 10))
	qty_text = text16.render("Qty Harvested", True, Color("black"), Color("white"))
	qty_rect = qty_text.get_rect(topleft = (inventory_rect.right + 20, inventory_rect.top))
	exit_text = text18.render("EXIT", True, Color("blue"), Color("gray"))
	exit_rect = exit_text.get_rect(midbottom = (window.centerx, window.bottom - 10))
	graph = text18.render("Crop Price Graph", True, Color("blue"), Color("lightgray"))
	graph_rect = graph.get_rect(bottomright = (window.centerx - 20, window.bottom - 37))
	contract = text18.render("Available Contracts", True, Color("blue"), Color("lightgray"))
	contract_rect = contract.get_rect(topleft = (graph_rect.right + 40, graph_rect.top))
	marketing = True
	while marketing:
		cash_text = text16.render("Cash:", True, Color("black"), Color("white"))
		cash_rect = cash_text.get_rect(bottomleft = (window.left + 10, window.bottom - 10))
		if player.cash < 0:
			cash_amount = text16.render("{0:.2f}".format(player.cash), True, Color("maroon"), Color("white"))
		else:
			cash_amount = text16.render("{0:.2f}".format(player.cash), True, Color("forestgreen"), Color("white"))
		amount_rect = cash_amount.get_rect(topleft = (cash_rect.right + 5, cash_rect.top))
		vert = crop_rect.bottom + 10
		for crop in garden.crops:
			crop.name_text = text14.render(crop.caps_name, True, Color("black"))
			crop.name_rect = crop.name_text.get_rect(topleft = (50 + window.left, vert))
			crop.price_text = text14.render("{0:.2f}".format(garden.prices[crop.name]), True, Color("black"))
			crop.price_rect = crop.price_text.get_rect(topleft = (200 + window.left, vert))
			crop.inv_text = text14.render(str(player.crops[crop.name]), True, Color("black"))
			crop.inv_rect = crop.inv_text.get_rect(topleft = (310 + window.left, vert))
			crop.qty_text = text14.render(str(player.crops_harvested[crop.name]), True, Color("black"), Color("white"))
			crop.qty_rect = crop.qty_text.get_rect(topright = (qty_rect.right - 30, vert))
			if player.crops[crop.name] < 1:
				crop.sell_text = text14.render("Sell", True, Color("maroon"), Color("lightgray"))
				crop.sell_all_text = text14.render("Sell All", True, Color("maroon"), Color("lightgray"))
			else:
				crop.sell_text = text14.render("Sell", True, Color("forestgreen"), Color("lightgray"))
				crop.sell_all_text = text14.render("Sell All", True, Color("forestgreen"), Color("lightgray"))
			
			crop.sell_all_rect = crop.sell_all_text.get_rect(topright=(window.right - 20, vert))
			crop.sell_rect = crop.sell_text.get_rect(topright = (crop.sell_all_rect.left - 10, vert))
			vert += crop.name_rect.height + 10
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					marketing = False
				elif graph_rect.collidepoint(x, y):
					show_graph(surface, screenwidth, garden, 500, 20, 3, 2)
				elif contract_rect.collidepoint(x, y):
					contracting = True
					while contracting:
						title = text24.render("Available Contracts", True, Color("black"))
						title_rect = title.get_rect(midtop = (window.centerx, window.top + 10))
						leave = text18.render("Exit", True, Color("blue"), Color("lightgray"))
						leave_rect = leave.get_rect(midbottom = (window.centerx, window.bottom - 10))
						vert = title_rect.bottom + 50
						blitters = [(title, title_rect), (leave, leave_rect)]
						for item in garden.daily_contracts:
							item.text = text18.render("{0} {1} @  ${2:.2f} in {3} days".format(item.amount, item.crop, item.price, item.length),
								True, Color("black"), Color("white"))
							item.rect = item.text.get_rect(topleft = (window.left + 50, vert))
							item.accept = text18.render("Accept Contract", True, Color("blue"), Color("lightgray"))
							item.accept_rect = item.accept.get_rect(topright = (window.right - 10, item.rect.top))
							blitters.append((item.text, item.rect))
							blitters.append((item.accept, item.accept_rect))
							vert += item.rect.height + 20
						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN:
								x, y = event.pos
								if leave_rect.collidepoint(x, y):
									contracting = False
								for item in garden.daily_contracts:
									if item.accept_rect.collidepoint(x, y):
										item.accept_contract(player)
										garden.daily_contracts.remove(item)
						
						pygame.draw.rect(surface, Color("white"), window) 
						pygame.draw.rect(surface, Color("gray"), window, 5)
						for item in blitters:
							surface.blit(item[0], item[1])
						pygame.display.update()
						fpsClock.tick(FPS)
						
				for crop in garden.crops:
					if crop.sell_rect.collidepoint(x, y) and player.crops[crop.name] > 0:
						player.crops[crop.name] -= 1
						player.cash += garden.prices[crop.name]
						player.tot_crop_sales += garden.prices[crop.name]
					elif crop.sell_all_rect.collidepoint(x, y) and player.crops[crop.name] > 0:
						player.cash += garden.prices[crop.name] * player.crops[crop.name]
						player.tot_crop_sales += garden.prices[crop.name] * player.crops[crop.name]
						player.crops[crop.name] = 0
						
		pygame.draw.rect(surface, Color("white"), window) 
		pygame.draw.rect(surface, Color("gray"), window, 5)
		to_blit = [ (crop_text, crop_rect), (price_text, price_rect), (inventory_text, inventory_rect),
			(qty_text, qty_rect), (cash_text, cash_rect), (cash_amount, amount_rect), (graph, graph_rect),
			(contract, contract_rect), (exit_text, exit_rect)]
		for item in to_blit:
			surface.blit(item[0], item[1])
		for crop in garden.crops:
			for elem in [(crop.name_text, crop.name_rect),(crop.price_text, crop.price_rect),(crop.inv_text, crop.inv_rect),
				(crop.qty_text, crop.qty_rect),(crop.sell_text, crop.sell_rect),(crop.sell_all_text, crop.sell_all_rect)]:
				surface.blit(elem[0], elem[1])
		pygame.display.update()
		fpsClock.tick(FPS)

def upgrade_screen(surface, screenwidth, left, top, width, height, player, garden):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(left, top, width, height)
	title = text24.render("Upgrades / Structures", True, Color("black"), Color("white"))
	title_rect  =title.get_rect(midtop = (window.centerx, window.top + 20))
	scoop_text = text18.render("Seed Scoop", True, Color("black"), Color("lightgray"))
	scoop_rect = scoop_text.get_rect(topleft = (window.left + 10, title_rect.bottom + 20))  
	scoop_price = text18.render("$100", True, Color("black"), Color("white"))
	scoop_price_rect = scoop_price.get_rect(topright = (window.left + 250, scoop_rect.top))
	scoop_comment = text14.render("- Harvests 2 - 4 seeds", True, Color("black"), Color("white"))
	scoop_comment_rect = scoop_comment.get_rect(topleft = (window.left + 300, scoop_rect.top))
	sieve_text = text18.render("Seed Sieve", True, Color("black"), Color("lightgray"))
	sieve_rect = sieve_text.get_rect(topleft = (scoop_rect.left, scoop_rect.bottom + 15))
	sieve_price = text18.render("$500", True, Color("black"), Color("white"))
	sieve_price_rect = sieve_price.get_rect(topright = (window.left + 250, sieve_rect.top))
	sieve_comment = text14.render("- Harvests 2 - 5 seeds", True, Color("black"), Color("white"))
	sieve_comment_rect = sieve_comment.get_rect(topleft = (window.left + 300, sieve_rect.top))
	crate_text = text18.render("Produce Crate", True, Color("black"), Color("lightgray"))
	crate_rect = crate_text.get_rect(topleft = (scoop_rect.left, sieve_rect.bottom + 15))
	crate_price = text18.render("$100", True, Color("black"), Color("white"))
	crate_price_rect = crate_price.get_rect(topright = (window.left + 250, crate_rect.top))
	crate_comment = text14.render("- Harvests 2 - 4 crops", True, Color("black"), Color("white"))
	crate_comment_rect = crate_comment.get_rect(topleft = (window.left + 300, crate_rect.top))
	barrow_text = text18.render("Wheelbarrow", True, Color("black"), Color("lightgray"))
	barrow_rect = barrow_text.get_rect(topleft = (scoop_rect.left, crate_rect.bottom + 15))
	barrow_price = text18.render("$500", True, Color("black"), Color("white"))
	barrow_price_rect = barrow_price.get_rect(topright = (window.left + 250, barrow_rect.top))
	barrow_comment = text14.render("- Harvests 2 - 5 crops", True, Color("black"), Color("white"))
	barrow_comment_rect = barrow_comment.get_rect(topleft = (window.left + 300, barrow_rect.top))
	mill_text = text18.render("Windmill", True, Color("black"), Color("lightgray"))
	mill_rect = mill_text.get_rect(topleft = (scoop_rect.left, barrow_rect.bottom + 15))
	mill_price = text18.render("$1000", True, Color("black"), Color("white"))
	mill_price_rect = mill_price.get_rect(topright = (window.left + 250, mill_rect.top))
	mill_comment = text14.render("- Provides water to plants", True, Color("black"), Color("white"))
	mill_comment_rect = mill_comment.get_rect(topleft = (window.left + 300, mill_rect.top))
	house_text = text18.render("Greenhouse", True, Color("black"), Color("lightgray"))
	house_rect = house_text.get_rect(topleft = (scoop_rect.left, mill_rect.bottom + 15))
	house_price = text18.render("$1000", True, Color("black"), Color("white"))
	house_price_rect = house_price.get_rect(topright = (window.left + 250, house_rect.top))
	house_comment = text14.render("- Periodically produces a random seed", True, Color("black"), Color("white"))
	house_comment_rect = house_comment.get_rect(topleft = (window.left + 300, house_rect.top))
	pen_text = text18.render("Pig Pen", True, Color("black"), Color("lightgray"))
	pen_rect = pen_text.get_rect(topleft = (scoop_rect.left, house_rect.bottom + 15))
	pen_price = text18.render("$1000", True, Color("black"), Color("white"))
	pen_price_rect = pen_price.get_rect(topright = (window.left + 250, pen_rect.top))
	pen_comment = text14.render("- Provides free manure", True, Color("black"), Color("white"))
	pen_comment_rect = pen_comment.get_rect(topleft = (window.left + 300, pen_rect.top))
	exit = text24.render("Exit", True, Color("blue"), Color("lightgray"))
	exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 10))
	instruct = text18.render("Click on an item's name to purchase", True, Color("black"), Color("white"))
	instruct_rect = instruct.get_rect(midbottom = (window.centerx, exit_rect.top - 30))
	blit_rects = [(title, title_rect), (scoop_text, scoop_rect), (scoop_price, scoop_price_rect), (scoop_comment, scoop_comment_rect),
		(sieve_text, sieve_rect), (sieve_price, sieve_price_rect), (sieve_comment, sieve_comment_rect),
		(crate_text, crate_rect), (crate_price, crate_price_rect), (crate_comment, crate_comment_rect), (barrow_text, barrow_rect),
		(barrow_price, barrow_price_rect), (barrow_comment, barrow_comment_rect), (mill_text, mill_rect), (mill_price, mill_price_rect),
		(mill_comment, mill_comment_rect), (house_text, house_rect), (house_price, house_price_rect), (house_comment, house_comment_rect),
		(pen_text, pen_rect), (pen_price, pen_price_rect), (pen_comment, pen_comment_rect), (exit, exit_rect), (instruct, instruct_rect)]
	upgrading = True
	while upgrading:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if scoop_rect.collidepoint(x, y) and player.cash >= 100:
					new_tool = garden_tools.SeedScoop()
					new_tool.Rect.topleft = garden.tools[2].Rect.topleft
					new_tool.surface.blit(new_tool.image, (0, 0))
					garden.tools[2] = new_tool 
					player.cash -= 100
					player.tot_equip_usage += 100
				elif sieve_rect.collidepoint(x, y) and player.cash >= 500:
					new_tool = garden_tools.SeedSieve()
					new_tool.Rect.topleft = garden.tools[2].Rect.topleft
					new_tool.surface.blit(new_tool.image, (0, 0))
					garden.tools[2] = new_tool 
					player.cash -= 500
					player.tot_equip_usage += 500
				elif crate_rect.collidepoint(x, y) and player.cash >= 100:
					new_tool = garden_tools.Crate()
					new_tool.Rect.topleft = garden.tools[1].Rect.topleft
					new_tool.surface.blit(new_tool.image, (0, 0))
					garden.tools[1] = new_tool 
					player.cash -= 100
					player.tot_equip_usage += 100
				elif barrow_rect.collidepoint(x, y) and player.cash >= 500:
					new_tool = garden_tools.Wheelbarrow()
					new_tool.Rect.topleft = garden.tools[1].Rect.topleft
					new_tool.surface.blit(new_tool.image, (0, 0))
					garden.tools[1] = new_tool 
					player.cash -= 500
					player.tot_equip_usage += 500
				elif mill_rect.collidepoint(x, y) and player.cash >= 1000 and not garden.has_windmill:
					garden.has_windmill = True
					player.cash -=  1000
					player.tot_equip_usage += 1000
				elif house_rect.collidepoint(x, y) and player.cash >= 1000 and not garden.has_greenhouse:
					garden.has_greenhouse = True
					player.cash -= 1000
					player.tot_equip_usage += 1000
				elif pen_rect.collidepoint(x, y) and player.cash >= 1000 and not garden.has_pigpen:
					garden.has_pigpen = True
					player.cash -= 1000
					player.tot_equip_usage += 1000
				elif exit_rect.collidepoint(x, y):
					upgrading = False
					
		pygame.draw.rect(surface, Color("white"), window) 
		pygame.draw.rect(surface, Color("gray"), window, 5)
		for rect in blit_rects:
			surface.blit(rect[0], rect[1])
		pygame.display.update()
		fpsClock.tick(FPS)

def win_screen(surface, player, level):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(300, 120, 400, 400)
	line1 = text24.render("Level Passed!", True, Color("black"), Color("white"))
	line1_rect = line1.get_rect(midtop = (window.centerx, window.top + 20))
	cont = text18.render("Next Level", True, Color("blue"), Color("lightgray"))
	cont_rect = cont.get_rect(midbottom = (window.centerx, window.bottom - 20))
	replay = text18.render("Replay Level", True, Color("blue"), Color("lightgray"))
	replay_rect = replay.get_rect(midbottom = (window.centerx, cont_rect.top - 20)) 
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if cont_rect.collidepoint(x, y):
					return True
				elif replay_rect.collidepoint(x, y):
					return False
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		surface.blit(line1, line1_rect)
		surface.blit(cont, cont_rect)
		surface.blit(replay, replay_rect)
		pygame.display.update()
		fpsClock.tick(FPS)
	
def fail_screen(surface):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(300, 120, 400, 400)
	line1 = text24.render("Level Failed", True, Color("black"), Color("white"))
	line1_rect = line1.get_rect(midtop = (window.centerx, window.top + 20))
	replay = text18.render("Replay Level", True, Color("blue"), Color("lightgray"))
	replay_rect = replay.get_rect(midbottom = (window.centerx,window.bottom - 20)) 
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if replay_rect.collidepoint(x, y):
					return False
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		surface.blit(line1, line1_rect)
		surface.blit(replay, replay_rect)
		pygame.display.update()
		fpsClock.tick(FPS)
	
def goals_screen(surface, level):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(300, 120, 400, 400)
	title = text24.render("Level {0}".format(level.num), True, Color("black"), Color("white"))
	title_rect = title.get_rect(midtop = (window.centerx, window.top + 20))
	days = text18.render("Days left: {0}".format(level.days), True, Color("black"), Color("white"))
	days_rect = days.get_rect(topleft = (window.left + 20, title_rect.bottom + 20))
	goals_title = text18.render("Goals", True, Color("black"), Color("white"))
	goals_title_rect = title.get_rect(midtop = (window.centerx, days_rect.bottom + 50))
	exit = text18.render("Exit", True, Color("blue"), Color("lightgray"))
	exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 20))
	blit_rects = [(title, title_rect), (days, days_rect),(goals_title, goals_title_rect), (exit, exit_rect)]
	vert = goals_title_rect.bottom + 20
	for goal in level.goals:
		goal_text = text18.render("{0}".format(goal), True, Color("black"), Color("white"))
		goal_rect = goal_text.get_rect(topleft = (window.left + 10, vert))
		blit_rects.append((goal_text, goal_rect))
		vert += goal_rect.height + 20
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_rect.collidepoint(x, y):
					return False
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		for item in blit_rects:
			surface.blit(item[0], item[1])
		pygame.display.update()
		fpsClock.tick(FPS)

def menu_screen(surface, left, top, width, height, player):
	pygame.mouse.set_visible(True)
	window = pygame.Rect(left, top, width, height)
	save = text24.render("Save Game", True, Color("blue"), Color("lightgray"))
	save_rect = save.get_rect(midtop = (window.centerx, window.top + 50))
	music_text = text24.render("Toggle Music", True, Color("blue"), Color("lightgray"))
	music_rect = music_text.get_rect( midtop = (window.centerx, save_rect.bottom + 50))
	leave = text24.render("Leave", True, Color("blue"), Color("lightgray"))
	leave_rect = leave.get_rect( midtop = (window.centerx, music_rect.bottom + 50))
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if save_rect.collidepoint(x, y):
					pickle.dump(player, open("garden_save.pickle", "wb"))
				elif music_rect.collidepoint(x, y):
					if player.music_on:
						pygame.mixer.music.pause()
						player.music_on = False
					else:
						pygame.mixer.music.unpause()
						player.music_on = True
				elif leave_rect.collidepoint(x, y):
					return 
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		surface.blit(save, save_rect)
		surface.blit(music_text, music_rect)
		surface.blit(leave, leave_rect)
		pygame.display.update()
		fpsClock.tick(FPS)

	
player = garden_player.Player()					

def level_loop(player):			
	level = garden_levels.level_map[player.level]()
	goals_screen(DISPLAYSURF, level)
	player.cash = level.starting_cash
	watering_can = garden_tools.WateringCan()
	basket = garden_tools.Basket()
	seed_bag = garden_tools.SeedBag()
	manure = garden_tools.Manure()
	fertilizer = garden_tools.Fertilizer()
	shovel = garden_tools.Shovel()		
	windmill = garden_tools.Windmill()
	greenhouse = garden_tools.Greenhouse()
	pigpen = garden_tools.Pigpen()
	for i in range(4):
		pig = garden_tools.Pig(pigpen)
		pigpen.pigs.append(pig)
	
	
	weather = climate.make_weather(180, climate.weather_events)
	plots = gardens.make_garden_plots("empty_plot.png", 30, 10, 180, 120, 20, 50)
	garden = gardens.Garden(weather, plots, gardens.crop_types, level.interest_rate)			
	climate.weather_check(garden)
	garden.make_daily_contracts()
	garden.tools = [watering_can, basket, seed_bag, manure, fertilizer, shovel]
	make_funds(garden)
	for fund in garden.funds:
		garden.fund_graph_data.append((0, fund.price, fund.color))
	garden.add_fund_data()
	for crop in garden.crops:
		garden.graph_data.append((0, garden.prices[crop.name], crop.color))
	current_tool = None
	current_plant_type = garden.crop_types[0]
	horiz = 270
	for tool in garden.tools:
		tool.Rect.topleft = (horiz, SCREENHEIGHT - tool.Rect.height - 10) 
		tool.surface.blit(tool.image, (0, 0))
		horiz += tool.Rect.width + 20
	market_text = text16.render("Market", True, Color("blue"), Color("gray"))
	market_rect = market_text.get_rect(topleft = (shovel.Rect.right + 70, shovel.Rect.top + 10))
	seeds_text = text16.render("Seeds", True, Color("blue"), Color("gray"))
	seeds_rect = market_text.get_rect(topleft = (market_rect.left, market_rect.bottom + 10))
	finance_text = text16.render("Finance", True, Color("blue"), Color("gray"))
	finance_rect = finance_text.get_rect(topleft = (market_rect.right + 30, market_rect.top))
	upgrade_text = text16.render("Upgrades", True, Color("blue"), Color("gray"))
	upgrade_rect = upgrade_text.get_rect(topleft = (market_rect.right + 30, finance_rect.bottom + 10))
	goal_text = text16.render("Goals", True, Color("blue"), Color("gray"))
	goal_rect = goal_text.get_rect(topleft = (finance_rect.right + 20, finance_rect.top))
	menu_text = text16.render("Menu", True, Color("blue"), Color("gray"))
	menu_rect = menu_text.get_rect(topleft = (goal_rect.left, seeds_rect.top))
	road1 = pygame.image.load(os.path.join("Art", "cobble_path.png")).convert()
	road1_rect = road1.get_rect(topleft = (160, 280))
	road2 = pygame.image.load(os.path.join("Art", "cobble_path.png")).convert()
	road2_rect = road2.get_rect(topleft = (160, 460))
	road3 = pygame.image.load(os.path.join("Art", "cobble_path.png")).convert()
	road3_rect = road3.get_rect(topleft = (160, 632))
	road4 = pygame.image.load(os.path.join("Art", "cobble_path_vert.png")).convert()
	road4_rect = road4.get_rect(topleft = (150, 250))
	path1 = pygame.image.load(os.path.join("Art", "cobble_path_short.png")).convert()
	path1_rect = path1.get_rect(topleft = (80, 250))
	path2 = pygame.image.load(os.path.join("Art", "cobble_path_short.png")).convert()
	path2_rect = path2.get_rect(topleft = (80, 425))
	path3 = pygame.image.load(os.path.join("Art", "cobble_path_short.png")).convert()
	path3_rect = path3.get_rect(topleft = (80, 585))
	fence1 = pygame.image.load(os.path.join("Art", "fence_horiz.png")).convert()
	fence1_rect = fence1.get_rect(bottomleft = (170, SCREENHEIGHT - 86)) 
	fence2 = pygame.image.load(os.path.join("Art", "fence_horiz.png")).convert()
	fence2_rect = fence2.get_rect(bottomleft = (170, 120)) 
	fence3 = pygame.image.load(os.path.join("Art", "fence_vert.png")).convert()
	fence3_rect = fence3.get_rect(topleft = (fence2_rect.right, fence2_rect.top))
	fence4 = pygame.image.load(os.path.join("Art", "fence_vert_left.png")).convert()
	fence4_rect = fence4.get_rect(topright = (fence2_rect.left, fence2_rect.top))
	for fence in [fence1, fence2, fence3, fence4]:
		fence.convert_alpha()
		fence.set_colorkey((157, 187, 97))
	garden.make_daily_contracts()
	
	
	while True:
		#start = time.time()
		if level.wincheck(player, garden):
			if win_screen(DISPLAYSURF, player, level):
				player.level += 1
			return False
		if level.failcheck():
			fail_screen(DISPLAYSURF)
			return False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.mixer.quit()
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				x, y = event.pos
				if market_rect.collidepoint(x, y):
					market_screen(DISPLAYSURF, SCREENWIDTH, 200, 10, 600, 720, player, garden)
				elif seeds_rect.collidepoint(x, y):
					current_plant_type = seed_screen(DISPLAYSURF, 200, 10, 600, 720, player, garden, current_plant_type)
				elif finance_rect.collidepoint(x, y):
					finance_screen(DISPLAYSURF, SCREENWIDTH, 200, 100, 600, 600, player, garden)
				elif upgrade_rect.collidepoint(x, y):
					upgrade_screen(DISPLAYSURF, SCREENWIDTH, 200, 100, 600, 600, player, garden)
				elif goal_rect.collidepoint(x, y):
					goals_screen(DISPLAYSURF, level)
				elif menu_rect.collidepoint(x, y):
					menu_screen(DISPLAYSURF,200, 100, 600, 600, player)
				if windmill.rect.collidepoint(x, y):
					windmill.in_use = not windmill.in_use
				elif greenhouse.rect.collidepoint(x, y):
					if greenhouse.growth >= greenhouse.max_growth:
						greenhouse.give_seed(player)
				for tool in garden.tools:
					if tool.Rect.collidepoint(x, y):
						current_tool = tool	
				if current_tool == shovel:
					for plot in garden.plots:
						if plot.Rect.collidepoint(x, y) and not plot.empty:
							for plant in garden.plants:
								if plant.Rect.collidepoint(plot.Rect.center):
									if warning_window(DISPLAYSURF):
										garden.plants.remove(plant)
										plot.empty = True
					
			elif event.type == MOUSEBUTTONDOWN and event.button == 3:
				if not current_tool == None:
					current_tool.in_use = True	
			elif event.type == MOUSEBUTTONUP and event.button == 3:
				if not current_tool == None:
					current_tool.in_use = False	
		
		mousex, mousey = pygame.mouse.get_pos()
		for plant in garden.plants:
			if plant.Rect.collidepoint(mousex, mousey):
				if watering_can.in_use:
					watering_can.use(player, plant)
				elif manure.in_use:
					manure.use(player, plant)
				elif fertilizer.in_use:
					fertilizer.use(player, plant)
				elif manure.in_use:
					manure.use(player, plant)
				elif garden.tools[2].in_use and plant.stage == 6:
					current_plant_type = garden.tools[2].use(player, plant, garden.plants, garden.plots, garden.news_queue, current_plant_type)
				elif garden.tools[1].in_use and plant.stage == 6:
					garden.tools[1].use(player, plant, garden.plants, garden.plots, garden.news_queue)
				break	
		if shovel.in_use:	
			for plot in garden.plots:
				if plot.Rect.collidepoint(mousex, mousey) and plot.empty and player.seeds[current_plant_type.name] > 0:
					new_plant = current_plant_type()
					new_plant.Rect.center = plot.Rect.center
					plot.empty = False
					garden.plants.append(new_plant)
					player.seeds[current_plant_type.name] -= 1
		if garden.round_count % (300) == 0: # 10 second day length at 30 FPS
			garden.day_count += 1
			level.days -= 1
			garden.make_daily_contracts()
			if garden.day_count % 3 == 0:
				garden.economy_check()
			garden.price_update()
			climate.weather_check(garden)
			garden.charge_interest(player)
			garden.charge_player_tab(player)
			contract_check(garden, player, DISPLAYSURF, fpsClock, FPS, text24, text18, text16)
			for crop in garden.crops:
				garden.graph_data.append((garden.day_count, garden.prices[crop.name], crop.color))
			garden.add_fund_data()
			if garden.day_count % 7 == 0:
				player.pay_bill(DISPLAYSURF, text24, text16, text18, fpsClock, FPS)
			
		
		SURF.fill(Color(157, 187, 97))
		show_economy(SURF, garden, player)
		show_weather(SURF, 285, garden)
		hud(SURF, SCREENWIDTH, SCREENHEIGHT, Color("gray"), Color("white"), Color("lightgray"), shovel.Rect.right)
		print_news(SURF, garden)
		dirty_rects = [(market_text, market_rect),(seeds_text, seeds_rect),(finance_text, finance_rect),
			(upgrade_text, upgrade_rect),(goal_text, goal_rect), (menu_text, menu_rect),(fence1, fence1_rect),(fence2, fence2_rect),
			(fence3, fence3_rect),(fence4, fence4_rect),(road1, road1_rect),(road2, road2_rect),(road3, road3_rect),
			(road4, road4_rect),(path1, path1_rect),(path2, path2_rect),(path3, path3_rect)]
		for elem in dirty_rects:
			SURF.blit(elem[0], elem[1])
		for tool in garden.tools:
			SURF.blit(tool.surface, tool.Rect)
		for plant in garden.plants:
			plant.update(SURF, garden)
		for plot in garden.plots:
			plot.update(SURF)
		if garden.has_windmill:
			windmill.update(SURF, garden, player)
		if garden.has_greenhouse:
			greenhouse.update(SURF)
		if garden.has_pigpen:
			pigpen.update(SURF, garden)
		show_mouse_cursor(SURF, current_tool)
		DISPLAYSURF.blit(SURF, (0, 0))
		pygame.display.update()
		fpsClock.tick(FPS)
		garden.round_count += 1
		#now = time.time()
		#print now - start
	

		
def new_game_screen():
	new = text64.render("New Game", True, Color("blue"), Color("gray"))
	newRect = new.get_rect()
	loadgame = text64.render("Load Game", True, Color("blue"), Color("gray"))
	loadRect = loadgame.get_rect()
	newRect.midbottom = (HALFWIDTH, HALFHEIGHT - 100)
	loadRect.midtop = (HALFWIDTH, HALFHEIGHT + 100)
	choosing = True
	while choosing:
		DISPLAYSURF.fill(Color("black"))
		DISPLAYSURF.blit(new, newRect)
		DISPLAYSURF.blit(loadgame, loadRect)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				if newRect.collidepoint(mousex, mousey):
					welcome(DISPLAYSURF, "Overview", [
							"Tend your crops and manage your finances to victory.",
							"Randomly generated weather and economic conditions", 
							"influence the growth of crops and the prices they sell at.",
							"The in-game menus can be accessed by left-clicking on the",
							"appropriate button at the bottom-right of the screen."])
					welcome(DISPLAYSURF, "Tools", [
							"Tools are selected by left-clicking on their icon.",
							"- Watering Can: Right-click to water a plant. Drag to",
							"  water multiple plants. You will be charged weekly",
							"  for your water use.",
							"- Shovel: Drag the right mouse button to plant the currently",
							"  selected seed (chosen from the Seeds menu or by harvesting).",
							"  Left-click on a plant to dig it up.",
							"- Seed Bag: Drag the right mouse button to harvest 1 - 4 seeds from",
							"  a mature plant. Harvesting seeds will destroy annuals. Perennials",
							"  will revert to immaturity and begin to grow again. This tool can",
							"  be upgraded through the Upgrades menu."])
					welcome(DISPLAYSURF, "Tools", [
							"- Produce Basket: Used the same way as the Seed Bag, but harvests",
							"  crops instead. Crops can be sold at market or used to fulfill",
							"  a contract. This tool can be upgraded through the Upgrades menu.",
							"- Manure: Manure can be applied to a plant once during its growth",
							"  cycle for $50. You will be charged weekly for your manure use.",
							"  Building a pig pen provides a free source of manure.",
							"- Fertilizer: Liquid Sunshine. Fertilizer costs can build up quickly,",
							"  so use it wisely. You will be charged weekly for fertilizer use."])
					welcome(DISPLAYSURF, "Contracts", [
							"Contracts are an agreement for you to provide a certain quantity of",
							"a crop on a specific date. Failure to fulfill the contract will result",
							"in a penalty of 10% of the contract value. Available contratcs change",
							"daily and can be found through the Market menu."])
					welcome(DISPLAYSURF, "Index Funds", [
							"Index Funds are investment instruments based on the average value of",
							"different crops which can be bought and sold like stocks. Index Funds",
							"are traded through the Finance menu where you can see the current prices",
							"as well as a graph of past fund performance."])
					welcome(DISPLAYSURF, "Upgrades", [
							"The Upgrades menu allows you to purchase better tools and improvements",
							"for your farm. Tool upgrades provide better harvests of seeds or crops",
							"and replace their less efficient counterparts. Structural upgrades",
							"provide unique benefits. A Windmill allows you to water all plants",
							"simultaneously regardless of their thirstiness while the windmill is",
							"spinning (left-click to toggle). A Greenhouse slowly produces random",
							"seeds. Left-click on the Greenhouse to harvest a mature seed.",				
							"A Pig Pen gives you unlimited manure for free. Each plant may still",
							"only be fertilized once during its growth cycle."])
					return garden_player.Player()
				elif loadRect.collidepoint(mousex, mousey):
					try:
						return pickle.load(open("garden_save.pickle", "rb"))
					except:
						pass
		pygame.display.update()
		fpsClock.tick(FPS)
		
def welcome(surface, header, lines):
	title = text48.render("Green Thumb Gardens", True, Color("white"), Color(157, 187, 97))
	title_rect = title.get_rect(midtop = (HALFWIDTH, 20))
	header_text = text32.render(header, True, Color("black"))
	header_rect = header_text.get_rect(midtop = (HALFWIDTH, title_rect.bottom + 50))
	go_on = text24.render("Click anywhere to continue", True, Color("white"))
	go_on_rect = go_on.get_rect(midbottom = (HALFWIDTH, SCREENHEIGHT - 20))
	blit_rects = [(title, title_rect), (header_text, header_rect), (go_on, go_on_rect)]
	vert = header_rect.bottom + 30
	for line in lines:
		line_text = text24.render(line, True, Color("black"))
		line_rect = line_text.get_rect(midtop = (HALFWIDTH, vert))
		blit_rects.append((line_text, line_rect))
		vert += line_rect.height + 20
	pygame.event.clear()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				return
		surface.fill(Color(157, 187, 97))
		for elem in blit_rects:
			surface.blit(elem[0], elem[1])
		pygame.display.update()
		fpsClock.tick(FPS)
		
def main(player):
	pygame.mixer.music.load("song1.mp3")
	pygame.mixer.music.play(-1)
	while True:
		pygame.mouse.set_visible(True)
		level_holder = player.level
		player = garden_player.Player()
		player.level = level_holder
		level_loop(player)
		
main(new_game_screen())