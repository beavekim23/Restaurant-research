from selenium import webdriver
from time import sleep, ctime
import requests
from pymongo import MongoClient


def lambda_handler(event, context):
    # Web scraping with headless webdriver from selenium
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    ch_driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    ch_driver.implicitly_wait(5)
    yelp_url = 'https://www.yelp.com/'
    ch_driver.get(yelp_url)

    search_input = ch_driver.find_element_by_id('find_desc')
    search_input.send_keys('restaurants')
    city_input = ch_driver.find_element_by_id('dropperText_Mast')
    city_input.click()
    city_input.send_keys('los angeles')

    search_button = ch_driver.find_element_by_id('header-search-submit')
    search_button.click()

    executed_time = ctime()

    city = 'Los Angeles'
    city_list = ['Los Angeles', 'San Francisco', 'New York']
    all_result_dict = {}

    for city in city_list:
        another_city = ch_driver.find_element_by_id('search_location')
        another_city.click()
        another_city.send_keys(city)
        another_button = ch_driver.find_element_by_xpath('//*[@id="header_find_form"]/div/div[2]/div/div[2]/button')
        another_button.click()

        result_list = []
        result_dict = {}

        r_path = '//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div/div/div[2]/div[1]/div[1]/div[1]'
        restaurants = ch_driver.find_elements_by_xpath(r_path)

        # make a result_list
        for item in restaurants:
            title = item.find_element_by_tag_name('h3').text

            #pass ads
            if title[0].isdigit() == False:
                pass
            else:
                restaurant_name = item.find_element_by_tag_name('a').text
                link = item.find_element_by_tag_name('a').get_attribute('href')

                divs = item.find_elements_by_tag_name('div')

                rating_span = divs[1].find_element_by_tag_name('span')
                rating_div = rating_span.find_element_by_tag_name('div')
                rating = rating_div.get_attribute('aria-label')

                review_span = divs[3].find_element_by_tag_name('span')
                review_count = review_span.text

                pk_span = divs[4].find_elements_by_tag_name('span')
                if pk_span[0].text[0] == '$':
                    price = pk_span[0].text
                    keyword = pk_span[1].text
                else:
                    price = 'N/A'
                    keyword = pk_span[0].text

                result_list.append([restaurant_name, link, rating, review_count, price, keyword])

        # make a result_dict
        for i, item in enumerate(result_list):
            result_dict[str(i+1)] = {
                'restaurant_name' : item[0],
                'link' : item[1],
                'rating' : item[2],
                'review_count' : item[3],
                'price_index' : item[4],
                'keyword' : item[5]
            }

        #make all_result_dict
        all_result_dict[city] = result_dict

    # Connect MongoDB
    mongo_uri = "mongodb://<mLab_username>:<mLab_password>@ds145299.mlab.com:45299/mydbinstance"
    client = MongoClient(mongo_uri)
    db = client.mydbinstance
    yelp_collection = db.yelp

    data = {
        "executed": executed_time,
        "restaurants": all_result_dict,
    }

    yelp_collection.insert_one(data)

    return data

# for check
lambda_handler("ab", "something")
