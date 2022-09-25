import requests
import os
import time
import configparser
import json
from datetime import datetime


class Netatmo:
    def __init__(self, current_time=time.time(), expires_in=0, netatmo_output={}):

        self.current_time = current_time
        self.expires_in = expires_in
        self.__netatmo_output = netatmo_output
        self.counter = 0
        self.autorization_data = {}

        SETTING_FILE_PATH = os.path.join(os.path.dirname(__file__), "settings.ini")
        self.config = configparser.ConfigParser()
        self.config.read(SETTING_FILE_PATH)
        self.API_ENDPOINT = "https://api.netatmo.com"
        self.CLIENT_ID = self.config["CODES"]["client_id"]
        self.CLIENT_SECRET = self.config["CODES"]["client_secret"]
        self.REDIRECT_URI = "https://google.com"

        self.checktime_for_exchange_code = time.time() + self.expires_in
        self.checktime_for_timer = time.time()

        self.update_data()

    """ Må fortsatt implementere en slags "wait" dersom programmet havner i en exception
        Oppdatert tidspunkt må også hentes fra denne klassen i et nøkkelord.

    """

    def update_data(self):
        try:
            if self.checktime_for_exchange_code < time.time():
                self.autorization_data = self.exchange_code()
                self.checktime_for_exchange_code = time.time() + self.expires_in

            if self.checktime_for_timer < time.time():
                self.expires_in = self.autorization_data["expires_in"]
                authorization_token = self.autorization_data["access_token"]
                response = self.get_data(authorization_token)

                # data collection
                self.__netatmo_output["name_livingroom"] = response.json()["body"]["devices"][0]["module_name"]
                self.__netatmo_output["temp_livingroom"] = response.json()["body"]["devices"][0]["dashboard_data"]["Temperature"]
                self.__netatmo_output["co2_livingroom"] = response.json()["body"]["devices"][0]["dashboard_data"]["CO2"]
                self.__netatmo_output["humidity_livingroom"] = response.json()["body"]["devices"][0]["dashboard_data"]["Humidity"]
                self.__netatmo_output["noise_livingroom"] = response.json()["body"]["devices"][0]["dashboard_data"]["Noise"]
                self.__netatmo_output["pressure"] = response.json()["body"]["devices"][0]["dashboard_data"]["Pressure"]

                self.__netatmo_output["name_bedroom"] = response.json()["body"]["devices"][0]["modules"][1]["module_name"]
                self.__netatmo_output["temp_bedroom"] = response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["Temperature"]
                self.__netatmo_output["humidity_bedroom"] = response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["Humidity"]
                self.__netatmo_output["temptrend_bedroom"] = response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["temp_trend"]

                self.__netatmo_output["name_outside"] = response.json()["body"]["devices"][0]["modules"][0]["module_name"]
                self.__netatmo_output["temp_outside"] = response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["Temperature"]
                self.__netatmo_output["humidity_outside"] = response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["Humidity"]
                self.__netatmo_output["temptrend_outside"] = response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["temp_trend"]
                self.__netatmo_output["online"] = True
                self.__netatmo_output["counter"] = self.counter

                self.counter += 1

                self.checktime_for_timer = time.time() + int(self.config["TIMERS"]["refresh"])

            # else:
            #     response = self.get_data(authorization_token)
        except Exception as e:
            # print(e)
            self.__netatmo_output["online"] = False
            # time.sleep(int(self.config["TIMERS"]["noconnection"]))

    def __call__(self):
        self.update_data()
        return self.__netatmo_output

    @property
    def netatmo_output(self):
        # self.update_data()
        return self.__netatmo_output

    def exchange_code(self):
        data = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "password",
            "username": self.config["USERINFO"]["Username"],
            "password": self.config["USERINFO"]["Password"],
            "redirect_uri": self.REDIRECT_URI,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        r = requests.post(self.API_ENDPOINT + "/oauth2/token", data=data, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_data(self, auth_token):
        hed = {"Authorization": "Bearer " + auth_token}
        data = {"": ""}
        url = "https://api.netatmo.com/api/getstationsdata?device_id=70%3Aee%3A50%3A73%3Af1%3Aa4&get_favorites=true"
        return requests.get(url, data, headers=hed)


class Met_data:
    def __init__(self, alt, lat, long):
        self.alt = alt
        self.lat = lat
        self.long = long
        self.counter = 0

        self.response = self.get_met_data()
        self.met_data = json.loads(self.response.text)
        self.expires = self.response.headers["Expires"]
        self.expires_print = self.get_time_from_expires()

    def __call__(self):
        if self.check_expired():
            self.counter += 1
            self.response = self.get_met_data()
            self.met_data = json.loads(self.response.text)
            self.expires = self.response.headers["Expires"]
            self.expires_print = self.get_time_from_expires()

    # return True if currenttime > expired
    def check_expired(self):
        return datetime.utcnow() > datetime.strptime(self.expires, "%a, %d %b %Y %H:%M:%S %Z")

    def get_time_from_expires(self):
        lst = self.expires.split()
        return lst[4]

    def get_met_data(self):
        hed = {"user-agent": "anders@karlskaas.no"}
        data = {"": ""}
        url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?altitude=" + str(self.alt) + "&lat=" + str(self.lat) + "&lon=" + str(self.long)
        return requests.get(url, data, headers=hed)


def testfunc(data):
    data()


def main():
    weather = Netatmo()
    print(type(weather))

    print(weather.netatmo_output)


if __name__ == "__main__":
    main()
