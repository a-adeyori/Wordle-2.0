import random
import sys
import collections
import json
from colorama import init, Fore, Style

init()

player_scores = collections.defaultdict(int)


def get_scores():
    #get scores from json file
    try:
        with open('scores.json', 'r') as file:
            global player_scores
            data = json.load(file)
            player_scores.update(data)
    except FileNotFoundError:
        print('New player? starting fresh...')
        player_scores=collections.defaultdict(int)

def save_scores():
    #save scores to JSON file
    with open('scores.json','w') as file:
        json.dump(player_scores, file, indent = 4)

def get_valid_guess():
    while True:
        guess= input("🕵️ Enter a 5-letter guess: ")
        if guess.isalpha() and len(guess) == 5 and len(set(guess)) == len(guess):
            return guess
        print("⚠️ Invalid guess! Make sure it's a 5-letter word without repeating characters.")
        
def single():

    username = input("Enter your username: ").strip()
    get_scores()
    highest_score = player_scores[username]
    print(f"🏆Previous highest score for {username}: {highest_score}")

    max_trials = select_difficulty()
    answer = getRandomWord()
    store = collections.defaultdict(int)
    score = 0
    trial = 0

    while trial < max_trials:
        initial_guess = get_valid_guess()
        score+=(printGuessScore(initial_guess, answer))
        trial += 1

        colored_output = ''
        for i in range(len(initial_guess)):
            colored_output += letterColor(i, initial_guess, answer)
        print(colored_output.strip())
        if initial_guess == answer:
            print(f"🎉 Congratulations, {username}! You've guessed the word!")
            break
    else:
        print("❌ Oops! You're all out of guesses.")
        print(f"The correct word was: {answer}")

    update_scores(username, score)
    save_scores()

def multi():
    player1 = input("Enter Player 1's name: ").strip()
    player2 = input("Enter Player 2's name: ").strip()
    print(f"Welcome to Wordle 2.0 {player1} and {player2}!")

    players = [(player1, 0), (player2, 0)]
    max_trials = select_difficulty()
    trial=[0,0] # separate trials for each player
    current_player = 0 # 0 represents player1, 1 represents player 2
    answer = getRandomWord()
    store = collections.defaultdict(int)

    while trial[0] < max_trials or trial[1] < max_trials:
        player_name = players[current_player][0]
        print(f"\n🎲 {player_name}'s turn! ({trial[current_player]+1})/{max_trials} attempts")

        initial_guess = get_valid_guess()
        
        colored_output = ''
        for i in range(len(initial_guess)):
            colored_output += letterColor(i, initial_guess, answer)
        print(colored_output.strip())

        if initial_guess == answer:
            if trial[0] == trial[1]:
                print("🤝 It's a tie! Both players guessed the word!")
            else:
                print(f"🎉 Congratulations, {player_name}! You've guessed the word!")
            return
        
        trial[current_player] += 1
        current_player = 1 - current_player
        

    print("🕵️‍♂️ Oops! It seems our detectives couldn't crack the case this time! 🔍")
    print(f"The secret word was: {answer}. Better luck next time, {player1} and {player2}! Keep those thinking caps on! 🎩✨")


def select_difficulty():
    max_trials = 0
    while max_trials == 0:
        difficulty = input("Choose difficulty Normal or Hard (n/h): ").strip().lower()
        if difficulty == "n":
            max_trials = 5
        elif difficulty == "h":
            max_trials = 3
        else:
            print("⚠️ Enter 'n' or 'h' to select difficulty")
    return max_trials

def update_scores(username, score):
    if score > player_scores[username]:
        player_scores[username] = score
        print(f"🏆 New highest score for {username}: {score}")
    else:
        print(f"📊 {username}'s highest score remains: {player_scores[username]}")

def printGuessScore(guess, answer):
    score = 0
    for i in range(len(guess)):
        display = letterColor(i, guess, answer)
        if Fore.GREEN in display:
            score += 2
        elif Fore.YELLOW in display:
            score += 1
    # print("\n")  # New line after each guess
    return score

def letterColor(index, guess, answer):
    if guess[index] == answer[index]:
        return(f'{Fore.GREEN}{guess[index]}{Style.RESET_ALL}')
    elif guess[index] in answer:
        return(f'{Fore.YELLOW}{guess[index]}{Style.RESET_ALL}')
    else:
        return(f'{Fore.RED}{guess[index]}{Style.RESET_ALL}')

def getRandomWord():
    # Choose the word to be the answer for testing purposes.
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        with open("words.txt", "r") as file:
        # Strip removes the new line at the end of each word.
            words = [word.strip() for word in file.readlines()]
        return random.choice(words)

def main():
    mode=''
    while mode!='s' or mode!='m':
        print("Hello this is Wordle 2.0, let's begin...")
        mode = input("Choose your mode: single player or multiplayer (s/m): ")
        if mode == 'm':
            multi()
        elif mode == 's':
            single()
        else:
            print("⚠️ Input 's' for single player mode or 'm' for multiplayer mode")

main()