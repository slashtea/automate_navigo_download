#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbot
from base64 import b64decode
from os import rename
from datetime import datetime
from calendar import monthrange
import time
from shutil import move


def get_month_and_year(date, month_dict):
    month_number = date.month
    month_name = month_dict[month_number]
    return month_name, date.year


def get_monthly_subscription_certificate(date, month_dict, web, url, username,
                                         password):
    month, year = get_month_and_year(date, month_dict)
    number_of_days_in_month = monthrange(year, date.month)[1]

    # Login and navigate to certificate download page.
    web.go_to(url)
    web.type(username, into="username")
    web.type(b64decode(password).decode("utf-8"), into="Password",
             id="email-connect-error-dialog")
    web.click("Me Connecter", tag="span")
    web.click(id="compte-user-mon-espace-a-loop-1", tag="a")
    web.click("Mon attestation", tag="span")

    # Set start Date and year
    web.click(id="attestation_moisDebut", tag="select")
    web.click("1er {}".format(month),  tag="option")
    web.click(id="attestation_moisDebut", tag="select")
    web.click(id="attestation_anneeDebut", tag="select")
    web.click(str(year), tag="option")

    # Set end Date and year
    web.click(id="attestaition_moisFin", tag="select")
    web.click("{} {}".format(number_of_days_in_month, month),  tag="option")
    web.click(id="attestation_anneeFin", tag="select")
    web.click(str(year), tag="option")

    # Download
    web.click(id="actes-payment-attestation-txt-5", tag="button")
    time.sleep(5)

    web.driver.maximize_window()
    # Logout
    web.click(id="sel-base-nav-27", tag="a")
    web.quit()
    # web.click("Déconnexion", tag="span")

    return 0


def rename_pdf(file_path, month, year, first_name, last_name):
    rename(file_path + "/attestation.pdf", file_path +
           "attestation_navigo_{}_{}_{}_{}".format(month, year,
                                                   first_name, last_name))


def move_pdf(file_path, month, year, first_name, last_name, new_file_path=""):
    if new_file_path != "":
        move(file_path + "attestation_navigo_{}_{}_{}_{}"
             .format(month, year, first_name, last_name),
             new_file_path + "attestation_navigo_{}_{}_{}_{}"
             .format(month, year, first_name, last_name))


if __name__ == "__main__":
    date = datetime.now()
    web = webbot.Browser()
    navigo_url = "https://www.jegeremacartenavigo.fr/connexion/connexion"
    gmail_url = "https://mail.google.com/mail/u/0/#inbox"
    username = "ziyad.mestour@gmail.com"
    password = "XlNsYXNodGVhNGV2ZXIk"
    first_name = "ziyad"
    last_name = "mestour"
    file_path = "/home/shannon/Downloads/"
    # new_file_path = "/home/shannon/Documents/degetel/navigo/"
    new_file_path = ""

    month_number_name = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "aout",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre"
    }

    # Functions call.
    month, year = get_month_and_year(date, month_number_name)
    get_monthly_subscription_certificate(date, month_number_name, web,
                                         navigo_url, username, password)
    rename_pdf(file_path, month, date.year, first_name, last_name)
    move_pdf(file_path, month, date.year, first_name, last_name, new_file_path)
