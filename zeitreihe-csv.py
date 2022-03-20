import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
import time
import os
import datetime as dt


COMPLETE_FP = "C:/Users/YOUR_USER/YOUR_PROJECT_FOLDER/csv_data"
# TODO: Check line 135


def plot_aktuelle_covid_faelle_its():
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks

    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()

    ax1.plot(adult_complete["Datum"], adult_complete["Aktuelle_COVID_Faelle_ITS"], color=adult_color,
             label="Erwachsene")  # {DEPARR} per day
    ax2.plot(adult_complete["Datum"], child_complete["Aktuelle_COVID_Faelle_ITS"], color=child_color, label="Kinder")
    for label in ax2.get_yticklabels():
        label.set_color(adult_color)
    ax1.spines['left'].set_color(adult_color)
    ax1.spines['left'].set_linewidth(3)
    ax2.spines['right'].set_color(child_color)
    ax2.spines['right'].set_linewidth(3)
    ax1.tick_params(axis='y', colors=adult_color)
    ax2.tick_params(axis='y', colors=child_color)
    ax1.set_xlabel(f"Date", fontsize=12)
    ax1.set_ylabel(f"Erwachsene", color=adult_color, fontsize=12)
    ax2.set_ylabel(f"Kinder", color=child_color, fontsize=12)
    if len(adult_complete["Datum"]) > 31:
        plt.xticks(np.arange(0, len(adult_complete["Datum"]), int(len(adult_complete["Datum"]) / 31)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
    plt.title("Aktuelle Covid-Fälle ITS", fontsize=16)
    plt.show()


def plot_belegte_intensivbetten():
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks

    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()

    ax1.plot(adult_complete["Datum"], adult_complete["Belegte_Intensivbetten"], color=adult_color,
             label="Erwachsene")  # {DEPARR} per day
    ax2.plot(adult_complete["Datum"], child_complete["Belegte_Intensivbetten"], color=child_color, label="Kinder")
    for label in ax2.get_yticklabels():
        label.set_color(adult_color)
    ax1.spines['left'].set_color(adult_color)
    ax1.spines['left'].set_linewidth(3)
    ax2.spines['right'].set_color(child_color)
    ax2.spines['right'].set_linewidth(3)
    ax1.tick_params(axis='y', colors=adult_color)
    ax2.tick_params(axis='y', colors=child_color)
    ax1.set_xlabel(f"Date", fontsize=12)
    ax1.set_ylabel(f"Erwachsene", color=adult_color, fontsize=12)
    ax2.set_ylabel(f"Kinder", color=child_color, fontsize=12)
    if len(adult_complete["Datum"]) > 31:
        plt.xticks(np.arange(0, len(adult_complete["Datum"]), int(len(adult_complete["Datum"]) / 31)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
    plt.title("Belegte Intensivbetten", fontsize=16)
    plt.show()


def plot_freie_intensivbetten():
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks

    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()

    ax1.plot(adult_complete["Datum"], adult_complete["Freie_Intensivbetten"], color=adult_color,
             label="Erwachsene")  # {DEPARR} per day
    ax2.plot(adult_complete["Datum"], child_complete["Freie_Intensivbetten"], color=child_color, label="Kinder")
    for label in ax2.get_yticklabels():
        label.set_color(adult_color)
    ax1.spines['left'].set_color(adult_color)
    ax1.spines['left'].set_linewidth(3)
    ax2.spines['right'].set_color(child_color)
    ax2.spines['right'].set_linewidth(3)
    ax1.tick_params(axis='y', colors=adult_color)
    ax2.tick_params(axis='y', colors=child_color)
    ax1.set_xlabel(f"Date", fontsize=12)
    ax1.set_ylabel(f"Erwachsene", color=adult_color, fontsize=12)
    ax2.set_ylabel(f"Kinder", color=child_color, fontsize=12)
    if len(adult_complete["Datum"]) > 31:
        plt.xticks(np.arange(0, len(adult_complete["Datum"]), int(len(adult_complete["Datum"]) / 31)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
    plt.title("Freie Intensivbetten", fontsize=16)
    plt.show()


def plot_7_tage_notfallreserve():
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks

    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    ax2 = ax1.twinx()

    ax1.plot(adult_complete["Datum"], adult_complete["7_Tage_Notfallreserve"], color=adult_color,
             label="Erwachsene")  # {DEPARR} per day
    ax2.plot(adult_complete["Datum"], child_complete["7_Tage_Notfallreserve"], color=child_color, label="Kinder")
    for label in ax2.get_yticklabels():
        label.set_color(adult_color)
    ax1.spines['left'].set_color(adult_color)
    ax1.spines['left'].set_linewidth(3)
    ax2.spines['right'].set_color(child_color)
    ax2.spines['right'].set_linewidth(3)
    ax1.tick_params(axis='y', colors=adult_color)
    ax2.tick_params(axis='y', colors=child_color)
    ax1.set_xlabel(f"Date", fontsize=12)
    ax1.set_ylabel(f"Erwachsene", color=adult_color, fontsize=12)
    ax2.set_ylabel(f"Kinder", color=child_color, fontsize=12)
    if len(adult_complete["Datum"]) > 31:
        plt.xticks(np.arange(0, len(adult_complete["Datum"]), int(len(adult_complete["Datum"]) / 31)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
    plt.title("7 Tage Notfallreserve", fontsize=16)
    plt.show()


def update_csv():
    # check last entry in csv is current date
    if dt.datetime.now().strftime('%Y_%m_%d') != last_date:
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": COMPLETE_FP}

        options.add_experimental_option("prefs", prefs)

        # TODO Insert your chromedriver path
        chrome_driver_path = "C:/Users/YOUR_USER/chromedriver_win32/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver_path)

        driver.get("https://www.intensivregister.de/#/aktuelle-lage/downloads")
        time.sleep(2)
        # check, whether csv file was updated for current date
        tds = driver.find_elements_by_css_selector("td")
        if dt.datetime.now().strftime('%d.%m.%Y') == tds[27].text.split(" ")[0]:
            buttons = driver.find_elements_by_class_name("mat-icon.notranslate.material-icons.mat-icon-no-color")
            buttons[4].click()
            time.sleep(5)
            driver.close()
            os.remove("./data/csv_data/zeitreihe-deutschland.csv")
            dest_dir = COMPLETE_FP
            new_name = f"zeitreihe-deutschland.csv"
            current_file_name = "C:/Users/roman/Downloads/zeitreihe-deutschland.csv"
            os.rename(current_file_name, os.path.join(dest_dir, new_name))
            return True
        else:
            print(f"No updated csv-file for {dt.datetime.now().strftime('%d.%m.%Y')} "
                  f"published yet ({dt.datetime.strftime(dt.datetime.now(), '%H:%M')})")
            if input("Update anyway? (Y/n) ") == "Y":
                buttons = driver.find_elements_by_class_name("mat-icon.notranslate.material-icons.mat-icon-no-color")
                buttons[4].click()
                time.sleep(5)
                driver.close()
                os.remove("./data/csv_data/zeitreihe-deutschland.csv")
                dest_dir = COMPLETE_FP
                new_name = f"zeitreihe-deutschland.csv"
                current_file_name = "C:/Users/roman/Downloads/zeitreihe-deutschland.csv"
                os.rename(current_file_name, os.path.join(dest_dir, new_name))
                return True
            return False
    else:
        print("File already updated.")
        return False


def generate_all_plots():
    categories = ["Aktuelle_COVID_Faelle_ITS", "Belegte_Intensivbetten",
                  "Freie_Intensivbetten", "7_Tage_Notfallreserve",
                  "Freie_IV_Kapazitaeten_Gesamt", "Freie_IV_Kapazitaeten_Davon_COVID"]

    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks

    for cat in categories:
        fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
        ax2 = ax1.twinx()
        ax1.plot(adult_complete["Datum"], adult_complete[cat], color=adult_color,
                 label="Erwachsene")
        ax2.plot(adult_complete["Datum"], child_complete[cat], color=child_color, label="Kinder")
        for label in ax2.get_yticklabels():
            label.set_color(adult_color)
        ax1.spines['left'].set_color(adult_color)
        ax1.spines['left'].set_linewidth(3)
        ax2.spines['right'].set_color(child_color)
        ax2.spines['right'].set_linewidth(3)
        ax1.tick_params(axis='y', colors=adult_color)
        ax2.tick_params(axis='y', colors=child_color)
        ax1.set_xlabel(f"Date", fontsize=12)
        ax1.set_ylabel(f"Erwachsene", color=adult_color, fontsize=12)
        ax2.set_ylabel(f"Kinder", color=child_color, fontsize=12)
        if len(adult_complete["Datum"]) > 31:
            plt.xticks(np.arange(0, len(adult_complete["Datum"]), int(len(adult_complete["Datum"]) / 40)))
        fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
        plt.title(f"{cat.replace('_', ' ').replace('ae', 'ä')}\n"
                  f"{file_in_timeframe['Datum'].iloc[0]} - {file_in_timeframe['Datum'].iloc[-1]}", fontsize=16)
        filename_backup = f"./plots/csv_plots/history/{start_date}-{end_date}_{cat}.png"
        filename = f"./plots/csv_plots/{cat}.png"
        # os.remove(filename)
        plt.savefig(filename_backup)
        # filename = fr"C:\Users\roman\Python\PyCharmProjects\divi_tracker\plots\csv_plots\{cat}.png"
        # change_last_modified(filename, dt.datetime.now())
        plt.savefig(filename)
    if input("Show plots? (y/n) ").lower() == "y":
        plt.show()


if __name__ == "__main__":

    complete_file = pd.read_csv(
        f"{COMPLETE_FP}/zeitreihe-deutschland.csv", encoding="cp1252")
    # change timestamp data into date DD.MM.YYYY
    complete_file["Datum"] = (complete_file["Datum"].str.split("T").str[0].str.split("-").str[2] + "."
                              + complete_file["Datum"].str.split("T").str[0].str.split("-").str[1] + "."
                              + complete_file["Datum"].str.split("T").str[0].str.split("-").str[0])
    # create date_keys YYYY_MM_DD for date filtering
    complete_file["date_key"] = (complete_file["Datum"].str.split(".").str[-1] + "_"
                                 + complete_file["Datum"].str.split(".").str[1] + "_"
                                 + complete_file["Datum"].str.split(".").str[0]).astype(str)

    # ##### CHOOSE DATE OTIONS #####
    # complete
    start_date = "2020_03_20"
    end_date = dt.datetime.now().strftime("%Y_%m_%d")

    # specific
    # start_date = "2021_10_01"
    # end_date = "2021_06_30"

    # last n days
    # last_n_days = 14
    # start_date = (dt.datetime.now() - dt.timedelta(days=last_n_days)).strftime('%Y_%m_%d')
    # end_date = dt.datetime.now().strftime("%Y_%m_%d")
    # # ##### END OF DATE OPTIONS #####

    file_in_timeframe = complete_file[
        (complete_file["date_key"] >= start_date) & (complete_file["date_key"] <= end_date)]

    last_dates = file_in_timeframe["Datum"].iloc[-1].split(".")
    last_date = last_dates[2] + "_" + last_dates[1] + "_" + last_dates[0]

    if update_csv():    # returns True, if update was done -> re-read the file to include new data
        # change timestamp data into date DD.MM.YYYY
        complete_file = pd.read_csv(
            f"{COMPLETE_FP}/zeitreihe-deutschland.csv", encoding="cp1252")
        complete_file["Datum"] = (complete_file["Datum"].str.split("T").str[0].str.split("-").str[2] + "."
                                  + complete_file["Datum"].str.split("T").str[0].str.split("-").str[1] + "."
                                  + complete_file["Datum"].str.split("T").str[0].str.split("-").str[0])
        # create date_keys YYYY_MM_DD for date filtering
        complete_file["date_key"] = (complete_file["Datum"].str.split(".").str[-1] + "_"
                                     + complete_file["Datum"].str.split(".").str[1] + "_"
                                     + complete_file["Datum"].str.split(".").str[0]).astype(str)
        file_in_timeframe = complete_file[
            (complete_file["date_key"] >= start_date) & (complete_file["date_key"] <= end_date)]
        last_dates = file_in_timeframe["Datum"].iloc[-1].split(".")
        last_date = last_dates[2] + "_" + last_dates[1] + "_" + last_dates[0]
        print("zeitreihe-deutschland.csv updated")

    adult_complete = file_in_timeframe.query(f"Behandlungsgruppe == 'ERWACHSENE'")
    child_complete = file_in_timeframe.query("Behandlungsgruppe == 'KINDER'")
    adult_color = "#3f3351"
    child_color = "#e9a6a6"
    generate_all_plots()
