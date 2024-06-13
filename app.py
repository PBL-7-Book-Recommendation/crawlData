import schedule
import time
from crawlWeb import crawlThriftBooks
from crawlWeb.crawlGoodReads import crawlGoodReads
import preprocessData
from save import saveThriftBooks, saveGoodReads
from datetime import date


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

    # getThriftBooks()
    getGoodReads()
    print("Task executed!")


def main():
    schedule.every().day.at("00:00").do(getData)

    while True:
        schedule.run_pending()
        time.sleep(60)  # sleep for 60s before checking again


if __name__ == "__main__":
    main()
