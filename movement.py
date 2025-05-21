import json
import random
import argparse

# Load flat moves and transitions from moves.json
with open('moves.json', 'r') as f:
    moves_data = json.load(f)

# Define the 4 movement types
move_types = ['squat', 'stand', 'crawl', 'crab']

def get_random_start():
    # pick a starting move from one of the 4 types
    return random.choice(move_types)

def get_next_moves(move):
    return moves_data.get(move, [])

def generate_sequence(min_len=4, max_len=6):
    # generate a random sequence of moves, ignoring type moves in the count
    num_moves = random.randint(min_len, max_len)
    sequence = []
    current_move = get_random_start()
    sequence.append(current_move)
    count = 0
    while count < num_moves:
        next_move = random.choice(get_next_moves(current_move))
        sequence.append(next_move)
        # only count proper moves, not types
        if next_move not in move_types:
            count += 1
        current_move = next_move
    # optional: close loop if possible
    if sequence and sequence[0] in get_next_moves(current_move):
        sequence.append(sequence[0])
    return sequence

def focus_move(move):
    inputs = [k for k, vals in moves_data.items() if move in vals]
    outputs = moves_data.get(move, [])
    combos = [[inp, move, out] for inp in inputs for out in outputs]
    return combos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate movement sequences or focus on a specific move.")
    parser.add_argument('--focus', type=str, help="Name of the move to focus on")
    args = parser.parse_args()
    if args.focus:
        combos = focus_move(args.focus)
        print(f"Combinations for move {args.focus}:")
        # select up to 10 random combos to display
        selected = random.sample(combos, min(10, len(combos)))
        for combo in selected:
            print(combo)
    else:
        seq = generate_sequence()
        print("Random movement sequence:")
        print(seq)