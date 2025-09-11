from analyzer import *
from pathlib import Path
import os

script_directory = Path(__file__).resolve().parent

##==Config (Main)==##

ImagePath = script_directory / 'Images' / 'image.png'
PaletteDBPath = script_directory / 'palette.json'
Task = 'Mask'

##==Config (Quantize)==##

QuantizeToPalette = True ##False=AUTO PALETTE / True=MANUAL PALETTE
SaveColorPlotImage = False
SavePathColorPlot = ''
    ##If QuantizeToPalette is False: (Auto)
ColorAmount = 4
QuantizeAlgorithm = 1 ##0(Median Cut) / 1(Maximum Coverage) / 2(Fast Octree)
    ##If QuantizeToPalette is True: (Manual)
StainType = "H&E" ##Check palette.json

##==Config (Mask)==##

SaveMaskImage = False
SavePathMask = '' ##Configure the Directory of the saved image

##==========##

if QuantizeToPalette == True:
    StainDB = load_stain_database(PaletteDBPath)
    if StainType not in StainDB:
        print(f"Error: Stain type '{StainType}' not found in the database.")
        print("Available types are:", list(StainDB.keys()))
    stain_info = StainDB[StainType]
    custom_palette = stain_info['palette']
    color_names = stain_info['color_names']
else:
    custom_palette= 0
output, imgquantized = analyze_image_colors(ImagePath,ColorAmount,QuantizeAlgorithm,QuantizeToPalette,custom_palette)
print(output)
if Task == 'Colorplot':
    colorplot(output)
if Task == 'Mask':
    colorplot(output)
    print("Type in the index of the color to be masked:")
    if QuantizeToPalette == True:
        color_index=int(input("Index: Order of Color in palette.json (Start from 0)"))
    else:
        color_index=int(input("Index: Order of Color from the Color Plot (Start from 0)"))
    masks(imgquantized,color_index)