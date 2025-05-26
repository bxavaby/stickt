#!/usr/bin/env python3
"""
Interactive Sticker Generator using fofr/sticker-maker on Replicate
"""

import replicate
import os
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ASPECT_RATIOS = {
    "1": {"name": "Square (1:1)", "width": 1024, "height": 1024},
    "2": {"name": "Portrait (3:4)", "width": 768, "height": 1024},
    "3": {"name": "Landscape (4:3)", "width": 1024, "height": 768},
    "4": {"name": "Wide (16:9)", "width": 1024, "height": 576},
    "5": {"name": "Ultra Wide (21:9)", "width": 1024, "height": 438},
    "6": {"name": "Instagram Story (9:16)", "width": 576, "height": 1024},
    "7": {"name": "Instagram Post (1:1)", "width": 1080, "height": 1080},
    "8": {"name": "Icon/Logo (512x512)", "width": 512, "height": 512},
}

OUTPUT_FORMATS = {
    "1": {"ext": "webp", "name": "WebP (smaller file, good quality)"},
    "2": {"ext": "png", "name": "PNG (larger file, perfect quality)"},
}

generation_count = 0
estimated_cost_per_generation = 0.01

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def select_aspect_ratio():
    clear_screen()
    print("Aspect Ratios:")
    for key, ratio in ASPECT_RATIOS.items():
        print(f"  {key}. {ratio['name']}")

    while True:
        choice = input("\nPick aspect ratio: ").strip()
        if choice in ASPECT_RATIOS:
            selected = ASPECT_RATIOS[choice]
            return selected['width'], selected['height']
        print("Invalid choice. Enter 1-8.")

def select_output_format():
    """Select output format"""
    clear_screen()
    print("Output Formats:")
    for key, fmt in OUTPUT_FORMATS.items():
        print(f"  {key}. {fmt['name']}")

    while True:
        choice = input("\nPick output format: ").strip()
        if choice in OUTPUT_FORMATS:
            return OUTPUT_FORMATS[choice]['ext']
        print("Invalid choice. Enter 1-2.")

def get_prompt():
    """Get sticker description"""
    clear_screen()
    while True:
        prompt = input("Sticker description: ").strip()
        if prompt:
            return prompt
        print("Please enter a description.")

def get_filename():
    """Get output filename"""
    clear_screen()
    while True:
        filename = input("Filename (without extension): ").strip()
        if filename:
            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
            return safe_filename.replace(' ', '_')
        print("Please enter a filename.")

def generate_sticker():
    global generation_count

    api_key = os.getenv('REPLICATE_API_TOKEN')
    if not api_key:
        clear_screen()
        print("Error: REPLICATE_API_TOKEN not found in environment")
        print("Set it with: export REPLICATE_API_TOKEN=your_token")
        return False

    output_dir = Path("./stickers")
    output_dir.mkdir(exist_ok=True)

    clear_screen()
    print("STICKT - Sticker Generator")
    print("-" * 40)

    width, height = select_aspect_ratio()
    output_format = select_output_format()
    prompt = get_prompt()
    filename = get_filename()

    clear_screen()
    print("STICKT - Sticker Generator")
    print("-" * 40)
    print(f"Generating: {prompt}")
    print(f"Size: {width}x{height}")
    print(f"Format: {output_format.upper()}")
    print(f"Output: ./stickers/{filename}.{output_format}")
    print("\nProcessing...")

    output_file = output_dir / f"{filename}.{output_format}"

    try:
        output = replicate.run(
            "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            input={
                "prompt": prompt,
                "width": width,
                "height": height,
                "output_quality": 100,
                "steps": 20,
                "guidance_scale": 7.5,
            }
        )

        if isinstance(output, list) and len(output) > 0:
            image_url = output[0]
            response = requests.get(image_url)
            response.raise_for_status()

            with open(output_file, "wb") as file:
                file.write(response.content)

            generation_count += 1
        else:
            print("Error: Unexpected API response format")
            return False

        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            file_size = os.path.getsize(output_file) / 1024
            print(f"Saved: {output_file} ({file_size:.1f} KB)")

            try:
                subprocess.run(['xdg-open', str(output_file)], check=False,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Opening preview...")
            except:
                print("Preview unavailable - file saved successfully")

            return True
        else:
            print("Error: File was not saved properly")
            return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def show_session_summary():
    if generation_count > 0:
        estimated_total = generation_count * estimated_cost_per_generation
        print("Session Summary:")
        print(f"  Generated: {generation_count} sticker{'s' if generation_count != 1 else ''}")
        print(f"  Estimated cost: ~${estimated_total:.2f} USD")
        print("  (Check replicate.com/account for actual usage)")

def main():
    clear_screen()
    while True:
        if not generate_sticker():
            break

        print("\n" + "-" * 40)
        if input("Generate another? (y/n): ").strip().lower() not in ['y', 'yes']:
            break

    clear_screen()
    if generation_count > 0:
        show_session_summary()
        print()
    print("Done.")

if __name__ == '__main__':
    main()
