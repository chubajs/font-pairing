import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import qrcode
from datetime import datetime

class FontManager:
    def __init__(self, fonts_dir="fonts"):
        self.fonts_dir = fonts_dir
        self.fonts_data = {
            "SpaceGrotesk": {
                "css_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500&display=swap",
                "filename": "spacegrotesk.ttf",
            },
            "Inter": {
                "css_url": "https://fonts.googleapis.com/css2?family=Inter&display=swap",
                "filename": "inter.ttf",
            },
            "Outfit": {
                "css_url": "https://fonts.googleapis.com/css2?family=Outfit&display=swap",
                "filename": "outfit.ttf",
            },
            "DMSans": {
                "css_url": "https://fonts.googleapis.com/css2?family=DM+Sans&display=swap",
                "filename": "dmsans.ttf",
            },
            "PublicSans": {
                "css_url": "https://fonts.googleapis.com/css2?family=Public+Sans&display=swap",
                "filename": "publicsans.ttf",
            }
        }
        
        # Create fonts directory if it doesn't exist
        os.makedirs(self.fonts_dir, exist_ok=True)

    def get_ttf_url(self, css_url):
        """Extract the TTF font file URL from Google Fonts CSS"""
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/css,*/*;q=0.1'
        }
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        
        # Find the URL in the CSS content
        css_content = response.text
        url_start = css_content.find("url(") + 4
        url_end = css_content.find(")", url_start)
        font_url = css_content[url_start:url_end].strip("'\"")
        
        return font_url

    def download_font(self, font_name):
        """Download font if it doesn't exist"""
        font_data = self.fonts_data[font_name]
        font_path = os.path.join(self.fonts_dir, font_data["filename"])
        
        # Check if font already exists
        if os.path.exists(font_path):
            print(f"Font {font_name} already exists")
            return font_path
        
        print(f"Downloading {font_name}...")
        try:
            # Get the TTF URL from Google Fonts CSS
            ttf_url = self.get_ttf_url(font_data["css_url"])
            
            # Download the font file
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': '*/*'
            }
            response = requests.get(ttf_url, headers=headers)
            response.raise_for_status()
            
            # Save the font file
            with open(font_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Successfully downloaded {font_name}")
            return font_path
                
        except Exception as e:
            print(f"Error downloading {font_name}: {e}")
            return None

    def ensure_all_fonts(self):
        """Make sure all required fonts are available"""
        missing_fonts = []
        for font_name in self.fonts_data.keys():
            font_path = os.path.join(self.fonts_dir, self.fonts_data[font_name]["filename"])
            if not os.path.exists(font_path):
                if not self.download_font(font_name):
                    missing_fonts.append(font_name)
        
        return len(missing_fonts) == 0, missing_fonts

    def verify_font(self, font_path):
        """Verify if a font file is valid by attempting to load it"""
        try:
            font = ImageFont.truetype(font_path, size=24)
            font.getbbox("Test String")
            return True
        except Exception as e:
            print(f"Font verification failed for {font_path}: {e}")
            return False

def create_font_preview(headline_font_name, body_font_name, fonts_dir="fonts", output_dir="font_previews"):
    """Create a preview image showcasing font pairs in different combinations with varied typography"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Image settings
    width = 1400
    height = 1400  # Increased height for more content
    background_color = (252, 252, 252)
    headline_color = (10, 47, 47)     # #0A2F2F
    body_color = (71, 85, 105)        # Slate-600
    accent_color = (20, 184, 166)     # #14B8A6
    muted_color = (100, 116, 139)     # Slate-500
    card_color = (255, 255, 255)
    card_border = (226, 232, 240)
    
    # Update card settings
    card_border_width = 2
    card_padding = 40
    card_height = 380
    button_margin_bottom = 80
    caption_margin_bottom = 25
    
    # Adjust vertical spacing
    row_spacing = 400  # Increased from 360 to prevent overlap
    columns_y = 240    # Starting Y position for first row
    
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # Load fonts with more size variations
        headline_font_path = os.path.join(fonts_dir, f"{headline_font_name.lower()}.ttf")
        body_font_path = os.path.join(fonts_dir, f"{body_font_name.lower()}.ttf")
        
        if not all(os.path.exists(p) for p in [headline_font_path, body_font_path]):
            raise Exception("Required fonts not found")
        
        # Load all font sizes
        h1 = ImageFont.truetype(headline_font_path, size=72)
        h2 = ImageFont.truetype(headline_font_path, size=44)
        h3 = ImageFont.truetype(headline_font_path, size=36)
        h4 = ImageFont.truetype(headline_font_path, size=28)
        h5 = ImageFont.truetype(headline_font_path, size=24)
        body_xlarge = ImageFont.truetype(body_font_path, size=22)
        body_large = ImageFont.truetype(body_font_path, size=18)
        body_regular = ImageFont.truetype(body_font_path, size=16)
        body_small = ImageFont.truetype(body_font_path, size=14)
        caption = ImageFont.truetype(body_font_path, size=12)
        
        # Load bold variants for system info
        try:
            body_regular_bold = ImageFont.truetype(body_font_path, size=16, index=1)
            body_small_bold = ImageFont.truetype(body_font_path, size=14, index=1)
        except:
            # Fallback to regular weight if bold is not available
            body_regular_bold = body_regular
            body_small_bold = body_small
        
        # Create fonts dictionary for card drawing
        fonts = {
            "h1": h1,
            "h2": h2,
            "h3": h3,
            "h4": h4,
            "h5": h5,
            "body_xlarge": body_xlarge,
            "body_large": body_large,
            "body_regular": body_regular,
            "body_small": body_small,
            "caption": caption,
            "body_regular_bold": body_regular_bold,
            "body_small_bold": body_small_bold
        }
        
        # Main title section (centered, top)
        title = "Typography Exploration"
        title_bbox = draw.textbbox((0, 0), title, font=fonts["h1"])
        title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
        draw.text((title_x, 60), title, font=fonts["h1"], fill=headline_color)
        
        # Subtitle with more spacing
        subtitle = f"A Visual Study of {headline_font_name} + {body_font_name}"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=fonts["body_xlarge"])
        subtitle_x = (width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2
        draw.text((subtitle_x, 160), subtitle, font=fonts["body_xlarge"], fill=body_color)
        
        # Content pairs with varied text sizes and proper line breaks
        content_pairs = [
            {
                "title": "Digital Innovation",
                "subtitle": "Transforming the Future",
                "eyebrow": "TECHNOLOGY",
                "body_large": (
                    "Artificial intelligence and machine learning are\n"
                    "revolutionizing how we interact with technology."
                ),
                "body_regular": (
                    "These groundbreaking advances are creating unprecedented\n"
                    "opportunities for innovation and growth across industries."
                ),
                "button_text": "Explore AI Solutions",
                "caption": "Sergey Bulaev AI • AI use cases for everyone"
            },
            {
                "title": "User Experience",
                "subtitle": "Designing for Humans",
                "eyebrow": "DESIGN",
                "body_large": (
                    "Great design puts human needs first. Understanding\n"
                    "user behavior and psychology."
                ),
                "body_regular": (
                    "We create intuitive interfaces that delight users while\n"
                    "solving complex problems effectively."
                ),
                "button_text": "Learn More",
                "caption": "Updated weekly • Latest trends in UX"
            },
            {
                "title": "Data Privacy",
                "subtitle": "Protecting Digital Rights",
                "eyebrow": "SECURITY",
                "body_large": (
                    "In our interconnected world, protecting personal\n"
                    "data has become crucial."
                ),
                "body_regular": (
                    "Organizations must implement robust security measures\n"
                    "while maintaining transparency."
                ),
                "button_text": "View Guidelines",
                "caption": "Essential reading • Security guidelines"
            },
            {
                "title": "Sustainability",
                "subtitle": "Building Tomorrow",
                "eyebrow": "ENVIRONMENT",
                "body_large": (
                    "Environmental consciousness is reshaping how we\n"
                    "approach development."
                ),
                "body_regular": (
                    "From renewable energy to sustainable materials, every\n"
                    "choice impacts our future."
                ),
                "button_text": "Join Initiative",
                "caption": "Ongoing initiative • Join the movement"
            }
        ]

        # Draw columns with adjusted spacing
        margin = 70
        column_width = (width - (3 * margin)) // 2
        
        # Draw cards in row order to ensure proper layering
        for row in range(2):  # 2 rows
            for col in range(2):  # 2 columns
                i = row * 2 + col
                if i >= len(content_pairs):
                    continue
                
                content = content_pairs[i]
                x = margin + (col * (column_width + margin))
                y = columns_y + (row * row_spacing)
                
                # Determine if this should be an inverted card (right column)
                is_inverted = (col == 1)
                card_bg = headline_color if is_inverted else card_color
                text_color = (255, 255, 255) if is_inverted else headline_color
                body_text_color = (255, 255, 255) if is_inverted else body_color
                
                # Draw card using helper function
                draw_card(draw, content, x, y, column_width, card_height,
                         card_bg, card_border, text_color, body_text_color, accent_color,
                         fonts, card_padding, button_margin_bottom, caption_margin_bottom)

        # Bottom section y-position
        bottom_y = height - 200
        
        # Add Telegram section (left) and get QR bottom position
        qr_bottom = draw_telegram_section(draw, image, width, bottom_y, fonts, headline_color)
        
        # Add service information (right)
        right_margin = 70
        right_x = width - right_margin
        line_spacing = 30
        
        # Font information aligned with bottom of QR
        font_info = f"{headline_font_name} for Headlines • {body_font_name} for Body Text"
        font_bbox = draw.textbbox((0, 0), font_info, font=fonts["body_regular_bold"])  # Using bold font
        font_width = font_bbox[2] - font_bbox[0]
        font_x = right_x - font_width
        draw.text((font_x, qr_bottom - 45),  # Position relative to QR bottom
                  font_info, font=fonts["body_regular_bold"], fill=body_color)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_text = f"Generated on {timestamp}"
        timestamp_bbox = draw.textbbox((0, 0), timestamp_text, font=fonts["body_small_bold"])  # Using bold font
        timestamp_width = timestamp_bbox[2] - timestamp_bbox[0]
        timestamp_x = right_x - timestamp_width
        draw.text((timestamp_x, qr_bottom - 20),  # Position relative to QR bottom
                  timestamp_text, font=fonts["body_small_bold"], fill=muted_color)

        # Save the image
        output_filename = f"{headline_font_name.lower()}_{body_font_name.lower()}.png"
        output_path = os.path.join(output_dir, output_filename)
        image.save(output_path, quality=95)
        print(f"Created {output_path}")
        
    except Exception as e:
        print(f"Error creating preview for {headline_font_name} + {body_font_name}: {e}")

def create_font_comparison(fonts_dir="fonts", output_dir="font_previews"):
    """Create a single large image comparing all font combinations"""
    font_pairs = [
        ("SpaceGrotesk", "Inter"),
        ("SpaceGrotesk", "Outfit"),
        ("SpaceGrotesk", "DMSans"),
        ("SpaceGrotesk", "PublicSans")
    ]
    
    # Image settings
    preview_width = 1400
    preview_height = 1000  # Reduced height for comparison
    padding = 100
    footer_height = 200  # Height for QR code and system info
    
    # Calculate full image dimensions for horizontal layout
    total_width = (preview_width + padding) * len(font_pairs) + padding
    total_height = preview_height + (padding * 2) + footer_height
    
    # Create comparison image
    comparison = Image.new('RGB', (total_width, total_height), (252, 252, 252))
    draw = ImageDraw.Draw(comparison)
    
    try:
        # Load body font for system info (using Inter)
        body_font_path = os.path.join(fonts_dir, "inter.ttf")
        if not os.path.exists(body_font_path):
            raise Exception("Required font not found")
            
        # Load fonts for system info
        body_regular = ImageFont.truetype(body_font_path, size=16)
        body_small = ImageFont.truetype(body_font_path, size=14)
        try:
            body_regular_bold = ImageFont.truetype(body_font_path, size=16, index=1)
            body_small_bold = ImageFont.truetype(body_font_path, size=14, index=1)
        except:
            body_regular_bold = body_regular
            body_small_bold = body_small
        
        # Colors
        headline_color = (10, 47, 47)
        body_color = (71, 85, 105)
        muted_color = (100, 116, 139)
        
        # Add each preview
        for i, (headline_font, body_font) in enumerate(font_pairs):
            # Create preview image
            preview = create_preview_for_comparison(headline_font, body_font, preview_width, preview_height)
            
            # Calculate position
            x_pos = padding + i * (preview_width + padding)
            y_pos = padding
            
            # Paste preview
            comparison.paste(preview, (x_pos, y_pos))
            
            # Add font info under each preview
            font_info = f"{headline_font} for Headlines\n{body_font} for Body Text"
            info_x = x_pos + (preview_width // 2)
            info_y = y_pos + preview_height + 20
            
            # Draw centered font info
            for line in font_info.split('\n'):
                bbox = draw.textbbox((0, 0), line, font=body_regular_bold)
                text_width = bbox[2] - bbox[0]
                text_x = info_x - (text_width // 2)
                draw.text((text_x, info_y), line, font=body_regular_bold, fill=body_color)
                info_y += 25
        
        # Add footer with QR code and generation info
        footer_y = total_height - footer_height
        
        # Add Telegram section with QR code (centered)
        qr_bottom = draw_telegram_section(
            draw, comparison, total_width // 2, footer_y + 20,
            {"body_regular": body_regular, "body_large": body_regular, 
             "body_regular_bold": body_regular_bold}, headline_color
        )
        
        # Add generation timestamp (centered)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_text = f"Generated on {timestamp}"
        bbox = draw.textbbox((0, 0), timestamp_text, font=body_small_bold)
        text_width = bbox[2] - bbox[0]
        text_x = (total_width - text_width) // 2
        draw.text((text_x, qr_bottom + 20), 
                  timestamp_text, font=body_small_bold, fill=muted_color)
        
        # Save comparison image
        output_path = os.path.join(output_dir, "font_comparison.png")
        comparison.save(output_path, quality=95)
        print(f"Created font comparison at {output_path}")
        
    except Exception as e:
        print(f"Error creating font comparison: {e}")

def create_preview_for_comparison(headline_font, body_font, width, height):
    """Create a preview image for the comparison without footer section"""
    # ... (existing preview creation code, but with reduced height
    # and without footer section)

def create_qr_code(url, size=120):
    """Create a QR code for the given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((size, size), Image.Resampling.LANCZOS)
    return qr_image

def draw_button_with_shadow(draw, x, y, width, height, bg_color, text, font, text_color):
    """Draw a button with shadow effect"""
    # Create a new image for the button with space for shadow
    button_image = Image.new('RGBA', (width + 4, height + 4), (0, 0, 0, 0))
    button_draw = ImageDraw.Draw(button_image)
    
    # Draw shadow
    shadow_color = (0, 0, 0, 50)  # Semi-transparent black
    button_draw.rounded_rectangle(
        [2, 2, width + 2, height + 2],
        radius=8,
        fill=shadow_color
    )
    
    # Draw button
    button_draw.rounded_rectangle(
        [0, 0, width, height],
        radius=8,
        fill=bg_color
    )
    
    # Draw text
    text_bbox = button_draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - 1
    
    # Version with shadow
    shadow_offset = 1
    button_draw.text((text_x + shadow_offset, text_y + shadow_offset), 
                     text, font=font, fill=(0, 0, 0, 60))  # Text shadow
    button_draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return button_image

def draw_telegram_section(draw, image, width, y_position, fonts, text_color):
    """Draw Telegram channel link and QR code in the bottom left corner with text on the right"""
    telegram_url = "https://t.me/sergiobulaev"
    channel_name = "Sergey Bulaev AI"
    channel_description = "AI use cases for everyone"
    
    # Create QR code
    qr_size = 120  # QR code size
    qr_image = create_qr_code(telegram_url, size=qr_size)
    
    # Calculate positions for left corner
    margin = 70  # Match card margin
    qr_x = margin
    qr_y = y_position
    
    # Convert QR to RGBA if needed
    if qr_image.mode != 'RGBA':
        qr_image = qr_image.convert('RGBA')
    
    # Paste QR code
    image.paste(qr_image, (qr_x, qr_y), qr_image)
    
    # Position text to the right of QR code
    text_x = qr_x + qr_size + 30  # Add some spacing after QR
    
    # Calculate vertical positions from bottom of QR
    text_bottom = qr_y + qr_size
    line_spacing = 25
    
    # Draw description (bottom)
    draw.text((text_x, text_bottom - line_spacing), 
              channel_description, font=fonts["body_regular"], fill=text_color)
    
    # Draw Telegram link (middle)
    draw.text((text_x, text_bottom - (line_spacing * 2)), 
              telegram_url, font=fonts["body_large"], fill=text_color)
    
    # Draw channel name (top)
    draw.text((text_x, text_bottom - (line_spacing * 3)), 
              channel_name, font=fonts["body_regular_bold"], fill=text_color)
    
    return qr_y + qr_size  # Return bottom of QR code for system info alignment

def draw_card(draw, content, x, y, width, height, bg_color, border_color, 
              text_color, body_text_color, accent_color, fonts, padding,
              button_margin_bottom, caption_margin_bottom):
    """Helper function to draw a card with given colors"""
    # Draw card background
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=12,
        fill=bg_color,
        outline=border_color,
        width=2
    )
    
    # Content positioning
    content_x = x + padding
    content_y = y + padding
    
    # Draw eyebrow
    draw.text((content_x, content_y), content["eyebrow"], 
              font=fonts["body_small"], fill=accent_color)
    
    # Draw title
    draw.text((content_x, content_y + 30), content["title"], 
              font=fonts["h2"], fill=text_color)
    
    # Draw subtitle
    draw.text((content_x, content_y + 85), content["subtitle"],
              font=fonts["h5"], fill=accent_color)
    
    # Draw body text
    line_height_large = 28
    line_height_regular = 24
    
    y_offset = content_y + 130
    for line in content["body_large"].split('\n'):
        draw.text((content_x, y_offset), line.strip(),
                  font=fonts["body_large"], fill=body_text_color)
        y_offset += line_height_large
    
    y_offset = content_y + 190
    for line in content["body_regular"].split('\n'):
        draw.text((content_x, y_offset), line.strip(),
                  font=fonts["body_regular"], fill=body_text_color)
        y_offset += line_height_regular
    
    # Draw button with shadow
    button_text = content["button_text"]
    button_padding = 20
    button_height = 44
    button_bbox = draw.textbbox((0, 0), button_text, font=fonts["body_regular"])
    button_width = button_bbox[2] - button_bbox[0] + (button_padding * 2)
    max_button_width = width - (2 * padding)
    button_width = min(button_width, max_button_width)
    
    button_y = y + height - button_margin_bottom
    
    # Create and paste button with shadow
    button_bg_color = accent_color if bg_color == (255, 255, 255) else (255, 255, 255)
    button_text_color = (255, 255, 255) if bg_color == (255, 255, 255) else accent_color
    
    button_image = draw_button_with_shadow(
        draw, content_x, button_y, button_width, button_height,
        button_bg_color, button_text, fonts["body_regular"], button_text_color
    )
    
    # Draw caption
    caption_y = y + height - caption_margin_bottom
    caption_text = f"{content['caption']} • t.me/sergiobulaev"
    draw.text((content_x, caption_y), caption_text, 
              font=fonts["caption"], fill=body_text_color)

def generate_all_previews():
    """Generate individual previews and comparison image"""
    # Initialize font manager
    font_manager = FontManager()
    
    # Ensure all fonts are available
    success, missing_fonts = font_manager.ensure_all_fonts()
    if not success:
        print(f"Error: Could not download the following fonts: {', '.join(missing_fonts)}")
        return
    
    # Create or clean the output directory
    output_dir = "font_previews"
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith('.png'):
                os.remove(os.path.join(output_dir, file))
        print("Cleaned existing previews")
    else:
        os.makedirs(output_dir)
        print("Created previews directory")
    
    # Generate individual previews
    font_pairs = [
        ("SpaceGrotesk", "Inter"),
        ("SpaceGrotesk", "Outfit"),
        ("SpaceGrotesk", "DMSans"),
        ("SpaceGrotesk", "PublicSans")
    ]
    
    for headline_font, body_font in font_pairs:
        create_font_preview(headline_font, body_font)
    
    # Generate comparison image
    create_font_comparison()

def verify_existing_fonts():
    """Test function to verify all downloaded fonts"""
    font_manager = FontManager()
    print("Verifying existing fonts...")
    
    for font_name in font_manager.fonts_data.keys():
        font_path = os.path.join(font_manager.fonts_dir, font_manager.fonts_data[font_name]["filename"])
        if os.path.exists(font_path):
            if font_manager.verify_font(font_path):
                print(f"✓ {font_name} is valid")
            else:
                print(f"✗ {font_name} is invalid")
        else:
            print(f"- {font_name} does not exist")

if __name__ == "__main__":
    print("Checking and downloading fonts...")
    generate_all_previews()
    print("Done!")
    verify_existing_fonts()