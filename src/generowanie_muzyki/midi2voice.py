"""
Ten plik pochodzi z repozytorium: https://github.com/mathigatti/midi2voice
Udostepniony zostal na licencji MIT
MIT License

Copyright (c) 2018 Mathias Gatti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import urllib.request
from functools import reduce

from midi2xml import midi2xml

import requests
from pydub import AudioSegment

VOICE_XML = "voice.xml"
VOICE_WAV = "voice.wav"

def renderizeVoice(lyrics,midiPath,sex,tempo):
	midi2xml(lyrics,midiPath,VOICE_XML,tempo)
	
	if sex == "male":
		request(VOICE_XML, VOICE_WAV,"male")
	else:
		request(VOICE_XML, VOICE_WAV,"female")
	#sinsyFix(VOICE_WAV,tempo)

def sinsyFix(wavPath,tempo):
	song = AudioSegment.from_wav(wavPath)
	song = song[int(1000*4*60/tempo):] # Delete extra 4 beats of silence at the beginning of the file
	song.export(wavPath,format="wav")

def request(xml_file_path,wavPath,sex="female"):
	if sex == "male":
		SPKR = 5
	else:
		SPKR = 4

	headers = {'User-Agent': 'Mozilla/5.0'}
	payload = {'SPKR_LANG':'english', 'SPKR':SPKR, 'VIBPOWER':'1', 'F0SHIFT':'0'}
	files = {'SYNSRC': open(xml_file_path,'rb')}

	# Sending post request and saving response as response object 
	r = requests.post(url = 'http://sinsy.sp.nitech.ac.jp/index.php',headers=headers,data=payload,files=files)
	htmlResponse = r.text.split("temp/")

	# Magic scraping of the website to find the name of the wav file generated
	urlfileName = findWavNameOnWebsite(htmlResponse)

	if urlfileName is None:
		raise Exception("No wav file found on sinsy.jp")
	else:
		download(urlfileName,wavPath)

def findWavNameOnWebsite(htmlResponse):
	urlfileName = None
	for line in htmlResponse:
		parts = line.split(".")
		if parts[1][:3] == "wav":
			urlfileName = parts[0]
			break
	return urlfileName

def download(urlfileName,wavPath):
	urllib.request.urlretrieve("http://sinsy.sp.nitech.ac.jp/temp/" + urlfileName + ".wav", wavPath)

def main():
	textFilePath = sys.argv[1]
	midiPath = sys.argv[2]
	sex = "female"
	tempo = 80

	if len(sys.argv) >= 4:	
		sex = sys.argv[3]
		if len(sys.argv) >= 5:
			tempo = int(sys.argv[4])

	with open(textFilePath, 'r') as text:
		lyrics = text.readlines()

	print("Running voice renderization")
	renderizeVoice(lyrics,midiPath,sex, tempo)
	print("Finished voice renderization")

main()
