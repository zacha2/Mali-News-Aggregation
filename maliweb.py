import requests
from bs4 import BeautifulSoup

link_international = "https://www.maliweb.net/category/international/page/"


#function for scraping maliweb
def scrape_pages(link):
    #loop for number of pages to scrape
    articles = []
    for page in range(1):
        #concatonated string for to update the page number per page
        url = f'{link}{page}'
        result = requests.get(url)
        scraper = BeautifulSoup(result.text, 'html.parser')

        #prints pagenumber for clarity
        print(page)

        #grabs container and finds all article containers within
        page_container = scraper.find('div', class_="td-main-content")
        article_containers = page_container.find_all('div', class_="td_module_wrap")

        #gets article info from every article container in page
        for article_container in article_containers:
            #gets the url to access the article
            article_url = article_container.find('h3', class_="entry-title").find('a', href=True)['href']
            article_name = article_container.find('h3', class_='entry-title').text
            article_date = article_container.find('time', class_="entry-date").text
            
            #Splits the article date into monthly segments
            article_month = article_date.split(' ')[1] +article_date.split(' ')[2]

            #making a dictionary for the article for how many keywords it contains
            article = {'name': article_name,
                       'month': article_month, 
                       'keywords': {'Russie': 0, 'Russe': 0, 'Poutine': 0, 'Sputnik': 0, 'RT': 0, 'New Eastern Outlook': 0, 'Ria': 0, 'Tass': 0,},
                       }
            
            #scrapes article link
            article_result = requests.get(article_url)
            article_soup = BeautifulSoup(article_result.text, 'html.parser')

            #main div of article
            article_contents = article_soup.find('div', class_='td-post-content').text

            #looks for keyword in article and adds it to that articles dictionary
            for keyword in article['keywords']:
                if keyword in article_contents:
                    article['keywords'][keyword] += 1
            articles.append(article)

        
    monthly_keywords = []
    for article in articles:


            


scrape_pages(link_international)
