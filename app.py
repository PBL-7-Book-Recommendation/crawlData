from utils import crawlURL, crawlBookData
import pandas as pd

if __name__ == "__main__":

    book_info = crawlURL.get_new_book_url()

    # load data from csv
    book_info = pd.read_csv("books_url.csv").to_dict("records")
    book_data = crawlBookData.get_books_data(book_info)

    # Handle data after crawling
    # to csv
    df = pd.DataFrame(book_data)
    df.to_csv("books_info.csv", index=False)
    # Check xem sách nào không có đủ record (ISBN,...)
    #############################
