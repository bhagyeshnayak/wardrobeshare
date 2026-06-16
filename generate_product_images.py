"""
Utility script to generate product images using Pillow
Creates realistic-looking product placeholder images for the wardrobeshare application
"""
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / 'media' / 'products'

# Ensure media/products directory exists
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def create_product_image(filename, title, color_rgb, icon_text):
    """
    Create a professional product placeholder image
    
    Args:
        filename: Output filename (e.g., 'red_dress.jpg')
        title: Product title to display
        color_rgb: Background color as RGB tuple
        icon_text: Large text to display as icon (e.g., '👗')
    """
    # Image dimensions (matching typical product photos)
    width, height = 800, 1000
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Create subtle gradient effect
    for i in range(height):
        # Darken towards bottom
        factor = 1 - (i / height) * 0.2
        adjusted_color = tuple(int(c * factor) for c in color_rgb)
        draw.line([(0, i), (width, i)], fill=adjusted_color)
    
    # Add centered product icon/emoji
    try:
        # Try to use a larger font for the emoji/icon
        font_size = 200
        try:
            # Try to use system font
            font = ImageFont.truetype("seguiemj.ttf", font_size)  # Windows emoji font
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Draw icon text centered
        bbox = draw.textbbox((0, 0), icon_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 100
        
        # Add shadow effect
        shadow_offset = 5
        draw.text((x + shadow_offset, y + shadow_offset), icon_text, 
                 fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), icon_text, fill='white', font=font)
    except Exception as e:
        print(f"Warning: Could not add icon text: {e}")
    
    # Add product title at bottom
    try:
        title_font_size = 40
        try:
            title_font = ImageFont.truetype("arial.ttf", title_font_size)
        except:
            title_font = ImageFont.load_default()
        
        # Draw title with background
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        title_x = (width - title_width) // 2
        title_y = height - 100
        
        # Background rectangle for title
        padding = 20
        draw.rectangle([
            (title_x - padding, title_y - padding),
            (title_x + title_width + padding, title_y + title_height + padding)
        ], fill=(0, 0, 0, 180))
        
        draw.text((title_x, title_y), title, fill='white', font=title_font)
    except Exception as e:
        print(f"Warning: Could not add title: {e}")
    
    # Add subtle border
    border_width = 3
    draw.rectangle([
        (border_width, border_width),
        (width - border_width, height - border_width)
    ], outline='white', width=border_width)
    
    # Save image
    output_path = MEDIA_DIR / filename
    img.save(output_path, 'JPEG', quality=95)
    print(f"✅ Created: {output_path}")
    return output_path

def generate_all_images():
    """Generate all product images"""
    print("🎨 Generating product images using Pillow...")
    print(f"📁 Output directory: {MEDIA_DIR}\n")
    
    images = [
        {
            'filename': 'red_evening_dress.jpg',
            'title': 'Red Evening Dress',
            'color': (220, 53, 69),  # Red
            'icon': '👗'
        },
        {
            'filename': 'black_suit.jpg',
            'title': 'Black Suit',
            'color': (52, 58, 64),  # Dark gray/black
            'icon': '🤵'
        },
        {
            'filename': 'leather_jacket.jpg',
            'title': 'Leather Jacket',
            'color': (139, 90, 43),  # Brown
            'icon': '🧥'
        },
        {
            'filename': 'floral_summer_dress.jpg',
            'title': 'Floral Summer Dress',
            'color': (255, 193, 203),  # Pink
            'icon': '🌸'
        },
        {
            'filename': 'designer_handbag.jpg',
            'title': 'Designer Handbag',
            'color': (222, 184, 135),  # Beige
            'icon': '👜'
        }
    ]
    
    created_count = 0
    for img_data in images:
        try:
            create_product_image(
                img_data['filename'],
                img_data['title'],
                img_data['color'],
                img_data['icon']
            )
            created_count += 1
        except Exception as e:
            print(f"❌ Error creating {img_data['filename']}: {e}")
    
    print(f"\n✅ Successfully created {created_count}/{len(images)} images")
    print(f"📂 Images saved to: {MEDIA_DIR}")

if __name__ == '__main__':
    generate_all_images()
