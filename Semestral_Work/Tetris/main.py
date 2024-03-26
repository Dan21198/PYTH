import pygame
from tetromino import *
from display import *
from board import *
from direction import *
from rotation import *

isOpen = True
newGame = True
gameOver = False
paused = False

window = Window()
draw = Draw(window)
draw.createScreen()
clock = pygame.time.Clock()

while isOpen:
    # Draw new Frame
    pygame.display.update()
    # Clear screen
    draw.screen.fill("Black")

    # Reset board
    if newGame:
        board = Board()
        tetromino = board.generatePiece()
        timeCount = 0
        draw.drawStartScreen(board)

    # New game screen loop
    while newGame:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                newGame = False
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_p]:
                newGame = False
            if keyInput[pygame.K_b]:
                newGame = False

    # Pause / Start screen loop
    while paused:
        draw.drawPauseScreen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_ESCAPE]:
                paused = False
            if keyInput[pygame.K_n]:
                newGame = True
                paused = False

    # Game play Loop
    while not (newGame or gameOver or paused):
        # Draw game elements to screen
        draw.refreshScreen(board, tetromino)

        # Step game forward
        timeCount += clock.get_rawtime()
        clock.tick()
        if timeCount >= board.getDropInterval():
            timeCount = 0
            locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
            if locked:
                tetromino = board.newPieceOrGameOver(tetromino)
                if tetromino is None:
                    gameOver = True
            draw.refreshScreen(board, tetromino)

        # Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_ESCAPE]:
                paused = True
            if keyInput[pygame.K_n]:
                newGame = True
            if keyInput[pygame.K_LCTRL] or keyInput[pygame.K_RCTRL]:
                board.rotatePiece(tetromino, Rotation.ANTICLOCKWISE)
            if keyInput[pygame.K_UP]:
                board.rotatePiece(tetromino, Rotation.CLOCKWISE)
            if keyInput[pygame.K_RIGHT]:
                board.moveOrLockPiece(tetromino, Direction.RIGHT)
            if keyInput[pygame.K_LEFT]:
                board.moveOrLockPiece(tetromino, Direction.LEFT)
            if keyInput[pygame.K_DOWN]:
                locked = board.moveOrLockPiece(tetromino, Direction.DOWN)
                if locked:
                    tetromino = board.newPieceOrGameOver(tetromino)
                    if tetromino is None:
                        gameOver = True
            if keyInput[pygame.K_RETURN]:
                board.dropAndLockPiece(tetromino)
                tetromino = board.newPieceOrGameOver(tetromino)
                if tetromino is None:
                    gameOver = True
            if keyInput[pygame.K_LSHIFT] or keyInput[pygame.K_RSHIFT]:
                if board.isHeldPieceEmpty():
                    board.setHeldPiece(tetromino)
                    tetromino = board.generatePiece()
                else:
                    tetromino = board.swapWithHeldPiece(tetromino)

    # Game over screen loop
    while gameOver:
        draw.drawGameOver(board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                isOpen = False
            keyInput = pygame.key.get_pressed()
            if keyInput[pygame.K_n] or keyInput[pygame.K_ESCAPE]:
                newGame = True
                gameOver = False
