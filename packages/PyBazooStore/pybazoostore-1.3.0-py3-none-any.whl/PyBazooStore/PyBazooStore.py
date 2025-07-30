import requests

from .searched_by import Searched_by




class BazooStore:
    def __init__(
            self,
            proxies = {},
            User_Agent : str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            BaseURL : str = "https://api.bazoostore.ir"
        ):
        self.proxies = proxies
        self.BaseURL = str(BaseURL)
        self.User_Agent = str(User_Agent)


    def GetBestBots(
            self,
            offset : str | int = 1
        ):
        "برای دریافت بازو هایی که جز برترین بازو ها هستند به کار می رود"
        try:
            return list(
                requests.post(
                    f"{self.BaseURL}/best",
                    json={
                        "offset" : str(offset)
                    },
                    proxies=self.proxies,
                    headers={
                        "user-agent" : self.User_Agent
                    }
                ).json()["value"]
            )
        except:
            return None




    def GetNewBots(
            self,
            offset : str | int = 1
        ):
        "برای دریافت بازو هایی که جدیدا به بازو استور اضافه شدند به کار می رود"
        try:
            return list(
                requests.post(
                    f"{self.BaseURL}/bot",
                    json={
                        "offset" : str(offset)
                    },
                    proxies=self.proxies,
                    headers={
                        "user-agent" : self.User_Agent
                    }
                ).json()["value"]
            )
        except:
            return None


    def GetRandomBots(self):
        "برای دریافت ربات های تصادفی استفاده می شود"
        try:
            return list(
                requests.get(
                    f"{self.BaseURL}/random",
                    proxies=self.proxies,
                    headers={
                        "user-agent" : self.User_Agent
                    }
                ).json()["value"]
            )
        except:
            return None




    def SearchBots(
            self,
            NameBazoo : str,
            searched_by : Searched_by
        ):
        """
        برای جستجوی ربات در بازو استور به کار می رود
        """
        try:
            return list(
                requests.post(
                    f"{self.BaseURL}/search",
                    json={
                        "search_params" : str(NameBazoo),
                        "searched_by" : str(searched_by.value)
                    },
                    proxies=self.proxies,
                    headers={
                        "user-agent" : self.User_Agent
                    }
                ).json()["value"]
            )
        except:
            return None
    



    def GetDataBot(
            self,
            UsernameBot : str
        ):
        try:
            DataBot = requests.get(
                f"{self.BaseURL}/random/{UsernameBot}",
                proxies=self.proxies,
                headers={
                    "user-agent" : self.User_Agent
                }
            ).json()["value"]
            return {
                "id" : DataBot[0]["id"],
                "name" : DataBot[0]["name"],
                "chat_id" : DataBot[0]["chat_id"],
                "username" : DataBot[0]["username"],
                "description" : DataBot[0]["description"],
                "photo" : DataBot[0]["photo"],
                "track_id" : DataBot[0]["track_id"],
                "created_at" : DataBot[0]["created_at"],
                "average" : DataBot[1]["average"],
                "count" : DataBot[1]["count"]
            }
        except:
            return None
        
