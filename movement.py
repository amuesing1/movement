import random
import argparse
import re
import subprocess
import time
from pathlib import Path

def parse_markdown_moves(file_path):
    """Parse markdown file to extract move transitions from ## Transitions section"""
    moves_data = {}
    
    # Try multiple approaches to access the iCloud file
    # Method 1: Try direct file access
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except PermissionError:
        # Method 2: Try using AppleScript through osascript
        try:
            applescript = f'''
            tell application "System Events"
                set theFile to POSIX file "{file_path}"
                set fileContent to read theFile
                return fileContent
            end tell
            '''
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                content = result.stdout.strip()
            else:
                raise Exception(f"AppleScript failed: {result.stderr}")
        except:
            # Method 3: Try using 'open' command to trigger file access
            try:
                subprocess.run(['open', file_path], check=True, timeout=5)
                time.sleep(2)  # Wait for file access
                # Try direct access again
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                raise PermissionError(f"Cannot access file: {file_path}")
    
    # Find the ## Transitions section
    transitions_match = re.search(r'## Transitions\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if not transitions_match:
        raise ValueError("Could not find '## Transitions' section in markdown file")
    
    transitions_content = transitions_match.group(1)
    lines = transitions_content.strip().split('\n')
    
    current_move = None
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        # Check if it's a main move (starts with '- ' and no additional indentation)
        if line.startswith('- ') and not line.startswith('  '):
            current_move = line[2:].strip()
            moves_data[current_move] = []
        # Check if it's a sub-move (starts with '  - ')
        elif line.startswith('  - ') and current_move is not None:
            sub_move = line[4:].strip()
            moves_data[current_move].append(sub_move)
    
    return moves_data

# Load moves and transitions from markdown file
moves_file_path = '/Users/jeremymuesing/Library/Mobile Documents/iCloud~md~obsidian/Documents/MuseBrain/Health/Fitness/Moves.md'
moves_data = parse_markdown_moves(moves_file_path)

# Define the 4 movement types
move_types = ['squat', 'stand', 'crawl', 'crab']

def get_next_moves(move):
    """Get possible next moves for a given move"""
    return moves_data.get(move, [])

def generate_sequence(min_len=4, max_len=6):
    """Generate a random sequence of moves, ignoring type moves in the count"""
    num_moves = random.randint(min_len, max_len)
    sequence = []
    current_move = random.choice(move_types)  # Start with random type
    sequence.append(current_move)
    count = 0
    
    while count < num_moves:
        next_moves = get_next_moves(current_move)
        if not next_moves:
            break
        next_move = random.choice(next_moves)
        sequence.append(next_move)
        # Only count proper moves, not types
        if next_move not in move_types:
            count += 1
        current_move = next_move
    
    # Optional: close loop if possible
    if sequence and sequence[0] in get_next_moves(current_move):
        sequence.append(sequence[0])
    return sequence

def generate_focus_combinations(move):
    """Generate input-focus-output combinations for a specific move"""
    inputs = [k for k, vals in moves_data.items() if move in vals]
    outputs = moves_data.get(move, [])
    return [[inp, move, out] for inp in inputs for out in outputs]

def format_with_arrows(sequence):
    """Format a sequence list with arrow notation"""
    return ' → '.join(sequence)

def write_to_movement_practice(content, section_type='sequence'):
    """Write content to Movement Practice.md file"""
    practice_file_path = '/Users/jeremymuesing/Library/Mobile Documents/iCloud~md~obsidian/Documents/MuseBrain/Health/Fitness/Movement Practice.md'
    
    # Read the current file content
    try:
        with open(practice_file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading Movement Practice.md: {e}")
        return False
    
    lines = file_content.split('\n')
    
    if section_type == 'sequence':
        # Find the line with >[!workout] Sequence
        target_marker = '>[!workout] Sequence'
        for i, line in enumerate(lines):
            if target_marker in line:
                # Remove any existing sequence lines (lines that start with > after the marker)
                j = i + 1
                while j < len(lines) and lines[j].startswith('>'):
                    lines.pop(j)
                
                # Insert new sequence lines
                for sequence_line in content:
                    lines.insert(j, f'> - {sequence_line}')
                    j += 1
                break
        else:
            print("Could not find >[!workout] Sequence marker")
            return False
            
    elif section_type == 'transitions':
        # Find the line with >[!workout] Transitions
        target_marker = '>[!workout] Transitions'
        for i, line in enumerate(lines):
            if target_marker in line:
                # Remove any existing transition lines (lines that start with > after the marker)
                j = i + 1
                while j < len(lines) and lines[j].startswith('>'):
                    lines.pop(j)
                
                # Insert new transition lines
                for transition_line in content:
                    lines.insert(j, f'> - {transition_line}')
                    j += 1
                break
        else:
            print("Could not find >[!workout] Transitions marker")
            return False
    
    # Write the modified content back to the file
    try:
        with open(practice_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True
    except Exception as e:
        print(f"Error writing to Movement Practice.md: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate movement sequences or focus on a specific move.")
    parser.add_argument('--focus', type=str, help="Name of the move to focus on")
    parser.add_argument('--sequence', action='store_true', help="Generate only a sequence (not transitions)")
    args = parser.parse_args()
    
    if args.focus:
        # Focus mode - generate transitions for a specific move
        combos = generate_focus_combinations(args.focus)
        print(f"Combinations for move {args.focus}:")
        selected = random.sample(combos, min(10, len(combos)))
        
        formatted_combos = [format_with_arrows(combo) for combo in selected]
        for combo in formatted_combos:
            print(combo)
        
        success = write_to_movement_practice(formatted_combos, 'transitions')
        print(f"\n{'Transitions written' if success else 'Failed to write transitions'} to Movement Practice.md")
            
    elif args.sequence:
        # Sequence-only mode - generate 2 sequences
        sequences = []
        for i in range(2):
            seq = generate_sequence()
            formatted_seq = format_with_arrows(seq)
            sequences.append(formatted_seq)
            print(f"Random movement sequence {i+1}:")
            print(formatted_seq)
        
        success = write_to_movement_practice(sequences, 'sequence')
        print(f"\n{'Sequences written' if success else 'Failed to write sequences'} to Movement Practice.md")
            
    else:
        # Default mode - run both sequence and transitions
        print("=== Generating Movement Sequences ===")
        sequences = []
        for i in range(2):
            seq = generate_sequence()
            formatted_seq = format_with_arrows(seq)
            sequences.append(formatted_seq)
            print(f"Random movement sequence {i+1}:")
            print(formatted_seq)
        
        sequence_success = write_to_movement_practice(sequences, 'sequence')
        print(f"{'Sequences written' if sequence_success else 'Failed to write sequences'} to Movement Practice.md")
        
        print("\n=== Generating Transition Combinations ===")
        focus_move_name = random.choice(list(moves_data.keys()))
        combos = generate_focus_combinations(focus_move_name)
        print(f"Combinations for move {focus_move_name}:")
        selected = random.sample(combos, min(10, len(combos)))
        
        formatted_combos = [format_with_arrows(combo) for combo in selected]
        for combo in formatted_combos:
            print(combo)
        
        transitions_success = write_to_movement_practice(formatted_combos, 'transitions')
        print(f"\n{'Transitions written' if transitions_success else 'Failed to write transitions'} to Movement Practice.md")
        
        # Summary
        if sequence_success and transitions_success:
            print(f"\n✅ Both sequences and transitions successfully written to Movement Practice.md")
        elif sequence_success or transitions_success:
            print(f"\n⚠️  Partial success - check file for details")
        else:
            print(f"\n❌ Failed to write to Movement Practice.md")