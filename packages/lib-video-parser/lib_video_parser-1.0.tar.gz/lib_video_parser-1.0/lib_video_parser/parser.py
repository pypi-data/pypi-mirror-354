import requests, aiohttp, random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import choice

URL_HOME = f"https://tegos.club/erotic/video_eks/02_home/"
URL_STUDENT = f"https://tegos.club/erotic/video_eks/04_students/"
URL_MW = f"https://tegos.club/erotic/video_eks/08_mw/"
URL_GRUP = f"https://tegos.club/erotic/video_eks/06_grup/"
URL_MILF = f"https://tegos.club/erotic/video_eks/03_milf/"
URL_MULAT = f"https://tegos.club/erotic/video_eks/05_mulatka/"
URL_LESBI = f"https://tegos.club/erotic/video_eks/09_lesbi/"
URL_FULL_FILMS = f"https://tegos.club/erotic/video_eks/01_full_films/"

URL_CATEGORIES = [URL_HOME, URL_STUDENT, URL_MW, URL_GRUP, URL_MILF, URL_MULAT, URL_LESBI, URL_FULL_FILMS]

POSTFIX_PAGE = "?page="
MAX_PAGES = 9999

class VideoItem():
	def __init__(self, href:str, label_date:str) -> None:
		self.href = href
		self.label_date = label_date
		self.gif = None
		self.image = None
		self.download_link = self._build_download_link(href)
		self._cache_count_pages = 0
	
	def _build_download_link(self, href:str) -> str:
		return f"{href}&action=getvideo"
	
	def __str__(self) -> str:
		return f"href: {self.href}\nlabel_date: {self.label_date}\ngif: {self.gif}\nimage: {self.image}\n"

class Parser():
	def __init__(self, url:str) -> None:	
		self._user_agent = UserAgent().random
		self._headers = {'User-Agent':self._user_agent}	
		self._cookies = {}
		self.URL_SRC = url
		self.COUNT_FILES_IN_ONCE_PAGE = 11

	def _build_url_page(self, number_page:int) -> str:
		return f"{self.URL_SRC}{POSTFIX_PAGE}{number_page}/"
	
	def _get_soup(self, url:str) -> BeautifulSoup:
		response = requests.get(url, headers=self._headers, cookies=self._cookies)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def _is_found_video_in_page(self, text_html:str) -> bool:
		return "Больше →" in text_html

	def _binarie_search(self, start_page:int, stop_page:int, old_middle_point:int=0) -> int:
		middle_point = int((start_page + stop_page) / 2)
		if middle_point == old_middle_point: return middle_point
		temp_url = self._build_url_page(middle_point)
		text_html = self._get_soup(temp_url).text
		if self._is_found_video_in_page(text_html): return self._binarie_search(middle_point, stop_page, middle_point)
		else: return self._binarie_search(start_page, middle_point, middle_point)

	# binaries search (split range)
	def get_count_pages(self) -> int:
		count_pages = self._binarie_search(1, MAX_PAGES)
		self._cache_count_pages = count_pages
		return count_pages

	def get_count_all_files(self) -> int:
		if self._cache_count_pages == 0: self.get_count_pages()
		return self._cache_count_pages * self.COUNT_FILES_IN_ONCE_PAGE

	def get_files_page(self, number_page:int) -> list[VideoItem]:
		video_items = [] 
		temp_url = self._build_url_page(number_page)
		soup = self._get_soup(temp_url)

		box = soup.find('div', class_="box")
		for link in box.find_all("a"):
			try:
				href = f"{self.URL_SRC}{link.get('href')}"
				label_date = link.find("div").find("div").find("div").find("div").text
				video_items.append(VideoItem(href, label_date))
			except :
				pass
				
		c = 0
		box = soup.find('div', class_="box")
		for style_elem in box.find_all("style"):
			try:
				gif = style_elem.text.split("url(")[-1].split(");}")[0]
				image = style_elem.text.split("url(")[-2].split(");}")[0]
				video_items[c].gif = gif
				video_items[c].image = image
				c += 1
			except :
				pass

		return video_items

	def get_random_page_all_categories(self) -> list[VideoItem]:
		category = choice(URL_CATEGORIES)
		return self.get_random_page_on_category(category)


	def get_random_page_on_category(self, category_url:str) -> list[VideoItem]:
		self.URL_SRC = category_url
		number_page = random.randint(1, self.get_count_pages())
		return self.get_files_page(number_page)


	# def get_files_iterator(self, start_page=1, stop_page:int=2):
	# 	pass

	# async def get_random_file(self) -> str:
	# 	pass
		# number_page = random.randint(1, self.get_count_pages()-1)
		# url = self._build_url_page(number_page)
		# async with aiohttp.ClientSession() as session:
		# 	async with session.get(url, headers=self._headers) as response:
		# 		html = await response.text()
		# 		response = requests.get(url, headers=self._headers)
		# 		soup = BeautifulSoup(response.text, 'html.parser')
		# 		for link in soup.find_all('a'):
		# 			href = link.get('href')
		# 			if href and href.startswith('http'):
		# 				if href.find('/view') != -1:
		# 					soup = self._get_soup(href)
		# 					for link in soup.find_all('a'):
		# 						href = link.get('href')
		# 						if href and href.startswith('http'):
		# 							if href.find("download") != -1:
		# 								return href.replace("jpg","png")

