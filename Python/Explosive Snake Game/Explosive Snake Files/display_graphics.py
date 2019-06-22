import pygame
# Displaying graphics functions. Meant to work with already opened pygame screens.
def display_centered_image(image_str, size, screen):
	'''Given an image file name, the resolution size of an active pygame screen, and 
	the screen itself, this function displays the image centered in the screen. '''
	image = pygame.image.load(image_str)
	image_rect = image.get_rect()
	image_width = image_rect[2]
	image_height = image_rect[3]
	screen_center = (size[0]//2, size[1]//2)
	# Offset the corner of the image rectangle
	image_rect[0] = screen_center[0] - image_width//2
	image_rect[1] = screen_center[1] - image_height//2
	screen.blit(image, image_rect)
	pygame.display.flip()


