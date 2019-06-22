# cd Desktop\Technical\Personal Interest\Code\Python Code\Command Line Games\snake_development\snake_pygame
import random

def crash_check(snake_array, bolder_array, size):
	'''Returns True if snake has crashed. Uses resolution window sizes to check (crashes into walls). 
	Checks crashes into self by counting if same position occurs multiple times in snake chain. And checks for
	bolder crashes using 'in' operator.'''
	positions = []
	for rectangles in snake_array:
		positions.append( (rectangles[0], rectangles[1]) )
		if rectangles in bolder_array:
			return True
	for spots in range(0, len(positions)):
		if positions.count(positions[spots]) > 1:
			return True
	# Check if any of the walls have been crashed into. size[0] is width, size[1] is height.
	if snake_array[-1][0] < 0 or snake_array[-1][0] >= size[0]:
		return True
	elif snake_array[-1][1] < 0 or snake_array[-1][1] >= size[1]:
		return True
	return False

def determine_travel_direction(trvl_dir, keypressevent):
	'''This function determines if the up/down or left/right arrow keys were pressed. It then returns the 
	string representation of the snake's head's travel direction to reflect any changes.'''
	if keypressevent.key==273 and trvl_dir!='DOWN':
		return 'UP'
	elif keypressevent.key==274 and trvl_dir!='UP':
		return 'DOWN'
	elif keypressevent.key==275 and trvl_dir!='LEFT':
		return 'RIGHT'
	elif keypressevent.key==276 and trvl_dir!='RIGHT':
		return 'LEFT'
	return trvl_dir

def reposition_snake(trvl_dir, snk_arry):
	'''"Moves" each snake segment in appropriate direction. Method: (1) Attach new segment in front of the snake (index -1). (2) Move this newly
	attached section (head) one position over in travel_direction. (3) Delete tail section of snake (index 0) with snk_arry.pop(0) method.
	Creates an illusion of sequential snake movement.'''
	snk_arry.append(snk_arry[-1].copy())
	if trvl_dir == 'UP':
		snk_arry[-1][1] -= snk_arry[0][3]
	elif trvl_dir == 'DOWN': 
		snk_arry[-1][1] += snk_arry[0][3]
	elif trvl_dir == 'RIGHT':
		snk_arry[-1][0] += snk_arry[0][2] 
	elif trvl_dir == 'LEFT':
		snk_arry[-1][0] -= snk_arry[0][2]
	else:
		pass
	snk_arry.pop(0)

def add_bolder(snk_arry, bldr_array, game_dimensions_tuple, cube_side_len, bolder_rect):
	'''Adds a bolder to the snake gameboard in a space not occuppied by the snake and at least two spots away
	from the snake both vertically and horizontally.'''
	head_rect = snk_arry[-1]
	valid_spaces = game_dimensions_tuple[0] * game_dimensions_tuple[1]
	snk_rects = []
	bldr_rects = []
	for rectangle in range(0, len(snk_arry)):
		snk_rects.append( (snk_arry[rectangle][0], snk_arry[rectangle][1]))
	for rectangle in range(0, len(bldr_array)):
		bldr_rects.append( (bldr_array[rectangle][0], bldr_array[rectangle][1]) )
	while True:
		position = random.randint(1, valid_spaces)
		row = position // game_dimensions_tuple[0]
		column = position % game_dimensions_tuple[0]
		pxl_strtpnts = (horz_start, vert_start) = (row*cube_side_len, column*cube_side_len)
		if pxl_strtpnts not in snk_rects:
			if pxl_strtpnts not in bldr_rects:
				if abs(head_rect[0] - pxl_strtpnts[0]) > 2*cube_side_len:
					if abs(head_rect[1] - pxl_strtpnts[1]) > 2*cube_side_len:
						bldr_array.append(bolder_rect.copy())
						bldr_array[-1][0] = pxl_strtpnts[0]
						bldr_array[-1][1] = pxl_strtpnts[1]
						break