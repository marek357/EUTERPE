# Opis projektu

Projekt prowadzony na zajęcia z Inżynierii Oprogramowania na Wydziale MIMUW w roku akademickim 2019/2020. 
Założenia, jakie nam przyświecają przy tworzeniu tego projektu to wytworzenie jak najwyższej jakości narzędzi dla konsumenta, pragnącego posłuchać muzyki oryginalnej, jeszcze wcześniej nie słyszanej. 

# Jak z niego korzystać

# Generowanie muzyki z poziomu terminala

Żeby skrypt mógł się poprawnie uruchomić, należy zainstalować pythonowe modułu z pliki requirements.txt
oraz pakiety FFmepg, musescore i timidity. 

Aby wypróbować system tworzenia piosenki razem z wokalem należy uruchomić skrypt.sh w katalogu src.
Wygenerowana piosenka będzie w pełni losowa. W celu skorzystania z szerokiego wachlarza opcji przy generacji utworu należy skorzystać z z poniższych skryptów osobno, a następnie wykonać analogiczne komendy jak w skrypt.sh. 

Aby wypróbować system tworzenia muzyki wystarczy uruchomic plik EUTERPE/src/generowanie_muzyki/muzyka.py

Aby wypróbować system tworzenia tekstu wystarczy uruchomić plik EUTERPE/src/generowanie_tekstu/tekst.py

Skrypt generowania muzyki uruchamiamy w terminalu wpisując `python3 muzyka.py`. Zapyta się on nas następnie czy chcemy wybrać parametry utworu. Można zdać się na los lub samodzielnie dostosować opcje. Wybrać można tempo, metrum, tonację, rodzaj użytej skali muzycznej oraz gatunek utworu. Następnie skrypt wygeneruje plik z muzyką o nazwie "muzyka.mid".

Skrypt generowania tekstu uruchamiamy w terminalu wpisując `python3 tekst.py gatunek_muzyki długość_tekstu_piosenki`. 

# Generowanie muzyki z poziomu przeglądarki

W EUTERPE/src/euterpe_django należy przy pierwszym uruchomieniu wykonać wszystkie oczekujące migracje poleceniem:

  `python3 manage.py makemigrations`
  
  `python3 manage.py migrate`

Następnie należy uruchomić deweloperski serwer poleceniem:

  `python3 manage.py runserver`
  
Wtedy uzyskujemy dostęp do strony `127.0.0.1:8000` w przeglądarce, gdzie znajdziemy platformę.

Skrypt generowania tekstu uruchamiamy w terminalu wpisując `python3 tekst.py gatunek_muzyki długość_tekstu_piosenki`. 
Aby skorzystać z wszystkich dostępnych gatunków muzyki, należy w katalogu EUTERPE/src/generowanie_tekstu/ zapisać pliki json, które są dostępne pod linkiem:
https://drive.google.com/open?id=1XJjHaE632b7YFjB5o5X0tOeOPDIUM-Rg

Życzymy dużo zabawy z naszymi generatorami!


# Dostępne gatunki

Obecnie dostępne gatunki generowania tekstu to:
'Other', 'Metal', 'Country', 'Folk', 'Rock', 'Not Available', 'Jazz', 'Indie', 'Electronic', 'Pop', 'Hip-Hop'

