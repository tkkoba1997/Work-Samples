# cd Desktop\Technical\Personal Interest\Code\Python Code\Command Line Games\snake_development\snake_pygame

# Snake game implemented with pygame.
import sys, pygame, msvcrt, time, snake_functions, display_graphics

# Initialize pygame modules
pygame.init()

# Image file names
gameover = "images/game_over.png"
three = "images/num3.png"
two = "images/num2.png"
one = "images/num1.png"
go = "images/go.png"
explosion = "images/explosion3.png"

# Constructing the snake.
snk_sgmnt = pygame.image.load("images/segment2.png")	# Load snake segment image.
snk_sgmnt_rec = snk_sgmnt.get_rect()			# Create a rectangle (Rect) object representing the image
snk_arry = [snk_sgmnt_rec]						# Make an array with the rectangle in side
snake_len = 7									# Length of the snake, i.e, number of rectangles to make snake initially
while len(snk_arry) < snake_len:				# Loop till snake is desired initial length by lengthening snk_arry.
	snk_arry.append(snk_sgmnt_rec.copy())
	snk_arry[-1][0] = snk_arry[-2][0] + snk_arry[0][2] # Space each segment one width (snk_arry[0][2]) from its predecessor.

# Bolder image and rectangle
bolder = pygame.image.load("images/bolder.png")
bolder_rect = bolder.get_rect()
bolder_rect[2] = snk_sgmnt_rec[2]
bolder_rect[3] = snk_sgmnt_rec[3]

# Explosion gif for crashes
explosion = pygame.image.load(explosion)
explosion_rect = explosion.get_rect()
explosion_rect[2] = snk_sgmnt_rec[2]
explosion_rect[3] = snk_sgmnt_rec[3]

# Initial bolders = 0, start with an empty list.
bolder_array = []

# Initial snake travel direction
travel_direction = 'RIGHT'

# Window and game construction parameters. Should theoretically be dependent on rectangle dimensions returned
# by snk_sgmnt.get_rect() (line 16). The parameters lft_rgt_spaces & up_dwn_spaces determine how many spaces
# the snake can move around in. The valid number of spaces is lft_rgt_spaces * up_dwn_spaces.
lft_rgt_spaces = 16
up_dwn_spaces = 12
# Create size tuple that represents the window size produced by pygame and reflects
# how many spaces the snake how many left/right and up/down positions on the gameboard.
size = width, height = snk_sgmnt_rec[2]*lft_rgt_spaces, snk_sgmnt_rec[3]*up_dwn_spaces

# Black in RGB representation
black = 0, 0, 0	

# Speed parameters. Integer setting and time period.
spd_setting = 1
mvmnt_period  = 1 - spd_setting/8

# Update game setting parameters.
increase_speed = 20
add_boulder    = 7.5
lengthen_snake = 15

# Display the screen. 
screen = pygame.display.set_mode(size)

screen.fill(black)
pygame.display.flip()

# Create a 3-2-1-Go countdown before game starts. Maintain exit/quit capacity during this however.
countdown = [three, two, one, go]
for images in countdown:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    pygame.display.flip()
    time.sleep(0.25)
    display_graphics.display_centered_image(images, size, screen)
    time.sleep(0.5)

# Intially all the reference times are equal. The movement, game speedup, snake lengthen, and 
# obstacle addition times are all in reference to the same instance initially.
mvmnt_rfrnce_time = time.time()
incrse_spd_rfrnce_time = mvmnt_rfrnce_time
lngthn_snk_rfrnce_time = mvmnt_rfrnce_time
add_bldr_rfrnce_time = mvmnt_rfrnce_time
start_time = mvmnt_rfrnce_time

play = True
while play==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            travel_direction = snake_functions.determine_travel_direction(travel_direction, event)
        else: pass

    tail_position_rect = snk_arry[0]
    present_time = time.time()
    if present_time - mvmnt_rfrnce_time > mvmnt_period:
        snake_functions.reposition_snake(travel_direction, snk_arry)
        if present_time - lngthn_snk_rfrnce_time > lengthen_snake:
            snk_arry.insert(0, tail_position_rect)
            lngthn_snk_rfrnce_time = time.time()
        mvmnt_rfrnce_time = time.time()
    if (present_time - incrse_spd_rfrnce_time > increase_speed) and spd_setting < 7:
        spd_setting += 1
        mvmnt_period = 1 - spd_setting/8
        increase_speed += 5
        incrse_spd_rfrnce_time = time.time()
    if present_time - add_bldr_rfrnce_time > add_boulder:
        snake_functions.add_bolder(snk_arry, bolder_array, (lft_rgt_spaces, up_dwn_spaces), snk_sgmnt_rec[2], bolder_rect)
        add_bldr_rfrnce_time = time.time()

    # Display each snake segment individually after black screen.
    screen.fill(black)
    for rects in snk_arry:
        screen.blit(snk_sgmnt, rects)
    for rects in bolder_array:
        screen.blit(bolder, rects)
    pygame.display.flip()

    if snake_functions.crash_check(snk_arry, bolder_array, size):
        explosion_rect[0] = snk_arry[-2][0]
        explosion_rect[1] = snk_arry[-2][1]
        screen.blit(explosion, explosion_rect)
        pygame.display.flip()
        time.sleep(0.01)
        display_graphics.display_centered_image(gameover, size, screen)
        print(f"\nScore: {spd_setting**2 + len(bolder_array)*3 + len(snk_arry)*3}\t You survived {int((time.time()-start_time)//60)} minutes and {abs(start_time-time.time())%60:.0f} seconds.")
        time.sleep(2.5)
        sys.exit()