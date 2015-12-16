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

def layout(img, layer, paper_size, inputFolder, outputFolder):
    ''' Make multiple page layouts  of different pictures loaded from a directory.
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
    outputFolder : string The folder in which save the modified images.
    '''
    
    #gimp.message("Picture Size: " + str(picture_size))
    #gimp.message("Paper Size: " + str(paper_size))
    paper = {0:'4R',1:'5R',2:'A4'}
    picture = {0:'1 x 1',1:'1.5 x 1.5',2:'2 x 2',3:'PH Passport',4:'2R'}
    
    paper_size = paper[paper_size]
    #picture_size = picture[picture_size]

    #gimp.message("Picture Size: " + str(picture_size))
    #gimp.message("Paper Size: " + str(paper_size))
    
    # Generate filename
    file_counter = 0

    
    
    
   
    paper_sizes = {'4R':{'width':1200,'height':1800},'5R':{'width':1500,'height':2100},'A4':{'width':2481,'height':3507}}
    picture_sizes = {'1 x 1':{'width':300,'height':300}, '1.5 x 1.5':{'width':450,'height':450}, '2 x 2':{'width':600,'height':600},'PH Passport':{'width':411,'height':531},'2R':{'width':1050,'height':750}}
    
    
    #img_resolution_x = picture_sizes[picture_size]['width']
    #img_resolution_y = picture_sizes[picture_size]['height']
    img_resolution_x = 600
    img_resolution_y = 600
    
    # If image is not up to spec, return an error message.
    # Image must be a perfect square
    # Image should be at least 600x600 pixels (for a 2x2 picture)
    #if img_height != img_width:
    #    passport_ratio =  round(531/411.0,2)
    #    ratio = img_height * 1.0 / img_width
    #    ratio = round(ratio, 2)
    #    
    #    if ratio == passport_ratio:
    #    
    #        gimp.message("Image is a PH passport!")
    #    else:
    #        gimp.message("Image size is not processable!")
    #        return
    #elif img_height < img_resolution_y:
    #    gimp.message("Minimum size should be" + str(img_resolution_x) + " X " + str(img_resolution_y) + " pixels")
    #    return
        
    
    
    #Some variables used throughout
    RGB = 0
    canvass_width = paper_sizes[paper_size]['width']
    canvass_height = paper_sizes[paper_size]['height']
    copy_width = 1050
    copy_height = 750
    copy_interval = 50
    current_position_x = copy_interval + 50
    current_position_y = copy_interval + 50
    
    files = sorted(os.listdir(inputFolder))
    file_count = len(files)
    last_file = False
    canvass_full = True
    for file in files :
        gimp.message("File: "+str(file))
        if files.index(file) + 1 == file_count:
            last_file = True
            
        try:
            # Build the full file paths.
            inputPath = inputFolder + "\\" + file
            outputPath = outputFolder + "\\" + file
                        
            # Open the file if is a JPEG or PNG image.
            image = None
            if(file.lower().endswith(('.png'))):
                image = pdb.file_png_load(inputPath, inputPath)
            if(file.lower().endswith(('.jpeg', '.jpg'))):
                image = pdb.file_jpeg_load(inputPath, inputPath)
                
                
            # Verify if the file is an image.
            if(image != None):
                # Invert the image.
                if(len(image.layers) > 0):
                    #layer = image.layers[0]
                    #pdb.plug_in_cartoon(image, layer, maskRadius, blackPct)
                    
                    
                    layer = image.layers[0]
                    
        
                    # Make copies of the original image.
                    # This is so that the original image remains unmodified all throughout the processing
                    
                    img_copy = image
                    
                    # Get original image height and width
                    img_height = pdb.gimp_image_height(image)
                    img_width = pdb.gimp_image_width(image)
                    img_orientation = None
                    
                    
                    # If image is not up to spec, return an error message.
                    # Image must be a perfect square
                    # Image should be at least 600x600 pixels (for a 2x2 picture)
                    if img_height > img_width:
                        img_orientation = 'portrait'        
                        gimp.message("Image is Portrait")
                        #return
                    
                    if img_height < img_width:
                        img_orientation = 'landscape'
                        gimp.message("Image is Landscape")
                        #return
                        
                    if img_orientation == 'portrait':
                        pdb.gimp_image_rotate(img_copy, 0)
                        img_height = pdb.gimp_image_height(img_copy)
                        img_width = pdb.gimp_image_width(img_copy)
                        #gimp.message("Image Width:"+str(img_width))
                        #gimp.message("Image Height:"+str(img_height))
                    # PROCESS image sizes
                    img_copy = resize_picture(img_copy,copy_width, copy_height)
                    
                    # Make the picture canvass. This is where we will do all the dirty work.
                    
                    # If canvass is full, create a new canvass
                    if canvass_full:
                        #gimp.message("Reached maximum number of drawings!")
                        canvass = None
                        canvass = pdb.gimp_image_new(canvass_width,canvass_height,RGB)
                        canvass_full = False
                        #display = pdb.gimp_display_new(canvass)
                        gimp.message("File counter:" + str(file_counter))
                    
                    #Create duplicates of the processed (resized) images
                    
                    gimp.message("Duplicate picture")
                    layer = duplicate_picture(img_copy,canvass,current_position_x, current_position_y,copy_width,copy_height,"duplicate")
                    current_position_x = current_position_x + pdb.gimp_drawable_width(layer) + copy_interval

                    gimp.message("Set next position")
                    if current_position_x > canvass_width - (copy_width + copy_interval):
                        current_position_x = copy_interval + 50
                        current_position_y = current_position_y + copy_height + copy_interval
                    
                        if (current_position_y > canvass_height - (copy_height + copy_interval)) or last_file:
                            gimp.message("Reached maximum number of drawings!")
                            canvass_full = True
                            
                            current_position_x = copy_interval + 50
                            current_position_y = copy_interval + 50
                            		        
                            gimp.message("Flatten canvass")
                            pdb.gimp_image_flatten(canvass)
                            
                            gimp.message("Set image resolution")
                            pdb.gimp_image_set_resolution(canvass, img_resolution_x, img_resolution_y)
                    
                            # Save the image.
                            file_counter = file_counter + 1
                            prefix = "doublespace_image" + "_" + str(file_counter)
                            extension = ".jpg"
                            filedate = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = prefix + "_" + filedate + extension
                            outputPath = outputFolder + "\\" + filename
    
                            #if(file.lower().endswith(('.png'))):
                            #    pdb.file_png_save(canvass, canvass.layers[0], outputPath, outputPath, 0, 9, 0, 0, 0, 0, 0)
                                
                            #if(file.lower().endswith(('.jpeg', '.jpg'))):
                            gimp.message("Save file")
                            pdb.file_jpeg_save(canvass, canvass.layers[0], outputPath, outputPath, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)
                            #del canvass
                            #Display resulting image
                            #display = pdb.gimp_display_new(canvass)
                            pdb.gimp_image_delete(canvass)
                            gimp.message("Deleted canvass image!")
                    
                    #del img_copy
                #del image
                pdb.gimp_image_delete(image)
                gimp.message("Deleted image copy")
                    
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
    gimp.message("Set background to white")
    pdb.gimp_context_set_background((255,255,255))
    
    gimp.message("Add new layer")
    layer = pdb.gimp_layer_new(canvass_image,img_width,img_height,0,name,100,0)
    pdb.gimp_image_add_layer(canvass_image,layer,-1)
    pdb.gimp_selection_all(orig_image)
    pdb.gimp_edit_copy(orig_image.layers[0])
    gimp.message("Paste image")
    selection = pdb.gimp_edit_paste(layer,-1)
    pdb.gimp_floating_sel_anchor(selection)
    gimp.message("Set image position")
    pdb.gimp_layer_set_offsets(layer,xpos,ypos)
    return layer
    
from os.path import expanduser
folder = expanduser("~") + "\\Desktop\\doublespace"
if not os.path.exists(folder):
    os.makedirs(folder)

register(
    "python_fu_multi_picture",
    "Multi picture 2R",
    "Make multiple 2R layouts of different pictures from a source directory",
    "ETT",
    "Open source (BSD 3-clause license)",
    "2015",
    "<Image>/Filters/DoubleSpace/Multiple Sources 2R Output haay",
    "*",
    [
        #(PF_OPTION, "picture_size"  ,("Picture Size: "), 0 ,["1 x 1", "1.5 x 1.5", "2 x 2", "PH Passport"]),
        (PF_OPTION, "paper_size"  ,("Paper Size: "), 0 ,["4R", "5R", "A4"]),        
        #(PF_OPTION, "file_type"  ,("File type: "), 0 ,[".jpg", ".png", ".tif", ".pcx", ".xcf", ("all registered formats")]),
        (PF_DIRNAME, "inputFolder", "Input directory", folder),
        (PF_DIRNAME, "outputFolder", "Output directory", folder),
        #(PF_SLIDER, "maskRadius", "Mask radius", 7, (1,50,1)),
        #(PF_SLIDER, "blackPct", "Percentage of dark" , 0.2, (0.0,1.0,0.01))
    ],
    [],
    layout)

main()
