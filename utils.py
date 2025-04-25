import random

def generate_random_reference(length=12, max_page=9):
    return ' '.join(str(random.randint(0, max_page)) for _ in range(length))
