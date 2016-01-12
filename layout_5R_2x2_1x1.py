#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2015, Edwin T. Tumbaga
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#    - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation and/or 
#    other materials provided with the distribution.
#    - Neither the name of the author nor the names of its contributors may be used 
#    to endorse or promote products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.

import os
import sys
import copy
from gimpfu import *
from datetime import datetime

def layout(img, layer, outputFolder):
    ''' Make 2x2 and 1x1 copies of a square ID picture.
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
    outputFolder : string The folder in which save the modified images.
    '''
    
    # Generate filename
    prefix = "doublespace_image"
    extension = ".jpg"
    filedate = datetime.now().strftime("%Y%m%d_%H%M%S")
    file = prefix + "_" + filedate + extension
    
    # Get original image height and width
    img_height = pdb.gimp_image_height(img)
    img_width = pdb.gimp_image_width(img)
    
    # If image is not up to spec, return an error message.
    # Image must be a perfect square
    # Image should be at least 600x600 pixels (for a 2x2 picture)
    if img_height != img_width:
        gimp.message("Image is not a perfect square!")
        return
    elif img_height < 600:
        gimp.message("Minimum size should be 600 X 600 pixels (or 2 inches)")
        return

    #Some variables used throughout
    RGB = 0
    canvass_width = 1500
    canvass_height = 2100
    copy_width_1x1 = 300
    copy_height_1x1 = 300
    copy_width_2x2 = 600
    copy_height_2x2 = 600
    current_position_x = 100
    current_position_y = 100

    try:
        # Create output path and filename
        outputPath = outputFolder + "\\" + file
        
        # Make copies of the original image.
        # This is so that the original image remains unmodified all throughout the processing
        img2x2 = copy_orig_picture(img,layer)
        img1x1 = copy_orig_picture(img,layer)
        
        # PROCESS image sizes
        img2x2 = resize_picture(img2x2,copy_width_2x2, copy_height_2x2)
        img1x1 = resize_picture(img1x1,copy_width_1x1, copy_height_1x1)
        
        # Make the picture canvass. This is where we will do all the dirty work.
        canvass = None
        canvass = pdb.gimp_image_new(canvass_width,canvass_height,RGB)
        
        #Create duplicates of the processed (resized) images
        layer = duplicate_picture(img2x2,canvass,current_position_x, current_position_y,copy_width_2x2,copy_height_2x2,"2x2 1st copy")    

        current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + 75
        
        layer = duplicate_picture(img2x2,canvass,current_position_x, current_position_y,copy_width_2x2,copy_height_2x2,"2x2 2nd copy")
        
        current_position_x = 100
        
        current_position_y = current_position_y + pdb.gimp_drawable_height(layer) + 50

        layer = duplicate_picture(img2x2,canvass,current_position_x, current_position_y,copy_width_2x2,copy_height_2x2,"2x2 3rd copy")
 
        current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + 75
        
        layer = duplicate_picture(img2x2,canvass,current_position_x, current_position_y,copy_width_2x2,copy_height_2x2,"2x2 4th copy")
        
        current_position_x = 100
        
        current_position_y = current_position_y + pdb.gimp_drawable_height(layer) + 50
        
        
        layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 1st copy")

        current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + 25

        layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 2nd copy")

        current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + 25
        
        layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 3rd copy")
        
        current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + 25
        
        layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 4th copy")
        #layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 3rd copy")
        #current_position_y = current_position_y + pdb.gimp_drawable_height(layer) + 100
        #
        #layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 4th copy")
        #current_position_y = current_position_y + pdb.gimp_drawable_height(layer) + 100
        #
        #layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 5th copy")
        #current_position_y = current_position_y + pdb.gimp_drawable_height(layer) + 100
        #
        #layer = duplicate_picture(img1x1,canvass,current_position_x, current_position_y,copy_width_1x1,copy_height_1x1,"1x1 6th copy")
        
        pdb.gimp_image_flatten(canvass)
        pdb.gimp_image_set_resolution(canvass, 600, 600)
        
        
        if(file.lower().endswith(('.png'))):
            pdb.file_png_save(canvass, canvass.layers[0], outputPath, outputPath, 0, 9, 0, 0, 0, 0, 0)
            
        if(file.lower().endswith(('.jpeg', '.jpg'))):
            pdb.file_jpeg_save(canvass, canvass.layers[0], outputPath, outputPath, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)
        
        #Display resulting image
        display = pdb.gimp_display_new(canvass)


        #gimp.message("Success!")
    except Exception as err:
        gimp.message("Unexpected error: " + str(err))

# Function to copy the original image
def copy_orig_picture(image, layer):
    img_width = pdb.gimp_image_width(image)
    img_height = pdb.gimp_image_height(image)
    image_copy = pdb.gimp_image_new(img_width,img_height, 0)
    layer_copy = pdb.gimp_layer_new(image_copy,img_width,img_height,0,"default",100,0)
    
    pdb.gimp_image_add_layer(image_copy,layer_copy, -1)
    pdb.gimp_edit_copy(layer)
    selection = pdb.gimp_edit_paste(layer_copy,-1)
    pdb.gimp_floating_sel_anchor(selection)
    
    #display = pdb.gimp_display_new(image_copy)
    
    return image_copy
    
# Function to resize the original image to the appropriate width / height (2x2 or 1x1)    
def resize_picture(orig_image, new_width, new_height):
    resized = pdb.gimp_image_scale(orig_image, new_width, new_height)
    return orig_image

# Function to make additional copies of the resized images    
def duplicate_picture(orig_image, canvass_image, xpos, ypos,img_width, img_height, name):
    layer = pdb.gimp_layer_new(canvass_image,img_width,img_height,0,name,100,0)
    pdb.gimp_image_add_layer(canvass_image,layer,-1)
    pdb.gimp_selection_all(orig_image)
    pdb.gimp_edit_copy(orig_image.layers[0])
    selection = pdb.gimp_edit_paste(layer,-1)
    pdb.gimp_floating_sel_anchor(selection)
    pdb.gimp_layer_set_offsets(layer,xpos,ypos)
    return layer
    
from os.path import expanduser
folder = expanduser("~") + "\\Desktop\\doublespace"
if not os.path.exists(folder):
    os.makedirs(folder)

register(
    "python_fu_layout_5R",
    "Four 2x2's Four 1x1's",
    "Make 2x2 and 1x1 copies of a square ID picture",
    "ETT",
    "Open source (BSD 3-clause license)",
    "2015",
    "<Image>/Filters/DoubleSpace/ID Four 2x2's Four 1x1's on 5R",
    "*",
    [
        #(PF_DIRNAME, "inputFolder", "Input directory", ""),
        (PF_DIRNAME, "outputFolder", "Output directory", folder),
        #(PF_SLIDER, "maskRadius", "Mask radius", 7, (1,50,1)),
        #(PF_SLIDER, "blackPct", "Percentage of dark" , 0.2, (0.0,1.0,0.01))
    ],
    [],
    layout)

main()
