#!/bin/bash

if [ -f generowanie_muzyki/muzyka.mid ] ; then
    rm generowanie_muzyki/muzyka.mid
fi

if [ -f generowanie_muzyki/wokal.mid ] ; then
    rm generowanie_muzyki/wokal.mid
fi

cd generowanie_muzyki

argumenty="T"
argumenty+=$'\n'
argumenty+="$1"

echo "$argumenty"
python3 muzyka.py <<< "$argumenty"

cd ..

echo "Wygenerowano muzykę"

cd generowanie_tekstu

python3 tekst.py < ../generowanie_muzyki/infoTekst.txt

cd ..

python3 generowanie_muzyki/midi2voice.py generowanie_tekstu/xd.txt generowanie_muzyki/wokal.mid female "$(< generowanie_muzyki/wokalTekst.txt)"

timidity generowanie_muzyki/muzyka.mid -Ow -o muzyka.wav

ffmpeg -y -i muzyka.wav -i voice.wav -filter_complex "[0:0]volume=0.3[a];[1:0]volume=1.0[b];[a][b]amix=inputs=2:duration=longest" -c:a libmp3lame piece.wav
