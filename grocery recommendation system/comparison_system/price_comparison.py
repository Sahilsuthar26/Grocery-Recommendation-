import requests
from bs4 import BeautifulSoup
from Recommendation_System.collaborative_filtering import GroceryRecommendation
from Recommendation_System.user import return_users


class PriceComparison:

    def __init__(self, search_item):
        self.__search_item = search_item.replace(" ", "+")
        self.__headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
        self.amazon_search()
        self.grofers_search()

    def amazon_search(self):
        url = "https://www.amazon.in/s?k=" + self.__search_item #+ "&i=pantry"
        get_soup = self.beautiful_soup(url)
        #         for ur in get_soup.find_all('a'):
        #             print(ur.get('href'))
        new_soup = self.amazon_link_finder(get_soup)
        self.__amazon_price_title = self.get_amazon_price_title(new_soup)

    def grofers_search(self):
        url = "https://grofers.com/s/?q=" + self.__search_item + "&suggestion_type=0&t=1"
        get_soup = self.beautiful_soup(url)
        new_soup = self.grofers_link_finder(get_soup)
        self.__grofers_price_title = self.get_grofers_price_title(new_soup)

    def beautiful_soup(self, url):
        self.__request_page = requests.get(url, headers=self.__headers)
        soup = BeautifulSoup(self.__request_page.content, 'html.parser')
        return soup

    def amazon_link_finder(self, soup):
        booll = True
        get_url_key = ""
        for i in soup.find_all('a'):
            link = i.get('href')
            if str(link) == "None" or len(link) == 1 or "/gp/" in str(link):
                pass
            else:
                #                 newval=self.__search_item[0].upper() + self.__search_item[1:]
                newval = "keywords=" + self.__search_item
                #                 newval="keywords=whole+wheat+atta"
                #     keywords=whole+wheat+aata
                if booll:
                    #                     if "/s?k=" in str(link):
                    if newval in str(link):
                        get_url_key = str(link)
                        booll = False
                else:
                    if "nav" in str(link):
                        break
                    get_url_key = str(link)
                    break
        print("final ", "https://www.amazon.in" + get_url_key)
        return self.beautiful_soup("https://www.amazon.in" + get_url_key)

    def grofers_link_finder(self, soup):
        get_url_key = ""
        for i in soup.find_all('a'):
            link = i.get('href')
            if str(link) == "None" or len(link) == 1:
                pass
            else:
                if '/prn/' in link:
                    get_url_key = link
                    break
        print("final ", "https://grofers.com" + get_url_key)
        return self.beautiful_soup("https://grofers.com" + get_url_key)

    def get_amazon_price_title(self, soup):
        title = soup.title.string
        try:
            price = soup.find(id="priceblock_ourprice").string
        except:
            price = soup.find(id="priceblock_dealprice").string
        return (title, price)

    def get_grofers_price_title(self, soup):
        title = soup.title.string
        price = soup.find(class_="pdp-product__price--new").get_text()
        return (title, price)

    def display(self):
        print("AMAZON :")
        print("PRODUCT TITLE :", self.__amazon_price_title[0])
        print("PRODUCT PRICE :", self.__amazon_price_title[1])
        print("GROFERS :")
        print("PRODUCT TITLE :", self.__grofers_price_title[0])
        print("PRODUCT PRICE :", self.__grofers_price_title[1])
        return [[self.__amazon_price_title[0], self.__amazon_price_title[1]], [self.__grofers_price_title[0],
                                                                               self.__grofers_price_title[1]]]


if __name__ == '__main__':
    search = input("enter search item : ")
    PriceComparison(search)
    val = return_users(search)
    print(val[0], val[1])
    re = GroceryRecommendation(val[0], val[1])
    print(re.get_recommendation())
