from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import json
import cv2
from IPython.display import display

def load_stain_database(db_path):
    try:
        with open(db_path, 'r') as f:
            stain_database = json.load(f)
        print(f"Successfully loaded stain database from '{db_path}'.")
        return stain_database
    except FileNotFoundError:
        print(f"Error: Database file not found at '{db_path}'.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not parse '{db_path}'. Please check if it is a valid JSON file.")
        return None

def analyze_image_colors(image_path, num_colors, qalgo, palettebool, custom_palette): ## Find most prevalent colors & their %
    try:
        img = Image.open(image_path) 
        img = img.convert("RGB")
        if palettebool and custom_palette:
            imgquantized = quantize_to_palette(img, custom_palette)
        else:
            imgquantized = img.quantize(colors=num_colors, method=qalgo) ##Auto Quantization
        totalpixel = imgquantized.size[0]*imgquantized.size[1]
        plt.imshow(imgquantized)
        plt.title("Quantized Image")
        plt.show()
        colorfreq = imgquantized.getcolors(totalpixel) ##2D array of [freq,color id (0 to num_colors)]
        palette = imgquantized.getpalette() ##rgb values for each color id

        maincolors = []
        for count, color_index in sorted(colorfreq, reverse=True):
            start_index = color_index * 3
            rgb_color = tuple(palette[start_index : start_index + 3]) ##3D array of RGB values
            percentage = count / totalpixel *100
            maincolors.append((rgb_color,percentage))
        return maincolors, imgquantized
    
    except FileNotFoundError:
        print(f"Error: the file '{image_path}' is not found")
        return None
    except Exception as e:
        print (f"An exception has occurred: {e}")
        return None
    
def quantize_to_palette(img, custom_palette):
    palette_dummy = Image.new("P", (1, 1)) ##Create dummy to hold palette
    flat_palette = [value for color in custom_palette for value in color]
    palette_dummy.putpalette(flat_palette) ##Put palette in dummy
    imgquantized = img.convert("RGB").quantize(palette=palette_dummy, dither=Image.Dither.NONE)
    return imgquantized

def colorplot(colordata):
    if not colordata:
        print("No color data to plot bruh")
        return
    
    colors = [item[0] for item in colordata]
    percentages = [item[1] for item in colordata]

    plot_colors = [tuple(c / 255 for c in color) for color in colors]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(colors)), percentages, color=plot_colors, edgecolor='black')

    ax.set_title('Percentage of Stain in Image', fontsize=16)
    ax.set_ylabel('Percentage', fontsize=16)
    ax.set_xticks(range(len(colors)))
    ax.set_xticklabels([f'RGB\n{c}' for c in colors], rotation=45, ha="right", fontsize=10)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def masks(imgquantized, color_index):
    image_array = np.array(imgquantized)
    mask = (image_array == color_index) ##Creates a bool mask where entry n = true if image_array[n]==color_index[n]
    mask_array = (mask * 255).astype('uint8') ##true*255=255 this is so poggers
    mask_image = Image.fromarray(mask_array, mode='L') ##L=8bit greyscale; +(255,255,255) -(0,0,0)
    plt.imshow(mask_image, cmap='gray')
    plt.title(f"Image Mask for Color Index '{color_index}'")
    plt.show()
    return mask_image

def heatmap(ImagePath,mask_image,kernel_size,alpha):
    mask_cv = np.array(mask_image)
    density_map_grey = cv2.GaussianBlur(mask_cv, (kernel_size,kernel_size), 0)
    heatmap = cv2.applyColorMap(density_map_grey, cv2.COLORMAP_INFERNO)
    original_cv = cv2.imread(str(ImagePath))
    overlaid_image = cv2.addWeighted(original_cv, 1 - alpha, heatmap, alpha, 0)
    cv2.imshow('Density Heatmap', overlaid_image)
    cv2.imshow('Original Mask', mask_cv) # Also show the mask for comparison
    print("\nDisplaying heatmap. Press any key in the image window to close.")
    cv2.waitKey(0) # Wait for the user to press a key
    cv2.destroyAllWindows() # Close all OpenCV windows
    return