"""
Created on Sat May 15 14:12:47 2021

@author: Ramon Machado Ribeiro de Assumpcao Nunes

This code will implement the second task of the Intuitive Care developer's
position application.
"""

import pdfplumber
import re
import csv
import os
import shutil

def get_tables(file, table_names):
	"""This function will search the pdf for the desired tables and will save
	each table on a csv file, and last it will compile the files on a zip file.
		
	Args:
		file (str): the pdf file path.
		table_names (list): the list with the number of the table you want.
							It must be sorted. ex.: [30, 31, 32] 

	"""

	# Get the table from the whole pdf text.
	def get_table(text, table_title, table_end):
		index_1 = text.find(table_title)
		text = text[index_1:]
		index_2 = text.find(table_end)

		return text[:index_2], text[index_2:]

	# Open the pdf and compile the text of each page into one string.
	with pdfplumber.open(file) as pdf_file:
		whole_text = ""
		for page in pdf_file.pages:
			try:
				whole_text += page.extract_text()
			except TypeError:
				pass

	# Clean the tables and make the files.
	table = ""
	for name in table_names:
		table, whole_text = get_table(whole_text, "Quadro " + str(name), "Fonte")
		
		# Remove the footnotes and page number.
		end_of_page = re.compile(r"\n\d{1,}\s\nPadrão TISS - Componente Organizacional – março de 2021                \n ")
		table = end_of_page.sub("", table)
		table = table.split("\n")

		# Remove the table's head.
		wrong_line = re.compile("^\d")
		for index, element in enumerate(table):
			if wrong_line.search(element) != None:
				break
		table = table[index:]

		# Create the csv and write the table to it.
		cwd = os.getcwd()
		dir = os.path.join(cwd, "tables")
		if not os.path.exists(dir):
			os.mkdir(dir)

		with open(os.path.join(dir, "table" + str(name) + ".csv"), mode="w") as csvfile:
			writer_file = csv.writer(csvfile, delimiter=",")

			index = 0
			removed = 0
			size = len(table)

			while True:
				if wrong_line.search(table[index]) == None:
					table[index] = table[index+1] + " " + table[index] + table[index+2]
					table.remove(table[index+1])
					table.remove(table[index+1])
					removed += 2

				writer_file.writerow(table[index].split("  "))
				index += 1
				if index >= size - removed - 1:
					break

	shutil.make_archive("tables", "zip", dir)



if __name__ == "__main__":
	get_tables("teste.pdf", [30, 31, 32])

