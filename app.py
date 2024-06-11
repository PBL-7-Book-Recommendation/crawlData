from utils import crawlURL, crawlBookData
import pandas as pd

if __name__ == "__main__":

    books_url = crawlURL.get_new_book_url()

    # load books_url from csv
    # books_url = pd.read_csv("books_url.csv").to_dict("records")

    books_info = crawlBookData.get_books_data(books_url)

    # Handle data after crawling
    # books_info_df = pd.DataFrame(books_info)
    # books_info_df.to_csv("books_info.csv", index=False)

    #############################
    # Them phan schedule de crawl data moi
    # Check xem sách nào không có đủ record (ISBN,...) thì không preprocess
    # Sau do dưa vao DB
    #############################
