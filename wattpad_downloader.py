import bs4
import sys
import requests
import pyperclip
import re
import pypandoc
import string
import pyautogui as pg

address = pg.prompt("Enter the link: ")


search_id = re.compile(r'\d{9,}')
id_no = search_id.search(address)



res = requests.get("https://www.wattpad.com/apiv2/info?id="+id_no.group(), headers={'User-Agent':'Mozilla/5.0'})

try :
    res.raise_for_status()
except Exception as exc:
    pg.alert("There was a problem: %s" %(exc))



summary = res.json()["description"]
tags = res.json()["tags"]
chapters = res.json()['group']
name = res.json()['url']
author = res.json()['author']


search_name = re.compile(r"[\w]+['][\w]+|\w+")
name= requests.utils.unquote(name)
name = search_name.findall(name)
story_name = string.capwords(' '.join(name[2:]))


file = open(story_name+".html", 'w', encoding='utf-8')
file.write("<html><head></head><body>")

file.write("<br><h1>" + story_name +"</h1><br>BY  <h4>"+author+"</h4><br><b>Tags:</b> "+tags+"<br><br>"+summary+"<br>")
file.write("<br><br><div align='left'><h6>* If chapter number or names are Jumbled up, its definetely author's fault.(Author-san please Number them correctly and in order.)<br>* Converted using Wattpad2epub By Architrixs<br></h6></div>")


for i in range(len(chapters)):

	print("Getting Chapter", i+1, "....")
	story = requests.get("https://www.wattpad.com/apiv2/storytext?id=" + str(chapters[i]['ID']), headers={'User-Agent': 'Mozilla/5.0'})

	try:
		story.raise_for_status()
	except Exception as exc:
		pg.alert("There was a problem: %s" % (exc))
	
	
	soup_res = bs4.BeautifulSoup(story.text, 'html.parser')
	

	file.write("<br><br><h2>Chapter "+str(i+1)+" : '"+ chapters[i]['TITLE'] +"'</h2><br><br>")
	file.write(str(soup_res.prettify().encode('cp1252', errors='ignore')))

file.write("</body></html>")


file.close()



pg.alert("saved "+ story_name+".html")
pg.alert("Generating Epub...")


output = pypandoc.convert_file(story_name+".html", 'epub3', outputfile=story_name+".epub", extra_args=['--epub-chapter-level=2'])
assert output == ""
print("saved "+ story_name+".epub")
