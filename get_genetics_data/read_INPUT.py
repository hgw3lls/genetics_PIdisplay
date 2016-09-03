import csv
import urllib
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import textwrap
import re

urllib.urlretrieve("http://genetics.case.edu/VidDISPLAY/INPUT", "INPUT")

allinfo=[]


with open('INPUT','r') as f:
    # skip headings
    # next(f) 
    reader=csv.reader(f,delimiter='\t')
    for info in reader:
        allinfo.append(info)

talktype_font = ImageFont.truetype("../fonts/TitilliumMaps26L.otf",175)
speaker_font = ImageFont.truetype("../fonts/TitilliumMaps26L001.otf",150)
title_font = ImageFont.truetype("../fonts/TitilliumMaps26L002.otf",100)
description_font = ImageFont.truetype("../fonts/TitilliumTitle12.otf",100)
description_font = ImageFont.truetype("../fonts/TitilliumTitle12.otf",100)
day_time_font = ImageFont.truetype("../fonts/Titalic750wt.otf",100)
loc_font = ImageFont.truetype("../fonts/TitilliumMaps26L003.otf",100)
check_event=[]
news = []
count = 0
margin = 45
offset= 665
for event in allinfo:
	Type = event[0]
	Number = event[1]
	Background_Img = event[2]

	img=Image.open(Background_Img)
	draw = ImageDraw.Draw(img)

	if Type == "REG": #3-11
		Number = event[5]
		Dayoftheweek = event[6]
		TalkType = event[7]
		if '-' in TalkType:
			Compound_Info = re.split(r'-', TalkType)
			TalkType = Compound_Info[0].strip()
			Speaker = Compound_Info[1].strip()
		else:
			Speaker = event[8]
		Title = event[9]
		Time =  event[10]
		Location = event[11]
		Day_Time = Dayoftheweek + ', ' + Time
		
		draw.text((1000, 200),TalkType,(0,0,0),font=talktype_font)
		draw = ImageDraw.Draw(img)
		draw.text((1000, 490),Speaker,(0,0,0),font=speaker_font)
		draw = ImageDraw.Draw(img)
		for line in textwrap.wrap(Title, width=45):
    			draw.text((1000, offset), line, (0,0,0), font=title_font)
    			offset += title_font.getsize(line)[1]
    			
		#draw.text((1000, 550),Title,(0,0,0),font=title_font)
		draw = ImageDraw.Draw(img)
		draw.text((1000, 1250),Day_Time,(0,0,0),font=day_time_font)
		draw = ImageDraw.Draw(img)
		draw = ImageDraw.Draw(img)
		draw.text((1000, 1350),Location,(0,0,0),font=loc_font)
		draw = ImageDraw.Draw(img)
		image_name = "slide" + str(count) +".png"
		img.save(image_name)
		count = count+1
	elif Type == "NEWS": #3-6
		news = event[6]
		print news
		print len(news)
	elif Type == "SPEC":
		image_name = "slide" + str(count) +".png"
		img.save(image_name)
		count = count+1
	else: 
		print "Bad Type: I don't have this type in my logic."
	
	
	






