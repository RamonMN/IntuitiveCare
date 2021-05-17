"""
Created on Thu May 13 18:12:47 2021

@author: Ramon Machado Ribeiro de Assumpcao Nunes

This code will implement the first task of the Intuitive Care developer's
position application.
"""

from bs4 import BeautifulSoup
import requests


def download_pdf(url, filename):
	"""This function will search and download the pdf of the latest TISS 
	standard's organizational component.

	Args:
		url (str): the link of the TISS standard's main page.
		filename (str): the pdf's download name, without the ".pdf"

	"""

	first_target = "Clique aqui para acessar a versão"
	second_target = "Componente Organizacional"

	# Loads the first page and finds the desired element.
	first_page = requests.get(url)
	first_page.raise_for_status()
	soup_1 = BeautifulSoup(first_page.text, "html.parser")
	div = soup_1.find("div", class_="item-page")

	for element in div.find_all("a", class_="alert-link"):
		if first_target in element.get_text():
			first_link = element.get("href")
	
	# Loads the second page and looks for the pdf's link.
	second_page = requests.get(url[0:21]+first_link)
	second_page.raise_for_status()
	soup_2 = BeautifulSoup(second_page.text, "html.parser")
	div = soup_2.find("div", class_="table-responsive")

	for row in div.find_all("tr"):
		columns = row.find_all("td")
		if len(columns) > 1:
			if second_target in columns[0]:
				second_link = columns[2].find("a").get("href")
				break

	# Loads the pdf page and copy the binaries to a local file.
	pdf_page = requests.get(url[0:21]+second_link)
	pdf_page.raise_for_status()

	with open(filename+".pdf", "wb") as file:
		for chunk in pdf_page.iter_content(100000):
			file.write(chunk)


if __name__ == "__main__":
	url = "http://www.ans.gov.br/prestadores/tiss-troca-de-informacao-de-saude-suplementar"
	download_pdf(url, "teste")