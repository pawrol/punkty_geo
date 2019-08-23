"""
Aplikacja konsolowa wyszukująca przy pomocy wyrażeń regularnych współrzędnych
geograficznych podanego przez użytkownika miejsca.
"""

"""
Najpierw importuje ze standardowej biblioteki Pythona moduły, które będę wykorzystywał w dalszej części programu.
re- moduł potrzebny do przygotowania wyrażenia regularnego
urllib.request - moduł potrzebny do pobrania danych z sieci przy pomocy funkcji urlopen (pobranie tekstu strony internetowej)

"""
import re
from urllib.request import urlopen

"""
Za pomocą słowa kluczowego def tworzę funkcję. Nieskończona pętla (while True:) sprawdza, czy podałem
jakieś dane i czy dane nie posiadają jakiejś cyfry (dane.isalpha()).
Po wpisaniu zmiennej dane, z podanej wartości usuwam wszystkie spacje, poprzez
zastąpienie ich pustą wartością (dane.replace(" ", ""))
Następnie instrukcja warunkowa if - jeśli jest prawdziwa – zwraca za pomocą słowa return dane do następnej funkcji.
Jeśli nie (else) wypisuje komunikat o błędnych danych i pętla jest powtórzona. 

"""
def czy_dobre_dane():
	while True:
		dane = input("Podaj nazwę szukanego miasta: ")
		dane = dane.replace(" ", "")
		if dane.isalpha() == True:
			return nie_polskie_znaki(dane)
		else:
			print("Podałeś błędne dane")

"""
Dane zostały przekazane do następnej funkcji, gdzie przy pomocy dodatkowych zmiennych i metod zastępujemy wszystkie znaki diakrytyczne
(zmienna polskie) znakami „bez ogonków” (zmienna nie_polskie). Zdefiniowałem własną funkcję, ponieważ funkcja unicodedata.normalize() nie brała pod uwagę „Ł” i „ł”
Tworzę dwie zmienne typu string, w pierwszej zapisuje wszystkie znaki diakrytyczne,
w drugiej, w odpowiedniej kolejności, ich odpowiedniki. Kolejność jest ważna, bo za sprawą metody str.maketrans()
tworzymy słownik gdzie klucz to jeden znak diakrytyczny, a wartość to jego odpowiednik. Poniżej przykład na znaku „Ą”.
>>> znak_diakrytyczny = ("Ą")
>>> odpowiednik = ("A")
>>> słownik = str.maketrans(znak_diakrytyczny, odpowiednik)
>>> type(słownik)
<class 'dict'>
>>> print(słownik)
{260: 65}

Widać, że klucz 260 (wartość „Ą” w Unicode) ma przypisaną wartość 65 (wartość „A” w ASCII)
W ostatniej części funkcja zwraca wartość do kolejnej funkcji wyrażenia_regular(). Zwrócona wartość to
nasza dana w której – jeżeli występowały polskie znaki - za pomocą metody translate() został zwrócony string w którym
wszystkie znaki zostały przetłumaczone za pomocą tabeli ASCII.


"""
			
def nie_polskie_znaki(miasto):	
    polskie='ĄąĆćĘęŁłŃńÓóŻżŹź'
    nie_polskie='AaCcEeLlNnOoZzZz'
    zamiana=str.maketrans(polskie,nie_polskie)
    return wyrazenia_regular(miasto.translate(zamiana))		

"""
Punktów geograficznych będę szukał przy pomocy strony internetowej https://www.google.com/maps/.
W zmiennej html zapisuję obiekt zwrócony z powstałego adresu internetowego (string z adresem strony połączony z naszą daną).
Następnie metoda read odczytuje cały HTML strony internetowej i zwraca go w postaci łańcucha znaków.
Przy pomocy wyrażenia regularnego, w zwróconym łańcuchu znaków wyszukuje tekst od ciągu znaków INITIALIZATION
do dowolny znaku, który nie jest spacją, tabulatorem lub znakiem nowego wiersza (S+). Wyszukany tekst (regularne.search(szukane))
i zapisuję w zmiennej wycinek_tekstu (mo.group() bez argumentów zwraca cały wyszukany tekst).

"""
"""
Na początek tworzę zmienne pomocnicze a i b o wartości 0 oraz pustą tablicę. Chcę wyszukać
 znaku „.”, bo po analizie HTML doszedłem do wniosku, że tak najszybciej wyszukam punkty geograficzne.
 Przy pomocy pętli for iteruję wycinek_tekstu za każdym razem inkrementuję zmienną a (liczę w ten sposób liczbę znaków). Jeżeli
 wartość b jest większa równa 2 funkcja warunkowa kończy się, jeżeli nie sprawdzamy, czy iterowana wartość i jest równa „.”. Jeżeli
 tak to do tablicy dodajemy wycinek tekstu a-3:a+2 (a numer indeksu iterowanego znaku, w tablicy zapisujemy 5 takich znaków, 2przed
 wystąpieniem „.” I 2 po wystąpieniu tego znaku. Dodatkowo inkrementujemy zmienną b.

"""
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
"""

Po przerwaniu funkcji warunkowej (else: break) , czyli po nie spełnieniu warunku if b <= 2:
przypisujemy 2 wartości tablicy do 2 zmiennych.
Kolejne warunki sprawdzają, czy podana miejscowość w ogóle istnieje (standardowo przy błędnym wyszukaniu
punkty geograficzne to ['19.20', '52.02']). Jeżeli nie jest to akurat ta miejscowość wypisujemy błąd o braku takiej miejscowości i ponownie uruchamiamy program.

"""
