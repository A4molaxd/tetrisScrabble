import requests
from bs4 import BeautifulSoup


baseUrl = 'https://dle.rae.es'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
def searchUrl(word):
    r = requests.get(f"{baseUrl}/{word}", headers=header, timeout=5)
    #print(r.text)
    return BeautifulSoup(r.text, 'lxml')
def searchWord(word):
    soup = searchUrl(word)
    articles = []

    for article in soup.select('article.o-main__article'):
        title = ' '.join(article.select_one('h1.c-page-header__title').stripped_strings) if article.select_one('h1.c-page-header__title') else None
        intro = ' '.join(article.select_one('div.c-text-intro').stripped_strings) if article.select_one('div.c-text-intro') else None

        definitions = []
        for li in article.select('li.j'):
            item = li.select_one('div.c-definitions__item')

            if item:
                definitions.append(' '.join(item.stripped_strings))

        articles.append({
            'title': title,
            'intro': intro,
            'definitions': definitions
        })

    return articles
def getArticles(word):
    baseUrl = 'https://dle.rae.es'
    r = requests.get(f'{baseUrl}/{word}')
    soup = BeautifulSoup(r.text, 'lxml')
    definitions = []
    title = ''
    for article in soup.select('article.o-main__article'):
        title = ' '.join(article.select_one('h1.c-page-header__title').stripped_strings) if article.select_one('h1.c-page-header__title') else None
        if ',' in title:
            title.removesuffix(',')
        print(title)
        definitions = []
        for li in article.select('li.j'):
            item = li.select_one('div.c-definitions__item')
            if item:
                definitions.append(' '.join(item.stripped_strings))
        else:
            for li in article.select('li.m'):
                item = li.select_one('div.c-definitions__item')
                if item:
                    definitions.append(' '.join(item.stripped_strings))
        if title == '':
            break
        return (title, definitions)
    for div in soup.select('div.o-main__content'):
        for item in div.select('article'):
            if item:
                entry = ' '.join(item.stripped_strings).split()
                goodLine = ""
    
                for i in entry[1].lower()[1:-1]:
                    if i == "á":
                        goodLine += "a"
                    elif i == "é" or i == "è": 
                        goodLine += "e"
                    elif i == "í":
                        goodLine += "i"
                    elif i == "ó":
                        goodLine += "o"
                    elif i == "ú" or i == "ü":
                        goodLine += "u"
                    else:
                        goodLine += i
                if goodLine == word:
                    print(' '.join(item.stripped_strings).split())
                    title, definitions = getArticles(' '.join(item.stripped_strings).split()[0])
                    return (title, definitions)
    for div in soup.select('div.o-container'):
        for item in div.select('article'):
            if item:
                #entry = ' '.join(item.stripped_strings).split()
                print(' '.join(item.stripped_strings).split())
                title, definitions = getArticles(' '.join(item.stripped_strings).split()[0])
                return (title, definitions)
    return (title, definitions)
print(getArticles("lito"))
