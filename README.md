# Font Pairing Preview Generator

A Python tool for generating visual previews of font combinations, perfect for designers and developers to evaluate typography pairings. Created by [Sergey Bulaev](https://t.me/sergiobulaev).

## Features

- Automatic font downloading from Google Fonts
- High-quality preview generation with sample content
- Light and dark theme variations
- QR code integration for quick access
- Comparison view of multiple font combinations
- Professional typography hierarchy demonstration
- Button and interactive element previews

## Installation

1. Clone the repository:

    git clone https://github.com/sergiobulaev/font-pairing.git
    cd font-pairing

2. Create a virtual environment (recommended):

    python -m venv myenv
    source myenv/bin/activate  # On Windows use: myenv\Scripts\activate

3. Install dependencies:

    pip install -r requirements.txt

## Usage

Simply run the script to generate all previews:

    python check.py

This will:
1. Download required fonts from Google Fonts (if not already present)
2. Generate individual previews for each font combination
3. Create a comparison image showing all combinations
4. Save all previews in the `font_previews` directory

## Available Font Combinations

Currently supports the following font pairs:
- Space Grotesk + Inter
- Space Grotesk + Outfit
- Space Grotesk + DM Sans
- Space Grotesk + Public Sans

## Output

The script generates:
- Individual preview images for each font combination
- A comprehensive comparison image
- All images include:
  - Typography samples in different sizes
  - Light and dark theme variations
  - Interactive elements (buttons)
  - QR code linking to the creator's Telegram channel

## Directory Structure

    font-pairing/
    ├── check.py           # Main script
    ├── requirements.txt   # Dependencies
    ├── README.md         # Documentation
    ├── fonts/            # Downloaded fonts directory
    └── font_previews/    # Generated previews

## Requirements

- Python 3.7+
- Pillow
- requests
- qrcode

## Contributing

Feel free to open issues or submit pull requests with improvements.

## Author

Created by [Sergey Bulaev](https://t.me/sergiobulaev) - Follow for more AI and development content.

## License

MIT License - feel free to use in your projects.