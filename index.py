import random
import requests
import json
from bs4 import BeautifulSoup

# Oyuna Başla
isim = input("Adınız: ")
print(f"\nAdam Asmaca oyununa hoşgeldin {isim}")


# 1. Method - Kelime listesini apiden çekerek oluştur
def getWordListApi():
    url = "https://gist.githubusercontent.com/f/31ce39df408bebd30774458ff09d3d56/raw/c1c3c32a5a9a9965108998a7c7466088ba741813/kelimeler.json"
    response = requests.get(url)
    jsonData = json.loads(response.content)
    return jsonData


# 2. Method - Kelime listesini html scraping ile oluştur
def getWordListScraping():
    url = "https://isimsehirhayvan.net/c/tr/1688841/-/6-harfli-kelime/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    allWords = soup.find_all("li", class_="t3")
    words = []
    for item in allWords:
        words.append(item.get_text().lower())
    return words


# wordArr = getWordListApi()
wordArr = getWordListScraping()
totalWord = len(wordArr) - 1

# Kelimeyi seç
userChars = []
userLife = 5
selectedWord = random.choice(wordArr)


# Harf iste ve kontrol et
def getChar():
    global userChars
    char = input("\nBir harf giriniz: ").lower()
    if char in userChars:
        print("Bu harfi daha önce girmiştin, farklı bir harf dene!")
        getChar()
    else:
        userChars.append(char)
        checkChar()


# Harfi kontrol et
def checkChar():
    global userLife
    text = ""
    correct = 0
    lastChar = userChars[-1]
    for x in selectedWord:
        charStatus = 0
        if userChars:
            for y in userChars:
                if x == y:
                    correct += 1
                    charStatus += 1

        if charStatus == 0:
            text += "_"
        else:
            text += f"{x}"

    if lastChar not in selectedWord:
        userLife -= 1
        print("Yanlış X")
        print(f"Kalan Can: {userLife}")
    else:
        print("Doğru ✓")

    print(f"Kelime: {text}")

    if correct == len(selectedWord):
        print(f"\nTebrikler, kelimeyi bildiniz! Kelime: {selectedWord}")
    elif userLife == 0:
        print(f"\nTüüü yazıklar olsun, kelimeyi bilemedin! Kelime: {selectedWord}")
    else:
        getChar()


print(f"Kelimemiz {len(selectedWord)} harflidir.")
print(f"Toplam {userLife} deneme hakkınız vardır.")
getChar()
