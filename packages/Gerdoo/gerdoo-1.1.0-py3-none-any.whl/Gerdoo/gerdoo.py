import requests
from bs4 import BeautifulSoup

class Gerdoo:
    def __init__(
            self,
            Query : str,
            Proxies = {},
            Base_Url : str = "https://gerdoo.me",
            User_Agent : str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        ):
        "ساخت یک شیء از جستجوگر"
        self.Query = str(Query)
        self.Proxies = Proxies
        self.User_Agent = str(User_Agent)
        self.Base_Url = str(Base_Url)

    def GetSuggestions(self):#
        "دریافت پیشنهادات"
        try:
            return list(
                requests.get(
                    f"{self.Base_Url}/get_suggestions_meta_search/",
                    params={
                        "query" : self.Query
                    },
                    proxies=self.Proxies,
                    headers={
                        "user-agent" : self.User_Agent
                    }
                ).json()
            )
        except:
            return None
    
    def search(
            self,
            Number : int = 10,
            Page : str | int = 1
        ):#
        try:
            soup = BeautifulSoup(
                requests.get(
                    f"{self.Base_Url}/search/",
                    params={
                        "query" : self.Query,
                        "page" : str(Page)
                    },
                    headers={
                        "user-agent" : self.User_Agent
                    },
                    proxies=self.Proxies
                ).text,
                "html.parser"
            )
            ListResults = []

            for Index , result in enumerate(soup.find_all("div" , class_="search-result-wrapper")):
                if int(Index) == int(Number):
                    break
                Item = {}

                if result.find("a" , class_="none-decoration blue visited-link"):
                    Item.update({
                        "url" : str(result.find("a" , class_="none-decoration blue visited-link").get("href")),#
                    })

                if result.find("div" , class_="favicon-wrapper"):
                    Item.update({
                        "favicon" : str(result.find("div" , class_="favicon-wrapper").find("img").get("src")),#
                    })

                if result.find("span" , class_="highlight-text"):
                    Item.update({
                        "description" : str(result.find("span" , class_="highlight-text").text).strip(),#
                    })

                if result.find("div" , class_="title hover-bottom-line text-right"):
                    Item.update({
                        "title" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip(),#
                    })
                
                if len(Item.keys()) != 0:
                    ListResults.append(Item)
            return ListResults
        except:
            return None
        
    def search_image(
            self,
            Number : int = 10
        ):#
        "جستجوی تصاویر"
        try:
            soup = BeautifulSoup(
                requests.get(
                    f"{self.Base_Url}/search_image/",
                    params={
                        "query" : self.Query
                    },
                    headers={
                        "user-agent" : self.User_Agent
                    },
                    proxies=self.Proxies
                ).text,
                "html.parser"
            )
            ListResults = []

            for Index , result in enumerate(soup.find_all("div" , class_="image-card-wrapper")):
                if int(Index) == int(Number):
                    break

                Item = {}

                if result.find("img" , class_="cursor-pointer"):
                    Item.update({
                        "image" : str(result.find("img" , class_="cursor-pointer").get("src")),
                    })
                
                if result.find("div" , class_="title m-1 hidden-scroll text-right"):
                    Item.update({
                        "title" : str(result.find("div" , class_="title m-1 hidden-scroll text-right").text).strip(),
                    })

                if result.find("div" , class_="source-domain m-1"):
                    Item.update({
                        "domain" : str(result.find("div" , class_="source-domain m-1").text).strip(),
                    })

                if result.find("a" , class_="none-decoration source-url"):
                    Item.update({
                        "url" : str(result.find("a" , class_="none-decoration source-url").get("href"))
                    })
                
                if len(Item.keys()) != 0:
                    ListResults.append(Item)
            return ListResults
        except:
            return None

    def search_video(
            self,
            Number : int = 10
        ):
        "جستجوی ویدیو ها"
        try:
            soup = BeautifulSoup(
                requests.get(
                    f"{self.Base_Url}/search_video/",
                    params={
                        "query" : self.Query
                    },
                    headers={
                        "user-agent" : self.User_Agent
                    },
                    proxies=self.Proxies
                ).text,
                "html.parser"
            )
            ListResults = []

            for Index , result in enumerate(soup.find_all("div" , class_="video-card")):
                if int(Index) == int(Number):
                    break

                Item = {}

                if result.find("div" , class_="title hover-bottom-line text-right"):
                    Item.update({
                        "title" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip()
                    })

                if result.find("div" , class_="w-100 highlight-text m-1 text-right"):
                    Item.update({
                        "date" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip()
                    })
                
                if result.find("div" , class_="title hover-bottom-line text-right"):
                    Item.update({
                        "url" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip()
                    })
                
                if result.find("div" , class_="title hover-bottom-line text-right"):
                    Item.update({
                        "description" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip()
                    })

                if result.find("div" , class_="title hover-bottom-line text-right"):
                    Item.update({
                        "description" : str(result.find("div" , class_="title hover-bottom-line text-right").text).strip()
                    })

                
                if len(Item.keys()) != 0:
                    ListResults.append(Item)

            return ListResults
        except:
            return None

    def search_news(
            self,
            Number : int = 10
        ):#
        "جستجوی اخبار"
        try:
            soup = BeautifulSoup(
                requests.get(
                    f"{self.Base_Url}/search_news/",
                    params={
                        "query" : self.Query
                    },
                    headers={
                        "user-agent" : self.User_Agent
                    },
                    proxies=self.Proxies
                ).text,
                "html.parser"
            )
            ListResults = []

            for Index , result in enumerate(soup.find_all("div" , class_="news-card")):
                if int(Index) == int(Number):
                    break

                Item = {}

                if result.find("div" , class_="title").find("a" , class_="blue"):
                    Item.update({
                        "url" : str(result.find("div" , class_="title").find("a" , class_="blue").get("href"))
                    })

                if result.find("div" , class_="title").find("a" , class_="blue"):
                    Item.update({
                        "title" : str(result.find("div" , class_="title").find("a" , class_="blue").text).strip()
                    })

                if result.find("div" , class_="news-info-wrapper").find("div" , class_="color-green mr-2"):
                    Item.update({
                        "news_source" : str(result.find("div" , class_="news-info-wrapper").find("div" , class_="color-green mr-2").text).strip()
                    })

                if result.find("div" , class_="news-info-wrapper").find("div" , class_="color-gray text-right"):
                    Item.update({
                        "date" : str(result.find("div" , class_="news-info-wrapper").find("div" , class_="color-gray text-right").text).strip()
                    })

                if result.find("div" , class_="d-flex flex-column mr-2 ml-2").find("div" , class_="highlight color-gray"):
                    Item.update({
                        "description" : str(result.find("div" , class_="d-flex flex-column mr-2 ml-2").find("div" , class_="highlight color-gray").text).strip()
                    })

                if result.find("img" , class_="cart-rounded"):
                    Item.update({
                        "image" : str(result.find("img" , class_="cart-rounded").get("src"))
                    })
                
                if len(Item.keys()) != 0:
                    ListResults.append(Item)
            return ListResults
        except:
            return None






# f = SearchGerdoo("دلار استرالیا")

# for i in f.search(7):
#     for keyyy , valueee in i.items():
#         print(f"{keyyy} : {valueee}")
#     print("\n\n=================================================================================================\n\n")