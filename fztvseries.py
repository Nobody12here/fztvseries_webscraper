from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

main = "https://fztvseries.mobi/"
url = "https://fztvseries.mobi/subfolder-Rick%20and%20Morty.htm"

EpisodesLinks=[]

def CrawlPages(BaseUrl):
	page = requests.get(BaseUrl)
	soup = BeautifulSoup(page.content,"html.parser")
	season = soup.select(".mainbox3 > a")
	for link in season:
		GetEpisodes(main + link["href"])

def GetEpisodes(url):
	print("Getting Episodes Links ........")
	page = requests.get(url)
	soup = BeautifulSoup(page.content,"html.parser")
	Episode = soup.select(".mainbox > table > tr > td")
	for link in Episode:
		EpisodesLinks.append( main + link.a["href"])
	
	
def GetVideo(ListOfUrl):
	"""
	Gets the src attribute of the video tag using selenium from the list of episode urls.
	"""
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_options=options)
	for link in ListOfUrl:
		print("Finding the video links........")
		driver.get(link)
		Temp = driver.find_element("id","slink1")
		link = Temp.get_attribute("href")
		#Create a new tab and then switch to that
		driver.execute_script("window.open('');")
		windows = driver.window_handles
		driver.switch_to.window(windows[1])
		driver.get(link)
		video = driver.find_element("css selector","#vid1_html5_api > source")
		print(video.get_attribute("src"))
		#Close the second tab and then switch to the main tab
		driver.close()
		driver.switch_to.window(windows[0])

	driver.close()



# GetEpisodes(url)
CrawlPages(url)
print(EpisodesLinks)
GetVideo(EpisodesLinks)



