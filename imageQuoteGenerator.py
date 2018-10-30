# -*- coding: utf-8 -*-

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import os.path
import textwrap
import io
####DEFINITIONS##############################################################
TEMPLATE_IMAGE_TOP   = 'top.png'
TEMPLATE_IMAGE_BOTTOM= 'bottom.png'
TEMPLATE_IMAGE_MIDDLE= 'middle.png'
QUOTES_FILE          = 'quotes.txt'
OUT_FORMAT           = 'out\quote-'

FONT_FONT_NAME       = 'XXXXXXXXX.ttf'
FONT_MAX_SIZE=280 

IMAGE_WIDTH =952
IMAGE_HEIGHT=411

AREA_TOP_MARGIN = 5
AREA_LEFT_MARGIN = 60 #25
AREA_WIDTH  =IMAGE_WIDTH - AREA_LEFT_MARGIN +10
AREA_HEIGHT =IMAGE_HEIGHT - 11

COLOR_RGB=(204,51,51)
LINE_SPACING = 10
#################################################################################
def get_font(name, size):
    fonts_path = os.path.join(os.path.dirname(__file__), 'fonts')
    myfont = ImageFont.truetype(os.path.join(fonts_path, name), size,0)
    return myfont #ImageFont.truetype(font, size)

def myFit(width,height, font, size, text):
    font = get_font(font, size)
    text_w, text_h = font.getsize("2")
    charsInline =  width/text_w 
    margin = offset = charsInline
    newtext='';
    max_width=0;
    for line in text.splitlines():
       if line.strip()!='':  
         for the_line in textwrap.wrap(line, width=charsInline):
            newtext = newtext + the_line+'\n'
            offset += font.getsize(the_line)[1]
            if (max_width<font.getsize(the_line)[0]):
                max_width=font.getsize(the_line)[0]
       else: 
            newtext=newtext+'\n'
            offset += font.getsize(line)[1]
       #print line
       nlines = newtext.count('\n')
       #print 'new text number of line' + str(nlines)
    #print str(height-offset) + " " +  str(height/4) 
    if ((height-offset)> 0): 
           top_margin=(height-offset)/2 
    else:
           top_margin=AREA_TOP_MARGIN   
    if ((width - max_width)>0):
            left_margin = (width - max_width)/ 2
    else:
            left_margin = AREA_LEFT_MARGIN
    return offset<=height and max_width<=width,newtext,top_margin, left_margin
    
    
def verticalConcatImages(my_path,out_file_name):
    images = map(Image.open, [my_path +TEMPLATE_IMAGE_TOP,my_path +out_file_name, my_path +TEMPLATE_IMAGE_BOTTOM])
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)
    new_im = Image.new('RGB', (max_width, total_height))
    x_offset = 0
    for im in images:
      new_im.paste(im, (0,x_offset))
      x_offset += im.size[1]
    rgb_im = new_im.convert('RGB') #remove transparancy
    rgb_im.save(my_path +out_file_name)
def drawTextOnImage(my_path,out_file_name,draw_on_file,font_name, font_size, top_margin,left_margin):#"quotemiddles.png"
    img = Image.open(my_path + draw_on_file)
    draw = ImageDraw.Draw(img)
    mfont = get_font(font_name, font_size) 
    draw.text((left_margin,top_margin), text, font=mfont, fill=COLOR_RGB,spacing=LINE_SPACING)
    rgb_im = img.convert('RGB') #remove transparancy
    rgb_im.save(my_path +out_file_name)
def claculateNewTextAndSize(text,font,initialSize):
    size = initialSize
    while True:
     ans,newtext,top_margin, left_margin = myFit(AREA_WIDTH, AREA_HEIGHT, font, size, text) 
     if ans == True: 
        break
     else:
         size = size-1
    return newtext, size , top_margin, left_margin
#############################main###########################################
size = FONT_MAX_SIZE
font = FONT_FONT_NAME
my_path = os.path.dirname(__file__)+'/'
print '################Generating Quote Images##########################\n'
for filelineno, line in enumerate(io.open(my_path + QUOTES_FILE,mode="r",encoding="utf-8")): 
  line = line.strip().replace('\\n','\n')
  print str(filelineno+1) + ' ' + line 
  text,size, top_margin, left_margin = claculateNewTextAndSize(line,font,size)
  size=size+2 #correction
  print("Font_Size: {}".format(size)+ " Top Margin: {}".format(top_margin)+ " Left Margin: {}".format(left_margin)+'\n')
  drawTextOnImage(my_path,OUT_FORMAT+str(filelineno+1)+'.jpg',TEMPLATE_IMAGE_MIDDLE,font, size, top_margin,left_margin)
  verticalConcatImages(my_path,OUT_FORMAT+str(filelineno+1)+'.jpg')
print '################Finished##########################################\n'
