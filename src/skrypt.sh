#!/bin/bash

#skrypt można uruchomić po wygenerowaniu muzyki za pomocą skryptu muzyka.py oraz tekstu za pomocą skryptu tekst.py

rm generowanie_muzyki/muzyka.mid generowanie_muzyki/wokal.mid

cd generowanie_muzyki

python3 muzyka.py <<< "N"

cd ..

echo "Wygenerowano muzykę"

cd generowanie_tekstu

python3 tekst.py < ../generowanie_muzyki/infoTekst.txt

cd ..

python3 generowanie_muzyki/midi2voice.py generowanie_tekstu/xd.txt generowanie_muzyki/wokal.mid female "$(< generowanie_muzyki/wokalTekst.txt)"

timidity generowanie_muzyki/muzyka.mid -Ow -o muzyka.wav

ffmpeg -y -i muzyka.wav -i voice.wav -filter_complex "[0:0]volume=0.3[a];[1:0]volume=1.0[b];[a][b]amix=inputs=2:duration=longest" -c:a libmp3lame piece.wav
