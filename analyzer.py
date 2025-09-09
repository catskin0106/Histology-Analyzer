from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def analyze_image_colors(image_path, num_colors): ## Find most prevalent colors & their %
    try:
        img = Image.open(image_path) 
        img = img.convert("RGB") 
        imgquantized = img.quantize(colors=num_colors, method=1)
        ##methods: Median Cut / Maximum Coverage / Fast Octree
        totalpixel = imgquantized.size[0]*imgquantized.size[1]
        plt.imshow(imgquantized)
        plt.show()
        colorfreq = imgquantized.getcolors(totalpixel) 
        palette = imgquantized.getpalette() 

        maincolors = []
        for count, color_index in sorted(colorfreq, reverse=True):
            start_index = color_index * 3
            rgb_color = tuple(palette[start_index : start_index + 3]) 
            percentage = count / totalpixel *100
            maincolors.append((rgb_color,percentage))
        return maincolors, imgquantized
    
    except FileNotFoundError:
        print(f"Error: the file '{image_path}' is not found")
        return None
    except Exception as e:
        print (f"An exception has occurred: {e}")
        return None

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

def masks(imgquantized,data):
    return

##==Config==##
ColorAmount = 10
ImagePath = 'D:\Coding\multiplexthingy\Histology-Analyzer\Images\image.png'
QuantizeToPalette = False ##If True, Manually set the colors of the stain 
Task = 'Colorplot'
##==========##

output, imgquantized = analyze_image_colors(ImagePath,ColorAmount)
print(output)
if Task == 'Colorplot':
    colorplot(output)