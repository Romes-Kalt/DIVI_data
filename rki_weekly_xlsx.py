import pandas as pd
import numpy as np
import openpyxl
import datetime as dt
from selenium import webdriver
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
from ch405_t00ls.ch405_tools import list_items_to_string, date_of_next, change_last_modified
import codecs


pd.options.mode.chained_assignment = None  # avoid error message

COUNTIES = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',
            'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
            'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen', 'Gesamt']


# TODO UPDATE COMPLETE FILEPATH to your location
COMPLETE_FP = "C:/Users/YOUR_USER/YOUR_PROJECT_FOLDER/data/xlsx_data"
# TODO CHECK LINES 48, 61 & 399


def update_xlsx():
    # check last entry in csv is current date
    current_monday = None
    if dt.datetime.now().strftime('%A') != "Monday":
        for d in range(1, 7):
            if (dt.datetime.now() - dt.timedelta(d)).strftime("%A") == "Monday":
                current_monday = (dt.datetime.now() - dt.timedelta(d)).strftime("%Y_%m_%d")
    else:
        current_monday = dt.datetime.now().strftime("%Y_%m_%d")
    mod_time_since_epoc = os.path.getmtime(COMPLETE_FP+"/Fallzahlen_Kum_Tab_aktuell.xlsx")

    # Convert seconds since epoch to readable timestamp
    modification_time = time.strftime('%Y_%m_%d', time.localtime(mod_time_since_epoc))
    print(current_monday)
    if current_monday < modification_time:
        print(f"File is up to date (next update expected for "
              f"{dt.datetime.strftime(date_of_next('Monday'),'%Y_%m_%d')})")
        return False

    print("File will be updated...", end="")
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": COMPLETE_FP}

    options.add_experimental_option("prefs", prefs)
    # TODO Change to your chromedriver path
    chrome_driver_path = "C:/Users/YOUR_USER/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    driver.get("https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.html")
    time.sleep(2)
    driver.find_element_by_class_name("button.right.close").click()     # cookie window
    time.sleep(5)
    driver.find_element_by_class_name("more.downloadLink.InternalLink").click()  # xlsx-download
    time.sleep(5)
    os.remove(COMPLETE_FP+"/Fallzahlen_Kum_Tab_aktuell.xlsx")
    dest_dir = COMPLETE_FP
    new_name = f"Fallzahlen_Kum_Tab_aktuell.xlsx"
    # TODO CHANGE TO YOUR DOWNLOAD FOLDER
    current_file_name = "C:/Users/YOUR_USER/Downloads/Fallzahlen_Kum_Tab_aktuell.xlsx"
    os.rename(current_file_name, os.path.join(dest_dir, new_name))
    driver.close()
    print("Done.")
    return True


def seven_day_inci_lk(lk_lst: [list] = None, last_n_days: [int] = 14, add_min_max: [bool] = False):
    """creates line plot of all Landkreise in lk_lst (max is seven, is lk_lst contains more than seven entries, list
       will be reduced to the first seven entries) in the last_n_days from latest entry in Fallzahlen_Kum_Tab.xlsx
       provided by the RKI in Berlin, two lines for the Landkreise with the minimum and maximum incidence can be
       added"""
    colors = ["#110c29", "#0072b2", "#56b4e9", "#cc79a7", "#009e73", "#d55e00", "#e69f00", "#f0e442"]
    linestyles = [(0, (1, 1)), (0, (5, 3))]
    berlin_sk = ["SK Berlin Charlottenburg-Wilmersdorf", "SK Berlin Friedrichshain-Kreuzberg", "SK Berlin Lichtenberg",
                 "SK Berlin Marzahn-Hellersdorf", "SK Berlin Mitte", "SK Berlin Neukölln", "SK Berlin Pankow",
                 "SK Berlin Reinickendorf", "SK Berlin Spandau", "SK Berlin Steglitz-Zehlendorf",
                 "SK Berlin Tempelhof-Schöneberg", "SK Berlin Treptow-Köpenick"]

    if not lk_lst:
        lk_lst = ["SK Berlin Pankow"]
    if len(lk_lst) > 7:
        lk_lst = lk_lst[:7]
    min_inc = max_inc = 0
    last_day = ""
    timeframe_df = None
    complete_7d_inc = pd.read_excel(COMPLETE_FP+"/Fallzahlen_Kum_Tab_aktuell.xlsx",
                                    sheet_name="LK_7-Tage-Inzidenz (fixiert)",
                                    skiprows=lambda x: x not in range(4, 418))

    if add_min_max:
        last_col = complete_7d_inc[complete_7d_inc.columns[-1]]
        max_inc = round(last_col.max(), 2)
        max_inc_index = last_col[last_col == last_col.max()].index[0]
        min_inc = round(last_col.min(), 2)
        min_inc_index = last_col[last_col == last_col.min()].index[0]
        max_lk = complete_7d_inc.loc[[max_inc_index]]["LK"][max_inc_index]
        min_lk = complete_7d_inc.loc[[min_inc_index]]["LK"][min_inc_index]
        lk_lst.append(max_lk)
        lk_lst.append(min_lk)
    print(lk_lst)
    sns.set_style("darkgrid")
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75, top=0.85)
    col = 0
    linest = 0

    for lk in range(len(lk_lst)):
        this_lk = complete_7d_inc.loc[complete_7d_inc["LK"] == lk_lst[lk]].transpose()
        this_lk.drop(labels=["LK", "LKNR"], axis=0, inplace=True)
        this_lk["date"] = this_lk.index.astype(str)
        # TODO datum for prechange
        if len(this_lk) - last_n_days <= 149:  # dates for the 1st 149 entries does not have to be changed
            prechange_df = this_lk.loc[this_lk["date"].str.slice(start=0, stop=4) != "2021"]
            prechange_df["Datum"] = prechange_df["date"]
            postchange_df = this_lk.loc[this_lk["date"].str.slice(start=0, stop=4) == "2021"]
            this_lk = pd.concat([prechange_df, postchange_df])
        else:
            this_lk["Datum"] = this_lk["date"]
        last_day = this_lk["Datum"].iloc[-1]
        timeframe_df = this_lk.tail(last_n_days)
        timeframe_df.rename(columns={timeframe_df.columns[0]: "Inzidenz"}, inplace=True)
        if add_min_max:
            if lk < len(lk_lst)-2:
                ax1.plot(timeframe_df["Datum"], timeframe_df["Inzidenz"], color=colors[col],
                         linestyle=linestyles[linest], label=lk_lst[lk])
            else:
                if lk == len(lk_lst)-1:
                    label_txt = f"Min: {lk_lst[lk]} ({min_inc})"  # ({min_inc})"
                else:
                    label_txt = f"Max: {lk_lst[lk]} ({max_inc})"  # ({max_inc})"
                if len(label_txt) > 40:
                    lbl = label_txt.split(" ")
                    label_txt = lbl[0] + " " + lbl[1] + " " + lbl[2] + " " + "\n"
                    for _ in range(3, len(lbl)):
                        label_txt += lbl[_] + " "
                ax1.plot(timeframe_df["Datum"], timeframe_df["Inzidenz"], color="black", linestyle=(0, (2, 4)),
                         label=label_txt)
        else:
            ax1.plot(timeframe_df["Datum"], timeframe_df["Inzidenz"], color=colors[col], linestyle=linestyles[linest],
                     label=lk_lst[lk])
        linest = 1 if col % 2 == 0 else 0
        col += 1
    plt.legend(loc=(1, .54), fontsize=10)
    quelle = '\n\nQuelle: Robert Koch Institut\n' \
             'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.html'
    x_axis_title = "Datum"+quelle
    ax1.set_xlabel(x_axis_title, fontsize=12)
    y_axis_title = "Sieben Tage Inzidenz"
    ax1.set_ylabel(y_axis_title, fontsize=12)
    if len(timeframe_df["Datum"]) > 31:
        plt.xticks(np.arange(0, len(timeframe_df["Datum"]), int(len(timeframe_df["Datum"]) / 40)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')
    if add_min_max:
        title_txt = ""
        if len(list_items_to_string(lk_lst[:-2])) > 75:
            title1 = list_items_to_string(lk_lst[:-2]).split(",")
            for _ in range(len(title1)):
                title_txt += title1[_] + ", "
                if _ == (len(title1) // 2):
                    title_txt += "\n"
            title_txt = title_txt[:-2]
        else:
            title_txt = f"{list_items_to_string(lk_lst[:-2])}"
        title_txt += f"\nin den letzten {last_n_days} Tagen (Stand: {last_day}, nächstes Update erwartet am " \
                     f"{dt.datetime.strftime(date_of_next('Monday'),'%d.%m.%Y')})"
        title_txt += "\nim Vergleich zu der kleinsten und größten gemeldeten Inzidenz"
    else:
        title_txt = ""
        if len(list_items_to_string(lk_lst)) > 75:
            title1 = list_items_to_string(lk_lst).split(",")
            for _ in range(len(title1)):
                title_txt += title1[_] + ", "
                if _ == (len(title1) // 2):
                    title_txt += "\n"
            title_txt = title_txt[:-2]
        else:
            title_txt = f"{list_items_to_string(lk_lst)}"
        title_txt += f"\nin den letzten {last_n_days} Tagen (Stand: {last_day}, nächstes Update erwartet am " \
                     f"{dt.datetime.strftime(date_of_next('Monday'),'%d.%m.%Y')})"
    plt.title(title_txt, fontsize=14)

    if add_min_max:
        filename = f"./data/xlsx_data/plots/{'_'.join(list(last_day.split('.'))[::-1])}_inc_of_{len(lk_lst)-2}lk(__" \
                   f"{lk_lst[0][-10:]})_{last_n_days}_last_days_minmax.png"
    else:
        filename = f"./data/xlsx_data/plots/{'_'.join(list(last_day.split('.'))[::-1])}_inc_of_{len(lk_lst)}lk(__" \
                   f"{lk_lst[0][-10:]})_{last_n_days}_last_days.png"

    plt.savefig(filename)

    if input("Show plots? (y/n) ").lower() != "n":
        plt.show()


def seven_day_inci_bl(bl_lst: [list] = None, last_n_days: [int] = 14, incl_all: [bool] = False,
                      incl_min_max: [bool] = True):
    """creates line plot of all Bundesländer or selected ones in bl_lst in the last_n_days from latest entry in
       Fallzahlen_Kum_Tab.xlsx provided by the RKI in Berlin"""
    bl_styles = {
        "Baden-Württemberg": {"col": "#0072b2", "sty": (0, (1, 2))},
        "Bayern": {"col": "#cc79a7", "sty": (0, (1, 2))},
        "Berlin": {"col": "#d55e00", "sty": (0, (1, 2))},
        "Brandenburg": {"col": "#f0e442", "sty": (0, (1, 2))},
        
        "Bremen": {"col": "#0072b2", "sty": (0, (5, 3))},
        "Hamburg": {"col": "#cc79a7", "sty": (0, (5, 3))},
        "Hessen": {"col": "#d55e00", "sty": (0, (5, 3))},
        "Mecklenburg-Vorpommern": {"col": "#f0e442", "sty": (0, (5, 3))},
        
        "Niedersachsen": {"col": "#0072b2", "sty": (0, (3, 1, 1, 1, 1, 1))},
        "Nordrhein-Westfalen": {"col": "#cc79a7", "sty": (0, (3, 1, 1, 1, 1, 1))},
        "Rheinland-Pfalz": {"col": "#d55e00", "sty": (0, (3, 1, 1, 1, 1, 1))},
        "Saarland": {"col": "#f0e442", "sty": (0, (3, 1, 1, 1, 1, 1))},

        "Sachsen": {"col": "#0072b2", "sty": (0, (5, 1, 1, 1, 1, 1, 1, 5))},
        "Sachsen-Anhalt": {"col": "#cc79a7", "sty": (0, (5, 1, 1, 1, 1, 1, 1, 5))},
        "Schleswig-Holstein": {"col": "#d55e00", "sty": (0, (5, 1, 1, 1, 1, 1, 1, 5))},
        "Thüringen": {"col": "#f0e442", "sty": (0, (5, 1, 1, 1, 1, 1, 1, 5))},
                                         
        "Gesamt": {"col": "black", "sty": "solid"},
    }
    if bl_lst:
        for _ in bl_lst:
            if _ not in COUNTIES:
                print("Misspelled / Wrong County (Bundesland):", _)
                bl_lst.remove(_)
        if len(bl_lst) == 0:
            print("No valid entry in County (Bundesland) list, data for all counties will be plotted.")
    if not bl_lst:
        bl_lst = list(bl_styles.keys())
        pick_bl = False  # for filename attachment
    else:
        if incl_all and "Gesamt" not in bl_lst:
            bl_lst.append("Gesamt")
        pick_bl = True  # for filename attachment
    if type(last_n_days) != int or last_n_days < 1:
        print(f"---\nValue < {last_n_days} > for the last n days is not valid, will be set to 28.")
        last_n_days = 28

    complete_7d_inc = pd.read_excel("./data/xlsx_data/Fallzahlen_Kum_Tab_aktuell.xlsx",
                                    sheet_name="BL_7-Tage-Inzidenz (fixiert)",
                                    skiprows=lambda x: x not in range(4, 22))


    complete_7d_inc.rename(columns={complete_7d_inc.columns[0]: "Datum"}, inplace=True)

    complete_7d_inc = complete_7d_inc.transpose()

    complete_7d_inc["date"] = complete_7d_inc.index.astype(str)

    ## changed after 08.02.2022, kept for further reference
    # complete_7d_inc["Datum"] = (complete_7d_inc["date"].str.split("-").str[2].str.slice(0, 2) + "."
    #                             + complete_7d_inc["date"].str.split("-").str[1] + "."
    #                             + complete_7d_inc["date"].str.split("-").str[0]).astype(str)
    # complete_7d_inc.at["Datum", "Datum"] = "Datum"  # set empty space for making new header later
    complete_7d_inc.reset_index(drop=True, inplace=True)

    # move "Datum" column (last) to front
    cols = list(complete_7d_inc.columns)
    cols = [cols[-1]] + cols[:-1]

    complete_7d_inc = complete_7d_inc[cols]
    new_header = complete_7d_inc.iloc[0]  # grab the first row for the header
    complete_7d_inc = complete_7d_inc[1:]  # take the data less the header row
    complete_7d_inc.columns = new_header  # set the header row as the df header

    if last_n_days > len(complete_7d_inc):
        last_n_days = len(complete_7d_inc)
    timeframe_df = complete_7d_inc.tail(last_n_days)
    # print(bl_lst)

    # sns.set_style("whitegrid", {'axes.grid': False})
    sns.set_context("paper", font_scale=0.8)  # font scale lowered to avoid overlapping x-ticks
    fig, ax1 = plt.subplots(figsize=(11, 8))  # initializes figure and plots
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.74, top=0.85)
    last_day = timeframe_df["Datum"].iloc[-1]

    for bl in bl_lst:
        if bl in COUNTIES:
            if incl_min_max:
                this_label = f"{bl} " + "\n" + f"({round(timeframe_df[bl].min(), 1)}" \
                                               f" - {round(timeframe_df[bl].max(), 1)})"
            else:
                this_label = bl
            ax1.plot(timeframe_df["Datum"], timeframe_df[bl],
                     color=bl_styles[bl]["col"], linestyle=bl_styles[bl]["sty"], label=this_label)
        else:
            print("Following County/Bundesland not found: ", bl, ".")
    if incl_min_max:
        plt.legend(loc=(1, -.10), fontsize=9)
    else:
        plt.legend(loc=(1, .30), fontsize=10)
    quelle = '\n\nQuelle: Robert Koch Institut\n' \
             'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.html'
    x_axis_title = "Datum"+quelle
    ax1.set_xlabel(x_axis_title, fontsize=12)
    ax1.yaxis.grid()
    ax1.set_facecolor("#f2f4ff")
    y_axis_title = "Sieben Tage Inzidenz"
    ax1.set_ylabel(y_axis_title, fontsize=12)
    plt.title(f"Sieben Tage Inzidenz in den letzten {last_n_days} Tagen\nStand: {last_day} "
              f"\n(nächstes Update erwartet am {dt.datetime.strftime(date_of_next('Monday'),'%d.%m.%Y')})", fontsize=14)

    if len(timeframe_df["Datum"]) > 31:
        plt.xticks(np.arange(0, len(timeframe_df["Datum"]), int(len(timeframe_df["Datum"]) / 40)))
    fig.autofmt_xdate(bottom=0.2, rotation=70, ha='center')

    if pick_bl:
        filename = f"{COMPLETE_FP}/plots/" \
                   f"{'_'.join(list(last_day.split('.'))[::-1])}_inc_of_{len(bl_lst)}_bl_last_" \
                   f"{last_n_days}days.png"
    else:
        filename = f"{COMPLETE_FP}/plots/" \
                   f"{'_'.join(list(last_day.split('.'))[::-1])}_inc_of_ALL_bl_last_" \
                   f"{last_n_days}days.png"

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    plt.savefig(filename)

    if input("Show plots? (y/n) ").lower() != "n":
        plt.show()


def create_lk_file(separator: [str] = ":",
                   file_name: [str] = COMPLETE_FP+"/lk_list.txt"):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print(f"The file <{file_name}> will be created.")
    else:
        print(f"The file <{file_name}> will be replaced.")

    complete_7d_inc = pd.read_excel("./data/xlsx_data/Fallzahlen_Kum_Tab_aktuell.xlsx",
                                    sheet_name="LK_7-Tage-Inzidenz (fixiert)",
                                    skiprows=lambda x: x not in range(4, 416))
    lk_nummer = complete_7d_inc["NR"].tolist()
    lk_name = complete_7d_inc["LK"].tolist()
    for _ in range(len(lk_nummer)):
        with codecs.open(file_name, "a+", encoding="utf-8") as f:
            f.write(f"{lk_nummer[_]}{separator}{lk_name[_]}\n")


def create_bl_file(file_name: [str] = COMPLETE_FP+"/bl_list.txt"):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print(f"The file <{file_name}> will be created.")
    else:
        print(f"The file <{file_name}> will be replaced.")

    complete_7d_inc = pd.read_excel("./data/xlsx_data/Fallzahlen_Kum_Tab_aktuell.xlsx",
                                    sheet_name="BL_7-Tage-Inzidenz (fixiert)",
                                    skiprows=lambda x: x not in range(2, 20))
    complete_7d_inc.rename(columns={complete_7d_inc.columns[0]: "BL"}, inplace=True)

    bl_lst = complete_7d_inc["BL"].tolist()
    for _ in range(len(bl_lst)):
        with codecs.open(file_name, "a+", encoding="utf-8") as f:
            f.write(f"{bl_lst[_]}\n")


def user_choice_lk():
    """let's user choose from all Landkreise and returns list of these LK's"""
    with codecs.open("./data/xlsx_data/lk_list.txt", encoding="utf-8") as f:
        all_lk_raw = f.readlines()
    all_lk = [lk.split(":")[1].strip() for lk in all_lk_raw]
    user_search = input("Ort: ").lower()
    user_results = [lk for lk in all_lk if user_search in lk.lower()]
    sel = []
    if user_results:
        if len(user_results) > 1:
            for i in range(len(user_results)):
                print(f"{(i+1):2d}: {user_results[i]}")
            while not sel:
                sel_in = input("\n---\nBitte Auswahl treffen (getrennt durch Leerzeichen, max 8): ").\
                    replace(",", " ").replace(".", " ").replace("-", " ").replace("/", " ").replace("+", " ")
                for s in sel_in.split(" "):
                    try:
                        int(s)
                    except ValueError:
                        pass
                    else:
                        if 0 < int(s) <= len(user_results) and user_results[int(s)-1] not in sel:
                            sel.append(user_results[int(s)-1])
                if sel:
                    complete = True
        else:
            sel.append(user_results[0])
    return sel


if __name__ == "__main__":
    # TODO uncomment on first run
    # create_lk_file()
    # create_bl_file()
    if input("update file? (y/n) ").lower() == "y":
        update_xlsx()
    #
    # seven_day_inci(lk_lst=["SK Berlin Pankow", "SK Berlin Friedrichshain-Kreuzberg", "SK Berlin Mitte",
    #                        "SK Berlin Treptow-Köpenick", "SK Berlin Tempelhof-Schöneberg", "SK Berlin Lichtenberg",
    #                        "SK Berlin Steglitz-Zehlendorf"], last_n_days=100, add_min_max=False)

    seven_day_inci_bl(last_n_days=1500, incl_all=True)
    seven_day_inci_bl(last_n_days=100, incl_all=True, incl_min_max=True)
    # seven_day_inci_bl(last_n_days=1_000, incl_all=True, incl_min_max=False)

    seven_day_inci_bl(bl_lst=["Berlin", "Bayern", "Sachsen", "Thüringen"],
                      last_n_days=28, incl_all=True, incl_min_max=True)
    seven_day_inci_lk(["SK Berlin Pankow", "SK Berlin Friedrichshain-Kreuzberg"], 28, True)

    # user_ch = user_choice_lk()
    # seven_day_inci_lk(user_ch, 28, True)

