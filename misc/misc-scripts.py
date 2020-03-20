def return_letters(text):
    letters = [char for char in text if char.isalpha()]
    letters = ''.join(letters)
    return letters
