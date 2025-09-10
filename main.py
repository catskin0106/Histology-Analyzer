from analyzer import *
import os

##==Config (Main)==##
ImagePath = 'D:\Coding\multiplexthingy\Histology-Analyzer\Images\image.png'
Task = 'Mask'

##==Config (Quantize)==##
ColorAmount = 10
QuantizeAlgorithm = 2 ##0(Median Cut) / 1(Maximum Coverage) / 2(Fast Octree)
QuantizeToPalette = False ##If True, Manually set the colors of the stain

##==Config (Mask)==##
SaveMaskImage = False

##==========##

output, imgquantized = analyze_image_colors(ImagePath,ColorAmount,QuantizeAlgorithm)
print(output)
if Task == 'Colorplot':
    colorplot(output)
if Task == 'Mask':
    colorplot(output)
    color_index=int(input("Type in the index of the color to be masked: (From left to right in the plot & Start from 0)"))
    masks(imgquantized,color_index)