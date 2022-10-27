import time
import pandas as pd
from AmazonScraper import *
from text_preprocessing import *

class web_scraping:
    def __init__(self):
        flip_reviews = []
        fold_reviews = []
        amz_scraper = AmazonScraper()

        flip_url="https://www.amazon.com/SAMSUNG-Unlocked-Smartphone-Intuitive-Warranty/product-reviews/B097CNP994/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"
        fold_url="https://www.amazon.com/Samsung-Electronics-Unlocked-Smartphone-Foldable/product-reviews/B097CNBDX2/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"

        for page_num in range(1, 6):
            flip_reviews.extend(amz_scraper.scrapeReviews(url=flip_url, page_num=page_num))
            time.sleep(1)

        for page_num in range(1, 6):
            fold_reviews.extend(amz_scraper.scrapeReviews(url=fold_url, page_num=page_num))
            time.sleep(1)

        self.flip_df = pd.DataFrame(flip_reviews)
        self.fold_df = pd.DataFrame(fold_reviews)
        self.flip_df.to_csv('amazon product flip review.csv', index=False)
        self.fold_df.to_csv('amazon product fold review.csv', index=False)
        
        self.analyse=text_preprocessing(self)