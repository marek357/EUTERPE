# Opis projektu

Projekt prowadzony na zajęcia z Inżynierii Oprogramowania na Wydziale MIMUW w roku akademickim 2019/2020. 
Założenia, jakie nam przyświecają przy tworzeniu tego projektu to wytworzenie jak najwyższej jakości narzędzi dla konsumenta, pragnącego posłuchać muzyki oryginalnej, jeszcze wcześniej nie słyszanej. 

# Jak z niego korzystać

Żeby skrypt mógł się poprawnie uruchomić, należy do katalogu res pobrać plik lyrics.csv z linku:
https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics/data#

Aby wypróbować system tworzenia muzyki wystarczy uruchomic plik EUTERPE/src/generowanie_muzyki/muzyka.py

Aby wypróbować system tworzenia tekstu wystarczy uruchomić plik EUTERPE/src/generowanie_tekstu/tekst.py

Oba skrypty uruchamiamy będąc w lokalizacji podanej powyżej

Skrypt generowania muzyki uruchamiamy w terminalu wpisując `python3 muzyka.py`. Zapyta się on nas następnie czy chcemy wybrać parametry utworu. Można zdać się na los lub samodzielnie dostosować opcje. Wybrać można tempo, metrum, tonację, rodzaj użytej skali muzycznej oraz gatunek utworu. Następnie skrypt wygeneruje plik z muzyką o nazwie "muzyka.mid".

Skrypt generowania tekstu uruchamiamy w terminalu wpisując `python3 tekst.py gatunek_muzyki długość_tekstu_piosenki`

Życzymy dużo zabawy z naszymi generatorami!


# Dostępne gatunki

Obecnie dostępne gatunki generowania tekstu to:
'Other', 'Metal', 'Country', 'R&B', 'Folk', 'Rock', 'Not Available', 'Jazz', 'Indie', 'Electronic', 'Pop', 'Hip-Hop'
Można uzyskać listę obecnie wspieranych gatunków muzycznych przez uruchomienie skryptu znajdującego się w lokalizacji EUTERPE/src/checkAvailGenres.py
Znajdując się w EUTERPE/src możemy go wywołać w następujący sposób `python3 checkAvailGenres.py`
