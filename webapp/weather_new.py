import requests
from pathlib import Path
import time
import configparser
from datetime import datetime
import json


class Netatmo:
    def __init__(self) -> None:

        self.__current_time = time.time()
        self.__expires_in = 0
        self.counter = 0
        self.__autorization = {}

        SETTING_FILE_PATH = Path(__file__).parent / "settings.ini"
        self.__config = configparser.ConfigParser()
        self.__config.read(SETTING_FILE_PATH)

        self.__API_ENDPOINT = "https://api.netatmo.com"
        self.__CLIENT_ID = self.__config["CODES"]["client_id"]
        self.__CLIENT_SECRET = self.__config["CODES"]["client_secret"]
        self.__REDIRECT_URI = "https://google.com"

        self.__checktime_for_exchange_code = time.time() + self.__expires_in
        self.__checktime_for_timer = time.time()

        self.update_data()

    def update_data(self) -> None:
        try:
            """Tester for å se om oppdatering er nødvendig.
            Netatmoene oppdateres hvert 10.ende minutt."""
            if self.__checktime_for_exchange_code < time.time():
                self.__autorization_data = self.__exchange_code()
                self.__checktime_for_exchange_code = time.time() + self.__expires_in

            if self.__checktime_for_timer < time.time():
                self.__expires_in = self.__autorization_data["expires_in"]
                authorization_token = self.__autorization_data["access_token"]
                self.response = self.__get_data(authorization_token)

                """Hente data fra json-fila hentet fra Netatmo"""
                self.name_livingroom = self.response.json()["body"]["devices"][0]["module_name"]
                self.wifi_status_livingroom = self.response.json()["body"]["devices"][0]["wifi_status"]
                self.temp_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["Temperature"]
                self.tempmin_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["min_temp"]
                self.tempmax_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["max_temp"]
                self.temptrend_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["temp_trend"]
                self.co2_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["CO2"]
                self.humidity_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["Humidity"]
                self.noise_livingroom = self.response.json()["body"]["devices"][0]["dashboard_data"]["Noise"]
                self.pressure = self.response.json()["body"]["devices"][0]["dashboard_data"]["Pressure"]
                self.absolute_pressure = self.response.json()["body"]["devices"][0]["dashboard_data"]["AbsolutePressure"]
                self.pressure_trend = self.response.json()["body"]["devices"][0]["dashboard_data"]["pressure_trend"]

                self.name_outside = self.response.json()["body"]["devices"][0]["modules"][0]["module_name"]
                self.battery_percent_outside = self.response.json()["body"]["devices"][0]["modules"][0]["battery_percent"]
                self.temp_outside = self.response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["Temperature"]
                self.mintemp_outside = self.response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["min_temp"]
                self.maxtemp_outside = self.response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["max_temp"]
                self.humidity_outside = self.response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["Humidity"]
                self.temptrend_outside = self.response.json()["body"]["devices"][0]["modules"][0]["dashboard_data"]["temp_trend"]

                self.name_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["module_name"]
                self.battery_percent_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["battery_percent"]
                self.temp_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["Temperature"]
                self.mintemp_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["min_temp"]
                self.maxtemp_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["max_temp"]
                self.humidity_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["Humidity"]
                self.temptrend_bedroom = self.response.json()["body"]["devices"][0]["modules"][1]["dashboard_data"]["temp_trend"]

                self.online = True
                self.counter += 1
                """Setter timer for neste runde av oppdatering"""
                self.__checktime_for_timer = time.time() + int(self.__config["TIMERS"]["refresh"])

        except Exception as e:
            print(e)
            self.online = False

    def __exchange_code(self) -> json:
        data = {
            "client_id": self.__CLIENT_ID,
            "client_secret": self.__CLIENT_SECRET,
            "grant_type": "password",
            "username": self.__config["USERINFO"]["Username"],
            "password": self.__config["USERINFO"]["Password"],
            "redirect_uri": self.__REDIRECT_URI,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        r = requests.post(self.__API_ENDPOINT + "/oauth2/token", data=data, headers=headers)
        r.raise_for_status()
        return r.json()

    def __get_data(self, auth_token) -> requests:
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

        self.update_data()

    def update_data(self):
        if self.check_expired():
            self.counter += 1
            self.response = self.get_met_data()
            self.met_data = json.loads(self.response.text)
            self.expires = self.response.headers["Expires"]
            self.expires_print = self.get_time_from_expires()

        self.lufttrykk = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"]
        self.temperatur = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
        self.skydekning = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["cloud_area_fraction"]
        self.luftfuktighet = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"]
        self.vindretning = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"]
        self.vindhastighet = self.met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]
        self.neste_timen = self.met_data["properties"]["timeseries"][0]["data"]["next_1_hours"]["details"]["precipitation_amount"]
        self.neste_6_timer = self.met_data["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]

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


def main():
    weather = Netatmo()
    print(weather.response)
    weather.update_data()


if __name__ == "__main__":
    main()
