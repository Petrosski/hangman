import time
import random
import requests
import telebot
from telebot import types

API_KEY = "6967238258:AAHjjSaAEWAFs-qFs_u7L_Jj-y85Yvyve6I"

# Initializing all the conditions required for the game
def hangman(guess):
    global count, display, word, already_guessed, limit
    limit = 5
    guess = guess.strip()

    if len(guess) == 0 or len(guess) >= 2 or guess <= "9":
        return "Caractere errado, tente uma outra letra\n"

    elif guess in already_guessed:
        return "Outra letra.\n"

    else:
        count += 1
        already_guessed.extend([guess])
        time.sleep(1)

        if count == 1:
            return "   _____ \n" "  |      \n" "  |      \n" "  |      \n" "  |      \n" "  |      \n" "  |      \n" "__|__\n"
        elif count == 2:
            return "   _____ \n" "  |     | \n" "  |     |\n" "  |      \n" "  |      \n" "  |      \n" "  |      \n" "__|__\n"
        elif count == 3:
            return "   _____ \n" "  |     | \n" "  |     |\n" "  |     | \n" "  |      \n" "  |      \n" "  |      \n" "__|__\n"
        elif count == 4:
            return "   _____ \n" "  |     | \n" "  |     |\n" "  |     | \n" "  |     O \n" "  |      \n" "  |      \n" "__|__\n"
        elif count == 5:
            return "   _____ \n" "  |     | \n" "  |     |\n" "  |     | \n" "  |     O \n" "  |    /|\ \n" "  |    / \ \n" "__|__\n"

def get_random_word():
    try:
        with open('cars.txt', 'r') as file:
            words = [line.strip() for line in file.readlines()]
            return random.choice(words)
    except Exception as e:
        return f"Erro ao obter a palavra: {e}"

# Start the bot
bot = telebot.TeleBot(API_KEY)

def main():
    global count, display, word, already_guessed, limit
    word = get_random_word()
    length = len(word)
    count = 0
    display = '_' * length
    already_guessed = []
    limit = 5

@bot.message_handler(commands=['start'])
def start_ex(message):
    bot.send_message(message.chat.id, 'Bem-vindo ao Hangman! Digite /play para iniciar um novo jogo')

@bot.message_handler(commands=['play'])
def play_game(message):
    global count, display, word, already_guessed, limit
    count = 0
    display = ''
    word = ''
    already_guessed = []
    limit = 5

    # Call the main function to get a new word
    main()

    # Send the initial hangman status
    bot.send_message(message.chat.id, f"Esta é a palavra Hangman ({len(word)} letras): {display} Digite seu palpite:")

@bot.message_handler(func=lambda msg: msg.text.lower() == 'exit')
def exit_game(message):
    bot.send_message(message.chat.id, 'Saindo do jogo. Digite /play para iniciar um novo jogo.')

@bot.message_handler(func=lambda msg: msg.text.isalpha() and len(msg.text) == 1)
def make_guess(message):
    global count, display, word, already_guessed, limit

    guess = message.text.lower()

    if guess in already_guessed:
        bot.send_message(message.chat.id, "Outra letra")
        return

    already_guessed.append(guess)

    if guess not in word:
        count += 1

    # Update the display
    display = ''.join([letter if letter in already_guessed else '_' for letter in word])

    # Send hangman status
    bot.send_message(message.chat.id, hangman(guess))
    bot.send_message(message.chat.id, f"Esta é a palavra Hangman ({len(word)} letras): {display} Digite seu palpite:")

    # Check if the game is over
    if display == word:
        bot.send_message(message.chat.id, f"Parabéns! Você adivinhou a palavra {word}. Digite /play para iniciar um novo jogo.")
    elif count == limit:
        bot.send_message(message.chat.id, f"Game Over! A palavra era {word}. Digite /play para iniciar um novo jogo.")

# Start the bot
bot.polling()