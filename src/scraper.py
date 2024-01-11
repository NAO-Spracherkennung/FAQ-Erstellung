# coding=utf-8

import requests
from bs4 import BeautifulSoup

# scraping logic 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

hauptseite = 'https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/'

generalPage = requests.get(hauptseite,headers=headers)
soupGeneral = BeautifulSoup(generalPage.text, 'html.parser')

main_content = soupGeneral.find_all('div', class_= 'grid-group stop') #content ist in diesen div's

for div_element in main_content:
    headings = div_element.find_all(['h1', 'h2', 'h3'])
    for heading in headings:
        print("ueberschrift:" + heading.text)
        next_wysiwyg = heading.find_next('div', class_='wysiwyg')
        if next_wysiwyg:
            text = next_wysiwyg.get_text(strip=True)
            print("Text: " + text)        
            print('-' * 50)



def download_pdfs(url): 
    pdf = []

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    main = soup.find('main')
    links = main.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

    i = 0

    for link in links: 
        link_http = 'http://www.hwr-berlin.de' + link.get('href')
        print(link_http)
        response = requests.get(link_http, headers=headers)

        # Write content in pdf file
        pdf = open("pdf"+str(i)+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
        print("File ", i, " downloaded")

print("All PDF files downloaded")