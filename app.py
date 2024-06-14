import schedule
import time
from crawlWeb import crawlThriftBooks
from crawlWeb.crawlGoodReads import crawlGoodReads
import preprocessData
from save import saveThriftBooks, saveGoodReads
from datetime import date
import requests


def getThriftBooks():
    rawFilePath = crawlThriftBooks.execute()
    df = preprocessData.executeByAttribute(
        rawFilePath=rawFilePath, attribute="description", sourceId=1
    )
    print(df)
    inserted_books = saveThriftBooks.execute(df)
    return inserted_books


def getGoodReads():
    rawFilePath = crawlGoodReads.execute()
    df = preprocessData.executeByAttribute(
        rawFilePath=rawFilePath, attribute="description", sourceId=3
    )
    print(df)
    saveGoodReads.execute(df)


def getData():
    if date.today().day != 1:
        return

    getThriftBooks()
    getGoodReads()
    print("Task executed!")
    try:
        requests.get(
            "https://pbl7-book-recommender-content-base.onrender.com/retrain-content-base"
        )
    except Exception as e:
        print("Error when requesting the retrain model API")
        print(e)


def main():
    schedule.every().day.at("00:00").do(getData)

    while True:
        schedule.run_pending()
        time.sleep(60)  # sleep for 60s before checking again


if __name__ == "__main__":
    main()
