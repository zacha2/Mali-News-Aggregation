import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

link_international = "https://www.maliweb.net/category/international/page/"


#function for scraping maliweb
def scrape_pages(link):
    #loop for number of pages to scrape
    articles = []
    for page in range(1, 580):
        #concatonated string for to update the page number per page
        url = f'{link}{page}'

        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        result = requests.get(url, headers=headers)
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
                       'keywords': {'Russie': 0, 'Russe': 0, 'Poutine': 0, 'Sputnik': 0, 'RT': 0, 'New Eastern Outlook': 0, 'Tass': 0,},
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
            
            #adds article dictionary to a list of articles
            articles.append(article)

    #keeps track of all the months found in articles
    monthly_keywords = {}

    for article in articles:
        month = article['month']
        keywords = article['keywords']
        
        #adds month to list of months if not already present
        if month not in monthly_keywords:
            monthly_keywords[month] = {}
        
        #goes through keywords dictionary and updates the monthly value
        for keyword, count in keywords.items():
            if keyword not in monthly_keywords[month]:
                monthly_keywords[month][keyword] = 0
            monthly_keywords[month][keyword] += count

    
    #creating a workbook to export data to an xlsx file
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
    for month, results  in monthly_keywords.items():
        item_list = []
        print(month)
        item_list.append(month)
        for key, value in results.items():
            item_list.append(value)
        ws.append(item_list)
    wb.save('maliweb_data_pg1-200.xlsx')




scrape_pages(link_international)
