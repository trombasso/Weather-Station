from datetime import datetime
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from weather import Netatmo, Met_data
from getkey import getkey
import os

# import time
# from rich import print
# import json


"""
# from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
# from rich.syntax import Syntax
# from rich.text import Text
# import configparser
# import requests
# from os import name, system
# import os
"""

BOX_STYLE = "white on black"
OS_PATH = os.path.dirname(__file__)


console = Console()

try:
    netatmo_data = Netatmo()
except Exception as e:
    print(e)

try:
    bodo = Met_data(0, 67.28, 14.40)
    oslo = Met_data(50, 59.9, 10.44)
    misvaer = Met_data(0, 67.06, 15.00)
except Exception as e:
    print(e)

# def openfile(name):
#     try:
#         with open(file=os.path.join(OS_PATH, name, ".dat"), mode="rb") as file:
#     except FileNotFoundError:
#         pass
# def save2file(name):
#     pass


class Menu:
    def __rich__(self) -> Panel:
        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=2)
        n_line.add_column(style="white", justify="left", width=18)
        n_line.add_row("1)", "Options")
        n_line.add_row("2)", "Værmelding")
        n_line.add_row("3)", "Statistikk")
        # n_line.add_row("4)", "")
        # n_line.add_row("5)", "Menuitem")

        return Panel(
            Align.center(Group(n_line), vertical="top"),
            box=box.ROUNDED,
            padding=(4, 2),
            title="Menu",
            title_align="left",
            style=BOX_STYLE,
        )


class YR:
    def __rich__(self) -> Panel:
        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=2)
        n_line.add_column(style="white", justify="left", width=32)
        n_line.add_row("1)", "Bodø")
        n_line.add_row("2)", "Oslo")
        n_line.add_row("3)", "Misvær")
        # n_line.add_row("4)", "Tromsø")
        # n_line.add_row("5)", "Trondhjem")
        # n_line.add_row("6)", "Barcelona")
        # n_line.add_row("4)", "")
        # n_line.add_row("5)", "Menuitem")

        return Panel(
            Align.center(Group(n_line), vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="Menu",
            title_align="left",
            style=BOX_STYLE,
        )


class NetatmoLayout:
    def __rich__(self) -> Panel:
        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=18)
        n_line.add_column(style="white", justify="right", width=10)
        n_line.add_column(style="cyan", justify="left", width=6)

        n_line.add_row(f"{netatmo_data()['name_outside']}", style="cyan u b")
        n_line.add_row("Luftrykk:", str(netatmo_data()["pressure"]), " mbar")
        n_line.add_row("Temperatur:", str(netatmo_data()["temp_outside"]), " °c")
        n_line.add_row("Luftfuktighet", str(netatmo_data()["humidity_outside"]), " %")
        n_line.add_row("Temperaturtrend", str(netatmo_data()["temptrend_outside"]))

        n_line.add_row("")
        n_line.add_row(netatmo_data()["name_livingroom"], style="cyan u b")
        n_line.add_row("Temp: ", str(netatmo_data()["temp_livingroom"]), " °c")
        n_line.add_row("CO2: ", str(netatmo_data()["co2_livingroom"]), " ppm")
        n_line.add_row("Fuktighet: ", str(netatmo_data()["humidity_livingroom"]), " %")
        n_line.add_row("Støy: ", str(netatmo_data()["noise_livingroom"]), " dB")
        # n_line.add_row(datetime.now().ctime().replace(":", "[blink]:[/]"))

        n_line.add_row("")
        n_line.add_row(netatmo_data()["name_bedroom"], style="cyan u b")
        n_line.add_row("Temp", str(netatmo_data()["temp_bedroom"]), " °c")
        n_line.add_row("Luftfuktighet", str(netatmo_data()["humidity_bedroom"]), " %")
        n_line.add_row("Temp trend", str(netatmo_data()["temptrend_bedroom"]))
        n_line.add_row("")
        n_line.add_row("")
        # n_line.add_row("Online: ", str(netatmo_data()["online"]), style="grey37")

        return Panel(
            Align.center(Group(n_line), vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="Netatmo[grey37](N)[/grey37]",
            title_align="left",
            style=BOX_STYLE,
        )


class Bodo_YR:
    def __rich__(self) -> Panel:
        bodo()
        bodo_met_data = bodo.met_data

        i = len(bodo_met_data["properties"]["timeseries"])
        s = bodo_met_data["properties"]["timeseries"]

        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=19)
        n_line.add_column(style="white", justify="right", width=10)
        n_line.add_column(style="cyan", justify="left", width=6)

        n_line.add_row("Været nå", style="cyan b u")
        n_line.add_row("Lufttrykk: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"]), " mbar")
        n_line.add_row("Temperatur: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]), " °c")
        n_line.add_row("Skydekning: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["cloud_area_fraction"]), " %")
        n_line.add_row("Luftfuktighet: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"]), " %")
        n_line.add_row("Vindretning: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"]), " °")
        n_line.add_row("Hastighet: ", str(bodo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]), " m/s")

        t_line = Table.grid(padding=0)
        t_line.add_column(style="cyan", justify="left", width=18)
        t_line.add_column(style="white", justify="right", width=10)
        t_line.add_column(style="cyan", justify="left", width=6)

        t_line.add_row("")
        t_line.add_row("Nedbør", style="cyan b u")
        t_line.add_row("Neste timen:", str(bodo_met_data["properties"]["timeseries"][0]["data"]["next_1_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("Neste 6 timer:", str(bodo_met_data["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("")

        t_line.add_row("Langtidsvarsel:", style="cyan u b")

        m_line = Table.grid(padding=0)
        m_line.add_column(style="cyan b", width=7, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")

        m_line.add_row("", "1", "|", "2", "|", "3", "|", "4", style="cyan u")
        m_line.add_row(
            "T:",
            str(s[i - 29]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["air_temperature"]),
        )
        m_line.add_row(
            "V:",
            str(s[i - 29]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 29]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 25]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 21]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 17]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        m_line.add_row("", "5", "|", "6", "|", "7", "|", "8", style="cyan u")

        m_line.add_row(
            "T:",
            str(s[i - 13]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["air_temperature"]),
        )

        m_line.add_row(
            "V:",
            str(s[i - 13]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 13]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 9]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 5]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 1]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        e_line = Table.grid(padding=0)
        e_line.add_column(style="grey37", justify="right", width=34)
        e_line.add_row("")
        e_line.add_row(f"Neste update: {bodo.expires_print} GMT(-1)")

        return Panel(
            Align.center(Group(n_line, t_line, m_line, e_line), vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="Bodø",
            title_align="left",
            style=BOX_STYLE,
        )


class Misvaer_YR:
    def __rich__(self) -> Panel:
        misvaer()
        misvaer_met_data = misvaer.met_data

        i = len(misvaer_met_data["properties"]["timeseries"])
        s = misvaer_met_data["properties"]["timeseries"]

        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=19)
        n_line.add_column(style="white", justify="right", width=10)
        n_line.add_column(style="cyan", justify="left", width=6)

        n_line.add_row("Været nå", style="cyan b u")
        n_line.add_row("Lufttrykk: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"]), " mbar")
        n_line.add_row("Temperatur: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]), " °c")
        n_line.add_row("Skydekning: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["cloud_area_fraction"]), " %")
        n_line.add_row("Luftfuktighet: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"]), " %")
        n_line.add_row("Vindretning: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"]), " °")
        n_line.add_row("Hastighet: ", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]), " m/s")

        t_line = Table.grid(padding=0)
        t_line.add_column(style="cyan", justify="left", width=18)
        t_line.add_column(style="white", justify="right", width=10)
        t_line.add_column(style="cyan", justify="left", width=6)

        t_line.add_row("")
        t_line.add_row("Nedbør", style="cyan b u")
        t_line.add_row("Neste timen:", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["next_1_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("Neste 6 timer:", str(misvaer_met_data["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("")

        t_line.add_row("Langtidsvarsel:", style="cyan u b")

        m_line = Table.grid(padding=0)
        m_line.add_column(style="cyan b", width=7, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")

        m_line.add_row("", "1", "|", "2", "|", "3", "|", "4", style="cyan u")
        m_line.add_row(
            "T:",
            str(s[i - 29]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["air_temperature"]),
        )
        m_line.add_row(
            "V:",
            str(s[i - 29]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 29]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 25]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 21]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 17]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        m_line.add_row("", "5", "|", "6", "|", "7", "|", "8", style="cyan u")

        m_line.add_row(
            "T:",
            str(s[i - 13]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["air_temperature"]),
        )

        m_line.add_row(
            "V:",
            str(s[i - 13]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 13]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 9]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 5]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 1]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        e_line = Table.grid(padding=0)
        e_line.add_column(style="grey37", justify="right", width=34)
        e_line.add_row("")
        e_line.add_row(f"Neste update: {misvaer.expires_print} GMT(-1)")

        return Panel(
            Align.center(Group(n_line, t_line, m_line, e_line), vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="Misvær",
            title_align="left",
            style=BOX_STYLE,
        )


class Oslo_YR:
    def __rich__(self) -> Panel:
        oslo()
        oslo_met_data = oslo.met_data

        i = len(oslo_met_data["properties"]["timeseries"])
        s = oslo_met_data["properties"]["timeseries"]

        n_line = Table.grid(padding=0)
        n_line.add_column(style="cyan", justify="left", width=18)
        n_line.add_column(style="white", justify="right", width=10)
        n_line.add_column(style="cyan", justify="left", width=6)

        n_line.add_row("Været nå", style="cyan b u")
        n_line.add_row("Lufttrykk: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"]), " mbar")
        n_line.add_row("Temperatur: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]), " °c")
        n_line.add_row("Skydekning: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["cloud_area_fraction"]), " %")
        n_line.add_row("Luftfuktighet: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"]), " %")
        n_line.add_row("Vindretning: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"]), " °")
        n_line.add_row("Hastighet: ", str(oslo_met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"]), " m/s")

        t_line = Table.grid(padding=0)
        t_line.add_column(style="cyan", justify="left", width=18)
        t_line.add_column(style="white", justify="right", width=10)
        t_line.add_column(style="cyan", justify="left", width=6)

        t_line.add_row("")
        t_line.add_row("Nedbør", style="cyan b u")
        t_line.add_row("Neste timen:", str(oslo_met_data["properties"]["timeseries"][0]["data"]["next_1_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("Neste 6 timer:", str(oslo_met_data["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]), " mm")
        t_line.add_row("")
        t_line.add_row("Langtidsvarsel:", style="cyan u b")

        m_line = Table.grid(padding=0)
        m_line.add_column(style="cyan b", width=7, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")
        m_line.add_column(style="cyan", width=1, justify="center")
        m_line.add_column(width=6, justify="center")

        m_line.add_row("", "1", "|", "2", "|", "3", "|", "4", style="cyan u")
        m_line.add_row(
            "T:",
            str(s[i - 29]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["air_temperature"]),
        )
        m_line.add_row(
            "V:",
            str(s[i - 29]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 25]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 21]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 17]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 29]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 25]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 21]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 17]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        m_line.add_row("", "5", "|", "6", "|", "7", "|", "8", style="cyan u")

        m_line.add_row(
            "T:",
            str(s[i - 13]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["air_temperature"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["air_temperature"]),
        )

        m_line.add_row(
            "V:",
            str(s[i - 13]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 9]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 5]["data"]["instant"]["details"]["wind_speed"]),
            "|",
            str(s[i - 1]["data"]["instant"]["details"]["wind_speed"]),
        )

        # m_line.add_row(
        #     "R:",
        #     str(s[i - 13]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 9]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 5]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        #     "|",
        #     str(s[i - 1]["data"]["next_6_hours"]["details"]["precipitation_amount"]),
        # )

        e_line = Table.grid(padding=0)
        e_line.add_column(style="grey37", justify="right", width=34)
        e_line.add_row("")
        e_line.add_row(f"Neste update: {oslo.expires_print} GMT(-1)")

        return Panel(
            Align.center(Group(n_line, t_line, m_line, e_line), vertical="top"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="Oslo",
            title_align="left",
            style=BOX_STYLE,
        )


# def empty() -> Panel:
#     n_line = Table.grid(padding=0)
#     n_line.add_column(style="cyan", justify="left", width=18)
#     n_line.add_column(style="white", justify="right", width=10)
#     n_line.add_column(style="cyan", justify="left", width=6)

#     n_line.add_row("")

#     return Panel(
#         Align.center(Group(n_line), vertical="top"),
#         box=box.ROUNDED,
#         padding=(1, 2),
#         title="name",
#         title_align="left",
#         style=BOX_STYLE,
#     )


def make_layout() -> Layout:
    layout = Layout(name="root", size=100)

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", size=25),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="side", ratio=1),
        Layout(name="body", ratio=1),
    )

    # layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout


class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Været i Bodø[/b]",
            datetime.now().ctime(),
        )
        # replace(":", "[blink]:[/]")
        return Panel(grid, style=BOX_STYLE)


class Footer:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="right")
        # grid.add_row(str(netatmo_data()["counter"]), "[b]Sist oppdatert:[/b]", datetime.now().ctime())
        # grid.add_row(f"Online: {str(netatmo_data()['online'])}", f"Reloads: {str(netatmo_data()['counter'])}", style="grey37")
        grid.add_row(
            f"{'[dark_green]Online[/dark_green]' if (netatmo_data()['online']) else '[red]Offline[/red]'}",
            f"Reloads: {str(netatmo_data()['counter'])}/{str(bodo.counter)}",
            style="grey37",
        )
        return Panel(grid, style=BOX_STYLE)


if __name__ == "__main__":

    # Main Layout
    layout = make_layout()
    layout["header"].update(Header())
    layout["side"].update(NetatmoLayout())
    layout["body"].update(Bodo_YR())
    layout["footer"].update(Footer())

    try:
        with Live(layout, refresh_per_second=5, screen=True) as live:
            while True:
                a = getkey()
                if a == "m":
                    while True:
                        layout["body"].update(YR())

                        # Hovedmeny--------------------------------
                        a = getkey()
                        if a == "\x1b":
                            layout["body"].update(Bodo_YR())
                            break
                        elif a == "1":
                            layout["body"].update(Bodo_YR())
                            break
                        elif a == "2":
                            layout["body"].update(Oslo_YR())
                            break
                        elif a == "3":
                            layout["body"].update(Misvaer_YR())
                            break
                        elif a == "q":
                            exit()

                elif a == "q":
                    exit()

    except Exception as e:
        print(e)
