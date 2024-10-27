import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

#base link 
link_international = "https://malijet.com/actualite_internationale/?page="

#function to scrape site
def scrape_pages(link):
    articles = []

    #for loop for each page to be scraped
    for page in range(1, 276):
        #url pagenumber refreshes for every iteration of the loop
        url = f'{link}{page}'

        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        result = requests.get(url, headers=headers)
        scraper = BeautifulSoup(result.text, 'html.parser')

        #finds container of the articles and finds every article url in container
        page_container = scraper.find('div', id="v_container")
        article_list = page_container.find_all('div', class_="col-md-6")

        print(page)

        #loops through all
        for article_info in article_list:
            #gets article date f
            article_date_item = article_info.find('div', class_="bas_articles").find('h5').find_next_sibling('h5').text
            article_date = article_date_item.split(' ')[2] + article_date_item.split(' ')[3]

            #gets url to article
            article_url = article_info.find('h5', class_="card-title").find('a', href=True)['href']
            
            #creates a dictionary with keywords to be searched for
            article_dictionary = {"url": article_url, "date": article_date, 
                                  "keywords": {'Russie': 0, 'Russe': 0, 'Poutine': 0, 'Sputnik': 0, 'RT': 0, 'New Eastern Outlook': 0, 'Tass': 0,},
                       }
            
            #scrapes article
            article_request = requests.get(article_url)
            article_scraper = BeautifulSoup(article_request.text, "html.parser")

            #container with article text
            text_container = article_scraper.find('div', id="card_img_jt")

            if text_container.text != None:
                #checks article for every keyword
                for keyword in article_dictionary["keywords"]:
                    if keyword in text_container.text:
                        article_dictionary["keywords"][keyword] += 1

                articles.append(article_dictionary)

                time.sleep(1)

            

        months = {}
        
        #goes through every article and turns every month found into a dictionary in the months dictionary
        for article in articles:
            date = article["date"]
            keywords = article["keywords"]

            if date not in months:
                months[date] = {}

            #adds keywords for every month dictionary and then tallys the count
            for keyword, count in keywords.items():
                if keyword not in months[date]:
                    months[date][keyword] = 0
                
                months[date][keyword] += count
        
        print(months)

        wb = Workbook()
        ws = wb.active

          #row containing all the keywords being searched for
    ws['B1'] = 'Russie'
    ws['C1'] = 'Russe'
    ws['D1'] = 'Poutine'
    ws['E1'] = 'Sputnik'
    ws['F1'] = 'RT'
    ws['G1'] = 'New Eastern Outlook'
    ws['H1'] = 'Tass'

    #organizes monthly keywords and places them on a seperate row per month
    for month, results  in months.items():
        item_list = []
        
        item_list.append(month)
        for key, value in results.items():
            item_list.append(value)
        ws.append(item_list)
    wb.save('malijet_data_pg1-276.xlsx')



scrape_pages(link_international)