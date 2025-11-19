# Movement Flow Generator

A Python tool for generating randomized movement sequences from a library of transitions. Perfect for movement practice, flow training, and creative exploration.

## 🎯 Features

- **Random Flow Generation**: Create sequences of connected movements
- **Markdown Integration**: Parse movement transitions from Obsidian notes
- **Flexible Input**: Support for both markdown files and JSON data
- **Customizable Length**: Generate flows of any length
- **Movement Library**: 34+ movements including capoeira, animal flow, and ground movements

## 📋 Movement Library

Includes movements like:
- Ground movements: squat, lizard, crab, crawl
- Capoeira moves: negativa, role, ginja, s dobrado
- Transitions: corta capim, whip, underswitch
- Rotational: spiral, corkscrew, circular rolls
- And many more!

## 🚀 Usage

### Basic Flow Generation

```bash
# Generate a 10-move flow
python movement.py

# Generate a custom length flow
python movement.py --length 15

# Use a specific markdown file
python movement.py --file "/path/to/movements.md"

# Use JSON data directly
python movement.py --json moves.json
```

### Command Line Options

- `--length N` - Number of moves in the sequence (default: 10)
- `--file PATH` - Path to markdown file with transitions
- `--json PATH` - Path to JSON file with movement data
- `--start MOVE` - Starting movement (optional)

### Example Output

```
Movement Flow (10 moves):
1. squat
2. corta capim
3. negativa
4. role
5. lizard
6. crawl
7. underswitch
8. crab
9. backsweep
10. squat
```

## 📁 Files

- `movement.py` - Main script for generating flows
- `moves.json` - Movement transition data
- `moves_list.txt` - List of available movements

## 🔧 How It Works

1. **Parse Transitions**: Reads movement transitions from markdown or JSON
2. **Build Graph**: Creates a directed graph of possible transitions
3. **Random Walk**: Generates a flow by randomly selecting valid transitions
4. **Output**: Displays the sequence of movements

### Markdown Format

The script can parse transitions from markdown files with this format:

```markdown
## Transitions

- squat → corta capim, negativa, lizard
- negativa → role, lizard, squat
- role → squat, lizard, crawl
```

## 🎨 Use Cases

- **Practice Sessions**: Generate new flows for training
- **Creative Exploration**: Discover new movement combinations
- **Teaching**: Create sequences for students
- **Warm-ups**: Random flows for dynamic warm-ups
- **Flow State**: Practice continuous movement transitions

## 🔄 Integration with Obsidian

This tool is designed to work with Obsidian notes:
- Store movement transitions in your vault
- Parse directly from iCloud-synced files
- Update transitions as you learn new moves
- Track your movement practice

## 🛠️ Requirements

- Python 3.7+
- No external dependencies (uses standard library)

## 📝 Adding New Movements

### Option 1: Edit JSON

Add to `moves.json`:
```json
{
  "new_move": ["transition1", "transition2", "transition3"]
}
```

### Option 2: Edit Markdown

Add to your markdown file:
```markdown
- new_move → transition1, transition2, transition3
```

## 🤝 Contributing

Feel free to:
- Add new movements
- Improve transition logic
- Enhance output formatting
- Add new features

## 📄 License

MIT License - Use freely for your movement practice!

---

**Happy flowing! 🌊**