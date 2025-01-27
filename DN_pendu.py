import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main window dimensions
MAIN_WIDTH, MAIN_HEIGHT = 800, 600
main_window = pygame.display.set_mode((MAIN_WIDTH, MAIN_HEIGHT))
pygame.display.set_caption("Hangman Game - Main")

# Hangman window dimensions
HANGMAN_WIDTH, HANGMAN_HEIGHT = 400, 400
hangman_window = pygame.display.set_mode((HANGMAN_WIDTH, HANGMAN_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Hangman Drawing")

# Font for text
font = pygame.font.SysFont("Arial", 36)

# Function to display text
def display_text(surface, text, x, y):
    rendered_text = font.render(text, True, BLACK)
    surface.blit(rendered_text, (x, y))

# Function to choose a random word
def choose_word():
    try:
        with open("words.txt", "r") as file:
            words = file.read().splitlines()
        return random.choice(words)
    except FileNotFoundError:
        return "default"  # A fallback word if the file is missing

# Function to display the guessed letters in the word
def display_word(word, guessed_letters):
    result = ""
    for letter in word:
        if letter in guessed_letters:
            result += letter + " "
        else:
            result += "_ "
    return result

# Function to draw the hangman
def draw_hangman(attempts_left):
    hangman_window.fill(WHITE)  # Clear the hangman window

    # Draw the hangman structure and parts step by step
    if attempts_left <= 5:  # Base
        pygame.draw.line(hangman_window, BLACK, (50, 350), (150, 350), 5)
    if attempts_left <= 4:  # Pole
        pygame.draw.line(hangman_window, BLACK, (100, 350), (100, 50), 5)
    if attempts_left <= 3:  # Top bar
        pygame.draw.line(hangman_window, BLACK, (100, 50), (250, 50), 5)
    if attempts_left <= 2:  # Rope
        pygame.draw.line(hangman_window, BLACK, (250, 50), (250, 100), 5)
    if attempts_left <= 1:  # Head
        pygame.draw.circle(hangman_window, BLACK, (250, 125), 25, 5)
    if attempts_left == 0:  # Body and limbs
        # Body
        pygame.draw.line(hangman_window, BLACK, (250, 150), (250, 250), 5)
        # Left arm
        pygame.draw.line(hangman_window, BLACK, (250, 175), (200, 200), 5)
        # Right arm
        pygame.draw.line(hangman_window, BLACK, (250, 175), (300, 200), 5)
        # Left leg
        pygame.draw.line(hangman_window, BLACK, (250, 250), (200, 300), 5)
        # Right leg
        pygame.draw.line(hangman_window, BLACK, (250, 250), (300, 300), 5)

    pygame.display.flip()  # Update the hangman window

# Function to play the game
def play():
    word = choose_word()
    guessed_letters = []
    attempts_left = 6
    name = input("Enter your name: ")

    while attempts_left > 0:
        main_window.fill(WHITE)
        draw_hangman(attempts_left)

        display_text(main_window, f"Word: {display_word(word, guessed_letters)}", 200, 100)
        display_text(main_window, f"Attempts left: {attempts_left}", 200, 200)
        pygame.display.flip()

        letter = None
        while letter is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key)

        if letter in word and letter not in guessed_letters:
            guessed_letters.append(letter)
            if all(l in guessed_letters for l in word):
                display_text(main_window, f"Congratulations! The word was: {word}", 200, 300)
                pygame.display.flip()
                pygame.time.wait(2000)
                return
        else:
            attempts_left -= 1

    display_text(main_window, f"Game Over! The word was: {word}", 200, 300)
    pygame.display.flip()
    pygame.time.wait(2000)

# Main menu
def menu():
    running = True
    while running:
        main_window.fill(WHITE)
        display_text(main_window, "Game Menu", 300, 100)
        display_text(main_window, "1. Play", 350, 200)
        display_text(main_window, "2. Quit", 350, 300)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play()
                elif event.key == pygame.K_2:
                    running = False

# Run the menu
menu()
pygame.quit()
