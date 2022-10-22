import random
import os
import time
import pygame

# Initialise pygame. Since the keyboard module is not working, we have to import pygame to handle input
pygame.init()
screen = pygame.display.set_mode((10,10))
pygame.display.set_caption("Tetris by @shababTAFE")

# Game board size
HEIGHT = 14
WIDTH = 10

# Score
score = 0

# Initial Position and Shape. (xPos, yPos) refers to top left position of current piece
xPosition = 4
yPosition = 0
rotationIndex = 0
currentPiece = random.randint(0,6)

# Timing
delay = 0.4

# Boolean to check if game is lost
gameStillGoing = True

# Shape Assets
shapeWidth = 4
lineshape  = "B..."
lineshape += "B..."
lineshape += "B..."
lineshape += "B..."
lineshape += "...."
lineshape += "BBBB"
lineshape += "...."
lineshape += "...."
lineshape += "B..."
lineshape += "B..."
lineshape += "B..."
lineshape += "B..."
lineshape += "...."
lineshape += "BBBB"
lineshape += "...."
lineshape += "...."
squareshape =  "BB.."
squareshape += "BB.."
squareshape += "...."
squareshape += "...."
squareshape += "BB.."
squareshape += "BB.."
squareshape += "...."
squareshape += "...."
squareshape += "BB.."
squareshape += "BB.."
squareshape += "...."
squareshape += "...."
squareshape += "BB.."
squareshape += "BB.."
squareshape += "...."
squareshape += "...."
lefts =  "BB.."
lefts += ".BB."
lefts += "...."
lefts += "...."
lefts += ".B.."
lefts += "BB.."
lefts += "B..."
lefts += "...."
lefts += "BB.."
lefts += ".BB."
lefts += "...."
lefts += "...."
lefts += ".B.."
lefts += "BB.."
lefts += "B..."
lefts += "...."
rights  = ".BB."
rights += "BB.."
rights += "...."
rights += "...."
rights += "B..."
rights += "BB.."
rights += ".B.."
rights += "...."
rights += ".BB."
rights += "BB.."
rights += "...."
rights += "...."
rights += "B..."
rights += "BB.."
rights += ".B.."
rights += "...."
tshape =  "BBB."
tshape += ".B.."
tshape += "...."
tshape += "...."
tshape += ".B.."
tshape += "BB.."
tshape += ".B.."
tshape += "...."
tshape += ".B.."
tshape += "BBB."
tshape += "...."
tshape += "...."
tshape += "B..."
tshape += "BB.."
tshape += "B..."
tshape += "...."
leftl  = ".B.."
leftl += ".B.."
leftl += "BB.."
leftl += "...."
leftl += "B..."
leftl += "BBB."
leftl += "...."
leftl += "...."
leftl += "BB.."
leftl += "B..."
leftl += "B..."
leftl += "...."
leftl += "BBB."
leftl += "..B."
leftl += "...."
leftl += "...."
rightl  = "B..."
rightl += "B..."
rightl += "BB.."
rightl += "...."
rightl += "BBB."
rightl += "B..."
rightl += "...."
rightl += "...."
rightl += "BB.."
rightl += ".B.."
rightl += ".B.."
rightl += "...."
rightl += "..B."
rightl += "BBB."
rightl += "...."
rightl += "...."

# Array containing shapes
shapeList = []
shapeList.append(lineshape)
shapeList.append(squareshape)
shapeList.append(leftl)
shapeList.append(rightl)
shapeList.append(lefts)
shapeList.append(rights)
shapeList.append(tshape)

# String that will track the state of the game
Field =  "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "#........#"
Field += "##########"
# Invisible rows to avoid out of bounds errors
Field += "#........#"
Field += "#........#"
Field += "#........#"


def drawBoard(Field):
	for ii in range(HEIGHT):
		for jj in range(WIDTH):
			if jj < WIDTH -1 :
				print(Field[ii*WIDTH + jj], end='')
			else:
				print(Field[ii*WIDTH + jj])
	print("##########")

def drawField(characterToDraw):
	global Field
	for yy in range(4):
		for xx in range(4):
			# Update field value by drawing the shape based on xPosition and yPosition
			if (shapeList[currentPiece][xx + shapeWidth*yy + (rotationIndex % 4)*16] == 'B'):
				Field = Field[:(xPosition + WIDTH*yPosition + xx + WIDTH*yy)] + characterToDraw + Field[(xPosition + WIDTH*yPosition + xx + WIDTH*yy + 1):]
				

def eraseCurrentPiece():
	global Field
	for yy in range(4):
		for xx in range(4):
			currentShapePositionIndex = xPosition + WIDTH*yPosition + xx + WIDTH*yy
			# Replace the 'B' with '.' in the Field if condition is met
			if Field[currentShapePositionIndex] == 'B':
				Field = Field[:(currentShapePositionIndex)] + '.' + Field[(currentShapePositionIndex + 1):]


def canMoveHorizontally(movementDirection):
	movementPossible = True
	for yy in range(4):
		for xx in range(4):
			# Check if the left or right position. Direction +1 means right and direction -1 means left
			currentPositionIndex = xPosition + WIDTH*yPosition + xx + WIDTH*yy
			indexToCheck = currentPositionIndex + movementDirection
			if (Field[currentPositionIndex] == 'B') and (Field[indexToCheck] == '#' or Field[indexToCheck] == 'X'):
				return False
	return movementPossible
	
def canMoveDown():
	downMovementPossible = True
	for yy in range(4):
		for xx in range(4):
			currentPositionIndex = xPosition + WIDTH*yPosition + xx + WIDTH*yy
			indexToCheck = currentPositionIndex + WIDTH
			if (Field[currentPositionIndex] == 'B') and (Field[indexToCheck] == '#' or Field[indexToCheck] == 'X'):
				return False
	return downMovementPossible

def handleLineClearing():
	global Field
	global score

	# Going from top to bottom, check if each line is full. If full, then clear line and drop lines above.
	for currentLineCheck in range(1,14,1):
		canClear = True
		for xx in range(8):
			indexCheck = WIDTH * currentLineCheck + xx + 1  
			if Field[indexCheck] == '.':
				canClear = False
		
		# If full, then clear the line
		if canClear:
			score = score + 1
			# Replace each row except for top row with what is above it
			for yy in range(currentLineCheck, 0, -1):  
				for xx in range(8):
					currentIndex = WIDTH * yy + xx + 1 
					indexAbove = currentIndex - WIDTH
					Field = Field[:(currentIndex)] + Field[indexAbove] + Field[(currentIndex + 1):]
			# Replace top row with '.'
			for xx in range(8):
				currentIndex = xx + 1
				Field = Field[:(currentIndex)] + '.' + Field[(currentIndex + 1):]




def checkGameOver():
	global gameStillGoing
	# Check if the starting xPosition and yPosition are filled with 'X'
	for yy in range(4):
		for xx in range(4):
			fieldIndex = xPosition + WIDTH*yPosition + xx + WIDTH * yy
			shapeIndex = xx + shapeWidth*yy
			if shapeList[currentPiece][shapeIndex] == 'B' and Field[fieldIndex] == 'X':
				gameStillGoing = False

def handleRotation():
	global rotationIndex
	# Check if rotation is possible
	rotationPossible = True
	for yy in range(4):
		for xx in range(4):
			indexToCheck = xPosition + WIDTH*yPosition + xx + yy*WIDTH
			if shapeList[currentPiece][xx + shapeWidth*yy + ((rotationIndex+1)%4)*16] == 'B' and (Field[indexToCheck] == 'X' or Field[indexToCheck] == '#'):
				rotationPossible = False
	# Rotate is rotation is possible
	if rotationPossible:
		eraseCurrentPiece()
		rotationIndex = (rotationIndex + 1)%4
		drawField('B')

# Draw field before game begins
drawField('B')
#Game loop
while(gameStillGoing):
	####### Timing #######
	time.sleep(delay)

	####### Input #######
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if canMoveHorizontally(-1):
					eraseCurrentPiece()
					xPosition = xPosition - 1
					drawField('B')
			if event.key == pygame.K_RIGHT:
				if canMoveHorizontally(1):
					eraseCurrentPiece()
					xPosition = xPosition + 1
					drawField('B')
			if event.key == pygame.K_UP:
				handleRotation()

	####### Game logic #######	
	# If piece can move down, then erase current shape and edit yPosition and draw shape again
	if canMoveDown():
		eraseCurrentPiece()
		yPosition = yPosition + 1
		drawField('B')
	# If piece can't move down, then check if line can be cleared replace the 'B' with 'X', set xPosition to 5,
	# yPosition to 0, rotationIndex to 0 and currentPiece to a new random integer
	else:
		eraseCurrentPiece()
		drawField('X')
		handleLineClearing()

		xPosition = 4
		yPosition = 0
		rotationIndex = 0
		currentPiece = random.randint(0,6)

		checkGameOver()


	####### Draw to screen #######
	os.system("cls")
	print("")
	print("Tetris by @shababTAFE")
	print("")
	print("Left - move left | Right - move right | Up - rotate")
	print("")
	drawBoard(Field)
	print("Score: " + str(score))

os.system("cls")
print("Game Over!")
print("Your score: " + str(score))





