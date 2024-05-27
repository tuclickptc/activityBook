import random
import string

def generate_word_search(words, size=15):
    # Ajustar tamaño según la palabra más larga si es necesario
    size = max(size, max(len(word) for word in words))
    
    puzzle = [[' ']*size for _ in range(size)]
    solution = [[' ']*size for _ in range(size)]
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (-1, 1), (0, -1), (-1, 0), (-1, -1)]  # Todas las direcciones

    def can_place_word(word, x, y, dx, dy):
        for k in range(len(word)):
            nx, ny = x + k * dx, y + k * dy
            if not (0 <= nx < size and 0 <= ny < size) or (puzzle[nx][ny] != ' ' and puzzle[nx][ny] != word[k]):
                return False
        return True

    def place_word(word, x, y, dx, dy):
        for k in range(len(word)):
            nx, ny = x + k * dx, y + k * dy
            puzzle[nx][ny] = word[k]
            solution[nx][ny] = word[k]

    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 200:
            dir = random.choice(directions)
            start_x = random.randint(0, size - 1)
            start_y = random.randint(0, size - 1)
            if can_place_word(word, start_x, start_y, dir[0], dir[1]):
                place_word(word, start_x, start_y, dir[0], dir[1])
                placed = True
            attempts += 1
        if not placed:
            raise ValueError(f"Could not place the word: {word}")

    # Rellenar espacios vacíos con letras aleatorias
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] == ' ':
                puzzle[i][j] = random.choice(string.ascii_uppercase)
    
    return puzzle, solution

