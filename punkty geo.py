
import re
from urllib.request import urlopen

def czy_dobre_dane():
	while True:
		dane = input("Podaj nazwę szukanego miasta: ")
		dane = dane.replace(" ", "")
		if dane.isalpha() == True:
			return nie_polskie_znaki(dane)
		else:
			print("Podałeś błędne dane")

			
def nie_polskie_znaki(miasto):	
    polskie='ĄąĆćĘęŁłŃńÓóŻżŹź'
    nie_polskie='AaCcEeLlNnOoZzZz'
    zamiana=str.maketrans(polskie,nie_polskie)
    return wyrazenia_regular(miasto.translate(zamiana))		


def wyrazenia_regular(miasto):
	adres = "https://www.google.com/maps/place/"
	html = urlopen(adres + miasto)
	szukane = str(html.read())
	regularne = re.compile(r'INITIALIZATION\S+')
	mo = regularne.search(szukane)
	wycinek_tekstu = mo.group()
	
	a = b = 0
	tab = []
	for i in wycinek_tekstu:
		a = a+1
		if b <= 2:
			if '.' == i:
				tab.append(wycinek_tekstu[a-3:a+2])
				b = b+1
		else:
			break
	punktN, punktE = (tab[1:3])
	if ['19.20', '52.02'] == tab[1:3] and miasto.lower() == "lubien":	
		print("\nSzerokość geograficzna: %s\nDługość geograficzna: %s" % (punktE, punktN))
	elif ['19.20', '52.02'] != tab[1:3]:
		print("\nSzerokość geograficzna: %s\nDługość geograficzna: %s" % (punktE, punktN))
	else:
		print("takie miejsce nie istnieje!")
		czy_dobre_dane()

czy_dobre_dane()

