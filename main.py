#from typing import Optional
#from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
from datetime import date
import json

# if we print comments about what's happening
logging = True
verbose_logging = False

# constructing Elron's todays schedule
today = str(date.today())

routes = [
	{
		'url': 'https://elron.pilet.ee/et/otsing/Tallinn/Laagri/'+today,
		'direction': 'home'
	},{
		'url': 'https://elron.pilet.ee/et/otsing/Laagri/Tallinn/'+today,
		'direction': 'work'
	}
]

# chromium options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")













if logging:
	print ("\n\n#######################\nStarting Elron scraper...\n")
	print ("Today's URLs: ")
	print ("  "+routes[0]['direction']+": "+routes[0]['url'])
	print ("  "+routes[1]['direction']+": "+routes[1]['url'])
	print (" ")

trips = {"home": [], "work": []}

for route in routes:
	driver = webdriver.Chrome(options=options)  
	driver.get(route['url'])
	  
	# this is just to ensure that the page is loaded 
	time.sleep(10)  
	 
	html = driver.page_source 
	soup = BeautifulSoup(html, 'html.parser')
	
	if logging:
		if len(soup)>0:
			print("Successfully fetching URL "+route['url'])
	
	tripscontainer = soup.find('app-journeys-results-list-container')
	
	
	if len(tripscontainer)>0:
	
		if logging:
				print("Successfully found tag <app-journeys-results-list-container>")
				
		tripscode = soup.find_all('div', class_='trip-summary')
		tripno = 1
		
		
		for tripcode in tripscode:
			# Find the title (h2 tag) and description (p tag)
			
			if verbose_logging:
				print("Trip #"+str(tripno)+" found!")
				
			trip_time = tripcode.find('div', class_='trip-summary__timespan').text
			trip_details = tripcode.find('div', class_='trip-summary__line').text
			
			trip = {
				'time_start': trip_time[:5],
				'time_end': trip_time[5:],
				'train': trip_details[:3],
				'route': trip_details[4:]
			}
			
			trips[route['direction']].append(trip)

			
			if verbose_logging:
				print("  time: "+trip['time_start']+" - "+trip['time_end'])
				print("  train: "+trip['train'])
				print("  route: "+trip['route'])
			
			tripno += 1
			if verbose_logging:
				print(" ")
			
	
	if logging:
		print("Total trips found for route "+route['direction']+": "+str(len(trips[route['direction']])))
		print(" ")
		print("######")

#console.log(trips)	
	
	
