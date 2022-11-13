import requests
import bs4
import xlsxwriter



list_link = ''
#Request input until valid one received
while "https://www.goodreads.com/list/show" not in list_link:
    list_link = input("Enter the link to a goodreads List \n Example: https://www.goodreads.com/list/show/2681.Time_Magazine_s_All_Time_100_Novels\n")
    if "https://www.goodreads.com/list/show" not in list_link:
        print("Invalid Input")

#use requests/bs4 to pull page source/format and clean up
pull = requests.get(list_link)
pull_soup = bs4.BeautifulSoup(pull.text,"lxml")
page_title = pull_soup.select("title")
page_title = page_title[0].text
page_title, quantity = page_title.split('(')
quantity = quantity.replace(')','')

print("Selected list: " + page_title)
print(quantity.center(50,' '))

#Pull book titles along with corresponding authors and rating information
titles = pull_soup.select(".bookTitle")
authors = pull_soup.select(".authorName")
ratings = pull_soup.select(".minirating")

#Clean up each list leaving only desired information
author_list = [(i.text).strip() for i in authors ]
book_list = [(i.text).strip() for i in titles ]
rating_list = [(i.text).strip() for i in ratings]

#Moves all this information into list of lists containing all 3 elements
books_authors_ratings = list(zip(book_list,author_list,rating_list))


##### Fix column width so it matches longest title, author, and rating
long_author = ''
long_title = ''
long_rating = ''

for i in author_list:
    if len(i) > len(long_author):
        long_author = i
        
for i in book_list:
    if len(i) > len(long_title):
        long_title = i
  
for i in rating_list:
    if len(i) > len(long_rating):
        long_rating = i


#Create spreadsheet with file name matching the name of the list
workbook = xlsxwriter.Workbook(page_title+'.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0

#loop through the list, writing all information to the spreadsheet
for title, author, rating in (books_authors_ratings):
    worksheet.write(row, col, title)
    worksheet.write(row, col + 1, author)
    worksheet.write(row, col + 2, rating)
    row += 1
worksheet.set_column(0,0,len(long_title))
worksheet.set_column(1,1,len(long_author))
worksheet.set_column(2,2,len(long_rating))

workbook.close()

print("file saved as " + page_title + '.xlsx in current working directory')