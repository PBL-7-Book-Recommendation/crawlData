import schedule
import time
# from crawlWeb import crawlThriftBooks
import preprocessData
import pandas as pd
from save import saveThriftBooks, saveBookCrossing
import os

def getThriftBooks():
    rawFilePath = os.path.join(os.path.dirname(os.getcwd()), 'src/dataset/thrift-books/raw/1st_raw_thrift_books.csv')
    # rawFilePath = os.path.join(os.path.dirname(os.getcwd()), 'crawlData/dataset/thrift-books/raw/1st_raw_thrift_books.csv')
    df = preprocessData.executeByAttribute(rawFilePath=rawFilePath, attribute='description')
    columns = ['id', 'title', 'description', 'book_cover', 'image_url', 'release_date', 'publisher', 'number_of_pages', 'price', 'authors', 'rating', 'number_of_ratings', 'number_of_reviews', 'preprocessed_description']
    df = pd.read_csv(rawFilePath, names = columns)
    inserted_books = saveThriftBooks.execute(df)
    return inserted_books

def getBookCrossingBooks():
    rawFilePath = os.path.join(os.path.dirname(os.getcwd()), 'src/dataset/thrift-books/raw/1st_book_crossing_data.csv')
    # rawFilePath = os.path.join(os.path.dirname(os.getcwd()), 'crawlData/dataset/thrift-books/raw/1st_book_crossing_data.csv')
    df = preprocessData.executeByAttribute(rawFilePath=rawFilePath, attribute='description')
    df = pd.read_csv(rawFilePath)
    inserted_books = saveBookCrossing.execute(df)
    return inserted_books

def getData():
    # if date.today().day != 1:
    #     return

    getThriftBooks()
    print("Task executed!")


def main():
    schedule.every().day.at("00:00").do(getData)

    while True:
        schedule.run_pending()
        time.sleep(60)  # sleep for 60s before checking again

if __name__ == "__main__":
    # main()
    getThriftBooks()