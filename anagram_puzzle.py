import json, os
from random import choice, shuffle
import requests

def read_dictionary(filename) -> list:
    """Open a json file corresponding to a dictionary."""
    with open(filename) as data:
        return [word for word in list(json.load(data)) if len(word) > 3]


def dictionary_api(word, ninja_api_key):
    """From https://dictionaryapi.dev/ get the definition of a certain word."""
    header = {
        "X-Api-Key": ninja_api_key
    }
    url = f"https://api.api-ninjas.com/v1/dictionary?word={word}"
    response = requests.request("GET",
                                url=url,
                                headers=header)
    return response.json()

def picked_word(lst_words):
    """From a given list of words, choose randomly one."""
    return choice(lst_words)

def shuffle_word(word: str):
    """Change the order of each letter in the word."""
    lst_letters = list(word)
    shuffle(lst_letters)
    return "".join(lst_letters)

def find_word_dictionary(user_input: str, dictionary_words: list) -> bool:
    """Check if the user's input is an actual word.
    Return True if it is, elsewhere returns False."""
    if user_input in dictionary_words:
        return True
    else:
        return False
def file_text(lst_items: list, name_file: str):
    """Takes a list and add each item in a double separated line."""
    with open(name_file, "a") as file:
        for line in lst_items:
            if type(line) == dict:
                for k, v in line.items():
                    file.write(f"{k.title()} - {v}\n\n")
            else:
                file.write(f"{line}\n\n")


def main():
    title = """
       ___                                                    __   
      / _ | ___  ___ ____ ________ ___ _    ___  __ ________ / /__ 
     / __ |/ _ \/ _ `/ _ `/ __/ _ `/  ' \  / _ \/ // /_ /_ // / -_)
    /_/ |_/_//_/\_,_/\_, /_/  \_,_/_/_/_/ / .__/\_,_//__/__/_/\__/ 
                    /___/                /_/                       
    """
    dictionary_words = read_dictionary("words_dictionary.json")
    score = 0
    guessed_anagrams = []
    ninja_api_key = os.environ["API_NINJA"]
    print(title)
    while True:
        word = picked_word(dictionary_words)
        print(f"Word: {shuffle_word(word=word)}")
        anagram = input("> ")
        if find_word_dictionary(
                user_input=anagram,
                dictionary_words=dictionary_words):
            score += 1
            try:
                new_word = {
                    f"{anagram}": dictionary_api(word=anagram,
                                                 ninja_api_key=ninja_api_key)["definition"].strip()
                }
                guessed_anagrams.append(new_word)
            except json.JSONDecodeError:
                pass
        if len(anagram) == 0:
            print(f"You got a total of {score} anagrams.")
            file_text(lst_items=guessed_anagrams,
                      name_file="words.txt")
            break


if __name__ == '__main__':
    main()