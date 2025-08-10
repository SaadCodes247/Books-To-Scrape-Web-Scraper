from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

# 1. Looping through each page

start_time = time.time()

book_title = []
book_category = []
book_UPC = []
book_price_with_tax = []
book_availablilty = []

for page in range(1, 51):

  all_books_to_scrape_site = f'https://books.toscrape.com/catalogue/category/books_1/page-{page}.html'
  all_books_response = requests.get(all_books_to_scrape_site)
  print('Page number: ' + str(page) + ' has status code: ' + str(all_books_response.status_code) + '\n')

  # 2. Getting the link for each book
  all_books_soup = BeautifulSoup(all_books_response.text)

  all_individual_book_links = [book.get('href') for book in all_books_soup.find('section').find_all('a')]

  # Step a: I need to remove the duplicates
  all_book_links = list(set(all_individual_book_links))
  # Step b: Remove all the ../../../
  all_book_links = [link[6:] for link in all_book_links]
  # Step c: Need to add the actual prefix to the book (rest of the site)
  all_book_links = ['https://books.toscrape.com/catalogue/' + link for link in all_book_links]
  # setp d: Skip pages:
  all_book_links = [book for book in all_book_links if 'index' in book]

  # 3. Set up a soup for each book and extract the book details from each book link

  for book_link in all_book_links:
    book_link_response = requests.get(book_link)
    print('Book has status code ' + str(book_link_response.status_code))

    each_book_soup = BeautifulSoup(book_link_response.text, 'html.parser')

    book_title.append(each_book_soup.find(class_ = 'col-sm-6 product_main').h1.text)
    book_category.append(each_book_soup.find(class_ = 'breadcrumb').find_all('a')[2].text)
    book_UPC.append(each_book_soup.find(class_ = 'table table-striped').find_all('tr')[0].text.strip())
    book_price_with_tax.append(each_book_soup.find(class_ = 'table table-striped').find_all('tr')[3].text.strip()[19:])
    book_availablilty.append(each_book_soup.find(class_ = 'table table-striped').find_all('tr')[5].text.strip()[22:])

end_time = time.time()

print(f'time taken: {end_time - start_time} seconds')

# Make dataframe

df_all_books_to_scrape = pd.DataFrame({'Book_Title': book_title,
                                       'Book_Category': book_category,
                                       'Book_UPC': book_UPC,
                                       'Book_Price_With_Tax': book_price_with_tax,
                                       'Book_Availability': book_availablilty})

# CSV

all_books_to_scrape_csv = df_all_books_to_scrape.to_csv('all_books_to_scrape_details.csv', index=False)