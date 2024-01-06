import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BG_COLOR = (50, 50, 60)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 150, 200)

# Initial board settings
WIDTH = 8
HEIGHT = 8
MINES = 10


# Define difficulty levels
def set_difficulty(level):
    global WIDTH, HEIGHT, MINES
    difficulties = {"easy": (8, 8, 10), "medium": (16, 16, 40), "hard": (24, 24, 99)}
    WIDTH, HEIGHT, MINES = difficulties[level]
    reset_game()


def reset_game():
    global game, ai, revealed, flags, lost, start_time, cell_size, flag, mine
    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
    revealed = set()
    flags = set()
    lost = False
    start_time = pygame.time.get_ticks()  # Reset the timer

    # Adjust cell size based on the difficulty
    board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
    board_height = height - (BOARD_PADDING * 2)
    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))

    # Rescale flag and mine images
    flag = pygame.transform.scale(flag, (cell_size, cell_size))
    mine = pygame.transform.scale(mine, (cell_size, cell_size))


def draw_button(button_rect, text, center_pos, screen, font):
    """Draws a button with hover effect."""
    mouse = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, HOVER_COLOR, button_rect)  # Hover effect
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    buttonText = font.render(text, True, WHITE)
    buttonTextRect = buttonText.get_rect()
    buttonTextRect.center = center_pos
    screen.blit(buttonText, buttonTextRect)


# Create game
pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

# Initialize timer
start_time = pygame.time.get_ticks()

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent, initialize game state variables
reset_game()

# Show instructions initially
instructions = True

while True:
    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)

    # Show game instructions
    if instructions:
        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 80)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Uncover all safe cells to win!",
            "Uncover a mine though, and you lose!",
            "Choose a difficulty below to begin playing.",
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 40 * i)
            screen.blit(line, lineRect)

        # Difficulty buttons
        difficulty_levels = ["easy", "medium", "hard"]
        for i, level in enumerate(difficulty_levels):
            buttonRect = pygame.Rect((width / 4), 350 + 70 * i, width / 2, 50)
            center_pos = (width / 2, 350 + 70 * i + 25)
            draw_button(buttonRect, level.capitalize(), center_pos, screen, mediumFont)

            # Check if difficulty button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if buttonRect.collidepoint(mouse):
                    set_difficulty(level)
                    instructions = False
                    time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))), True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # Draw AI Move, Reset, and Main Menu buttons
    ai_button_rect = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING,
        (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2,
        50,
    )
    reset_button_rect = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING,
        (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2,
        50,
    )
    main_menu_button_rect = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING,
        (1 / 3) * height + 90,
        (width / 3) - BOARD_PADDING * 2,
        50,
    )

    draw_button(ai_button_rect, "AI Move", ai_button_rect.center, screen, mediumFont)
    draw_button(
        reset_button_rect, "Reset", reset_button_rect.center, screen, mediumFont
    )
    draw_button(
        main_menu_button_rect,
        "Main Menu",
        main_menu_button_rect.center,
        screen,
        mediumFont,
    )

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Display timer
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    timer_surface = smallFont.render(f"Time: {elapsed_time} s", True, WHITE)
    timer_rect = timer_surface.get_rect()
    timer_rect.topleft = ((2 / 3) * width + BOARD_PADDING, 20)
    screen.blit(timer_surface, timer_rect)

    # Display mine counter
    mines_left = MINES - len(flags)
    mine_counter_surface = smallFont.render(
        f"Mines left to mark: {mines_left}", True, WHITE
    )
    mine_counter_rect = mine_counter_surface.get_rect()
    mine_counter_rect.topleft = (
        (2 / 3) * width + BOARD_PADDING,
        70,
    )
    screen.blit(mine_counter_surface, mine_counter_rect)

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if ai_button_rect.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif reset_button_rect.collidepoint(mouse):
            reset_game()
            continue

        # Return to main menu
        elif main_menu_button_rect.collidepoint(mouse):
            instructions = True
            continue

        # User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (
                        cells[i][j].collidepoint(mouse)
                        and (i, j) not in flags
                        and (i, j) not in revealed
                    ):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
