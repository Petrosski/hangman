import time
import random
import telebot
from telebot import types

def ler_api_key():
    with open('token.txt', 'r') as arquivo:
        return arquivo.read().strip()

API_KEY = ler_api_key()

# Global variables
count = 0
display = ''
word = ''
already_guessed = []
limit = 5

def main():
    global count, display, word, already_guessed, limit
    word = get_random_word()
    length = len(word)
    count = 0
    display = '_' * length
    already_guessed = []
    limit = 5

def hangman(guess):
    global count, display, word, already_guessed, limit
    limit = 5
    guess = guess.strip()

    if not guess.isalpha() or len(guess) != 1:
        return "Caractere errado, tente uma outra letra\n"

    elif guess in already_guessed:
        return "Outra letra.\n"

    else:
        count += 1
        already_guessed.extend([guess])
        time.sleep(1)

def draw_hangman(attempt_count):

    visible_errors = 2
    total_errors = attempt_count + visible_errors

    hangman_array = [
        '    --',
        '    | ',
        '    O ',
        '    | ',
        '   \\|/',
        '    | ',
        '   / \\'
    ]
    hangman_stick = [
        '--|  ',
        '  |  ',
        '  |  ',
        '  |  ',
        '  |  ',
        '  |  ',
        ' _|__'
    ]

    hangman_status = ""
    for i in range(len(hangman_array)):
        hangman_status += hangman_array[i] + hangman_stick[i] + "\n" if i < total_errors else '      ' + hangman_stick[i] + "\n"
    
    return hangman_status

def get_random_word():
    try:
        with open('cars.txt', 'r') as file:
            words = [line.strip() for line in file.readlines()]
            return random.choice(words)
    except Exception as e:
        return f"Erro ao obter a palavra: {e}"

# Start the bot
bot = telebot.TeleBot(API_KEY)

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

    initial_message = f"Esta é a palavra Hangman ({len(word)} letras): {display} Digite seu palpite:\n{draw_hangman(count)}"
    bot.send_message(message.chat.id, initial_message)

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
    hangman_status = hangman(guess)
    # Draw hangman status
    hangman_drawing = draw_hangman(count)
    # Combine the hangman status and drawing
    combined_message = f"{hangman_status}\nEsta é a palavra Hangman ({len(word)} letras): {display} Digite seu palpite:\n{hangman_drawing}"

    bot.send_message(message.chat.id, combined_message)

    # Check if the game is over
    if display == word:
        bot.send_message(message.chat.id, f"Parabéns! Você adivinhou a palavra {word}. Digite /play para iniciar um novo jogo.")
    elif count == limit:
        bot.send_message(message.chat.id, f"Game Over! A palavra era {word}. Digite /play para iniciar um novo jogo.")

# Start the bot
bot.polling()