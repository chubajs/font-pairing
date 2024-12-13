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
- Space Grotesk + Plus Jakarta Sans

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

## Font Selection

To generate font pairs for comparison, you can use an AI assistant like Claude with the following prompt (copy everything after the line):

---
I need help selecting Google Fonts pairs for Space Grotesk. I'm looking for:
1. Space Grotesk will be used for headlines
2. I need 4-5 clean, highly readable sans-serif fonts that would pair well with Space Grotesk for body text

For each font, please provide:
- Font name as used in Google Fonts
- CSS import URL
- Brief explanation of why this font pairs well with Space Grotesk

Please format the output so it can be added to a fonts.txt file with the structure:
FontName|css_url
---

The fonts.txt file should follow this format:

Font pairs for comparison (one per line)
Main Font + BodyFont1
Main Font + BodyFont2
Main Font + BodyFont3
Main Font + BodyFont4

Available fonts
Format: FontName|css_url
Space Grotesk|https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap
BodyFont1|css_import_url
BodyFont2|css_import_url
BodyFont3|css_import_url
BodyFont4|css_import_url

Note: Font names can contain spaces (like "Plus Jakarta Sans"). The script will handle spaces in font names correctly.