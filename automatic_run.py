import io
import os
import requests
import datetime as dt
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage

# TODO change your credentials here
USER = os.environ.get("DIVI_MAIL")
PASSWORD = os.environ.get("DIVI_MAIL_PASSWD")
TO_ADDR = os.environ.get("ROKA_GOOGLM")


def bundesland_belegung(county_nums: [dict] = None):
    """returns dictionary of county with respective report status ['KEINE_ANGABE', 'VERFUEGBAR', 'BEGRENZT',
       'NICHT_VERFUEGBAR'] of each hospital (name = key)"""
    if not county_nums:
        return "No Numbers received"
    betten_einschatzung = {
        "ecmo_total": 0,
        "ecmo_availbl": 0,
        "ecmo_limited": 0,
        "ecmo_unavaib": 0,
        "hicare_total": 0,
        "hicare_availbl": 0,
        "hicare_limited": 0,
        "hicare_unavaib": 0,
        "locare_total": 0,
        "locare_availbl": 0,
        "locare_limited": 0,
        "locare_unavaib": 0,
    }
    for kh in county_nums:
        # total number of type
        if county_nums[kh]["ecmo"] != "KEINE_ANGABE":
            betten_einschatzung["ecmo_total"] += 1
        if county_nums[kh]["hicare"] != "KEINE_ANGABE":
            betten_einschatzung["hicare_total"] += 1
        if county_nums[kh]["locare"] != "KEINE_ANGABE":
            betten_einschatzung["locare_total"] += 1
        # add respective numbers, if estimate was given (!= KEINE_ANGABE)
        if county_nums[kh]["ecmo"] == "VERFUEGBAR":
            betten_einschatzung["ecmo_availbl"] += 1
        elif county_nums[kh]["ecmo"] == "BEGRENZT":
            betten_einschatzung["ecmo_limited"] += 1
        elif county_nums[kh]["ecmo"] == "NICHT_VERFUEGBAR":
            betten_einschatzung["ecmo_unavaib"] += 1
        if county_nums[kh]["hicare"] == "VERFUEGBAR":
            betten_einschatzung["hicare_availbl"] += 1
        elif county_nums[kh]["hicare"] == "BEGRENZT":
            betten_einschatzung["hicare_limited"] += 1
        elif county_nums[kh]["hicare"] == "NICHT_VERFUEGBAR":
            betten_einschatzung["hicare_unavaib"] += 1
        if county_nums[kh]["locare"] == "VERFUEGBAR":
            betten_einschatzung["locare_availbl"] += 1
        elif county_nums[kh]["locare"] == "BEGRENZT":
            betten_einschatzung["locare_limited"] += 1
        elif county_nums[kh]["locare"] == "NICHT_VERFUEGBAR":
            betten_einschatzung["locare_unavaib"] += 1
    return betten_einschatzung


def report_status(lang: [str] = "eng"):
    """statistics for divided in weekdays or weekends"""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend = ["Saturday", "Sunday"]
    if dt.datetime.now().strftime("%A") in weekdays:
        if lang.lower() in ["deu", "ger", "deutsch", "german"]:
            day_category = "Werktags"
        else:
            day_category = "On weekdays"
    else:
        if lang.lower() in ["deu", "ger", "deutsch", "german"]:
            day_category = "An Wochenden"
        else:
            day_category = "On weekdends"
    with open("./data/reporting_tracker.csv") as f:
        file_contents = f.readlines()
    weekday = weekdays if dt.datetime.now().strftime("%A") in weekdays else weekend
    time_window = (weekday,
                   f"{(int(dt.datetime.now().strftime('%H:%M').split(':')[0]) - 1):02d}:"
                   f"{dt.datetime.now().strftime('%H:%M').split(':')[1]}",
                   f"{(int(dt.datetime.now().strftime('%H:%M').split(':')[0]) + 1):02d}:"
                   f"{dt.datetime.now().strftime('%H:%M').split(':')[1]}")
    percentages = []
    missing = []
    this_date = ""
    for entry in file_contents[1:]:
        # print(entry)
        if entry.split(",")[1] in weekday and time_window[1] < entry.split(",")[2] < time_window[2]:
            if entry.split(",")[0] == this_date:
                continue
            else:
                this_date = entry.split(",")[0]
            percentages.append(float(entry.split(",")[3].replace(",", ".")))
            missing.append(int(entry.split(",")[4]))
    if len(missing) >= 2:
        if lang.lower() in ["deu", "ger", "deutsch", "german"]:
            return (True,
                    f"{day_category} um {dt.datetime.now().strftime('%H:%M')} Uhr "
                    f"(± eine Stunde) liegt der Meldestatus durchschnittlich bei "
                    f"{round(100 - (sum(percentages) / len(percentages)), 2)} Prozent\n (d.h. die Meldung von "
                    f"{sum(missing) // len(missing)} Krankenhäusern steht noch aus).")
        else:
            return (True,
                    f"{day_category} at {dt.datetime.now().strftime('%H:%M')} "
                    f"(± one hour) the average reporting status is {round(sum(percentages) / len(percentages), 2)} %"
                    f" (meaning {sum(missing) // len(missing)} hospitals missing).")
    else:
        return False, "No sufficient data for average reporting status."


def report_status1(lang: [str] = "eng"):
    if lang.lower() in ["deu", "ger", "deutsch", "german"]:
        weekdays_ger = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag",
        }
    else:
        weekdays_ger = None
    with open("./data/reporting_tracker.csv") as f:
        file_contents = f.readlines()
    time_window = (dt.datetime.now().strftime("%A"),
                   f"{int(dt.datetime.now().strftime('%H:%M').split(':')[0]) - 1}:"
                   f"{dt.datetime.now().strftime('%H:%M').split(':')[1]}",
                   f"{int(dt.datetime.now().strftime('%H:%M').split(':')[0]) + 1}:"
                   f"{dt.datetime.now().strftime('%H:%M').split(':')[1]}")
    percentages = []
    missing = []
    this_date = ""
    for entry in file_contents[1:]:
        if entry.split(",")[1] == time_window[0] and time_window[1] < entry.split(",")[2] < time_window[2]:
            if entry.split(",")[0] == this_date:
                continue
            else:
                this_date = entry.split(",")[0]
            percentages.append(float(entry.split(",")[3].replace(",", ".")))
            missing.append(int(entry.split(",")[4]))
    if len(missing) >= 2:
        if weekdays_ger:
            return (True,
                    f"{weekdays_ger[dt.datetime.now().strftime('%A')]}s um {dt.datetime.now().strftime('%H:%M')} Uhr " 
                    f"(± eine Stunde) liegt der Meldestatus durchschnittlich bei "
                    f"{100 - round(sum(percentages) / len(percentages), 2)} Prozent\n (d.h. die Meldung von "
                    f"{sum(missing) // len(missing)} Krankenhäusern steht noch aus).")
        else:
            return (True,
                    f"{dt.datetime.now().strftime('%A')}s at {dt.datetime.now().strftime('%H:%M')} "
                    f"(± one hour) the average reporting status is {round(sum(percentages) / len(percentages), 2)} %"
                    f" (meaning {sum(missing) // len(missing)} hospitals missing).")
    else:
        return False, "No sufficient data for average reporting status."


def read_create_send(category: [str] = "hicare", status_average: [bool] = True):
    print(f"Updating @ {dt.datetime.now().strftime('%H:%M Uhr')}")
    r = requests.get("https://www.intensivregister.de/api/public/intensivregister")
    contents = r.json()["data"]
    divi_numbers = {}
    for _ in range(len(contents)):
        if contents[_]["krankenhausStandort"]["bundesland"] in divi_numbers.keys():
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]] = {}
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["letzte_meldung"] = contents[_][
                "letzteMeldezeitpunkt"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["oldest_meldung"] = contents[_][
                "oldestMeldezeitpunkt"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["ecmo"] = contents[_][
                "maxBettenStatusEinschaetzungEcmo"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["hicare"] = contents[_][
                "maxBettenStatusEinschaetzungHighCare"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["locare"] = contents[_][
                "maxBettenStatusEinschaetzungLowCare"]
        else:
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]] = {}
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]] = {}
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["letzte_meldung"] = contents[_][
                "letzteMeldezeitpunkt"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["oldest_meldung"] = contents[_][
                "oldestMeldezeitpunkt"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["ecmo"] = contents[_][
                "maxBettenStatusEinschaetzungEcmo"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["hicare"] = contents[_][
                "maxBettenStatusEinschaetzungHighCare"]
            divi_numbers[contents[_]["krankenhausStandort"]["bundesland"]][
                contents[_]["krankenhausStandort"]["bezeichnung"]]["locare"] = contents[_][
                "maxBettenStatusEinschaetzungLowCare"]
    total_hosp = 0
    count = 0
    for county in divi_numbers.keys():
        for hosp in divi_numbers[county].keys():
            total_hosp += 1
            if divi_numbers[county][hosp]["letzte_meldung"][:10] != dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d"):
                count += 1

    if category not in ["ecmo", "hicare", "locare"]:
        category = "hicare"
    if category == "ecmo":
        pretty_cat = "ECMO"
    elif category == "locare":
        pretty_cat = "Low Care"
    else:
        pretty_cat = "High Care"

    pretty_date = dt.datetime.now().strftime("%d.%m.%Y")
    pretty_time = dt.datetime.now().strftime("%H:%M Uhr")
    county_names = []
    county_cat_perc = []
    for county in sorted(divi_numbers.keys()):
        this_county = bundesland_belegung(divi_numbers[county])
        county_cat_nums = []
        for k in this_county.keys():
            if k.split("_")[0] == category:
                county_cat_nums.append(this_county[k])
        this_county_cat_perc = []
        for _ in county_cat_nums[1:]:
            this_county_cat_perc.append((round(_*100/county_cat_nums[0], 3)))
        county_names.append(county.replace("_", "-").replace("UE", "Ü"))
        county_cat_perc.append(this_county_cat_perc)
    print(f"Creating {pretty_cat} plot... ", end="")
    fig, axes = plt.subplots(4, 4, figsize=[10, 8])
    fig.suptitle(f"{pretty_date}, {pretty_cat}\n(Stand: {pretty_time})")
    labels = ['Verfügbar', 'Begrenzt', 'Nicht Verfügbar']
    colors = ["lime", "yellow", "red"]
    for i, ax in enumerate(axes.flatten()):
        x = county_cat_perc[i]
        ax.pie(x, autopct=lambda p: '{:.1f}%'.format(round(p, 2)) if p > 0 else '', pctdistance=0.55,
               startangle=90, colors=colors, textprops={'fontsize': 8},
               wedgeprops={"edgecolor": "black", 'linewidth': .5, 'antialiased': True})
        ax.set_title(county_names[i], fontsize=10)
    plt.legend(labels, loc=(0.75, -.55), fontsize="small")
    plt.text(-14.8, -1.85,
             f'Quelle: https://www.divi.de/register/tagesreport,\n        '
             f'    umfasst tagesaktuelle Zahlen von {100 - (round(count * 100 / total_hosp, 2))} '
             f'% der meldenden Krankenhäuser.', horizontalalignment='left', verticalalignment='center')
    if status_average and report_status("deutsch")[0]:
        plt.text(-14.8, -2.6,
                 report_status("deutsch")[1],
                 horizontalalignment='left', verticalalignment='center')
    plt.grid(b=True, which='major', color='#666666', linestyle='-', rasterized=True)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.4)
    print(f"done.\nSending via email to {mail_addr}... ", end="")
    f = io.BytesIO()
    img_format = "png"
    plt.savefig(f, format=img_format, edgecolor='black', dpi=200, facecolor='silver', transparent=True)
    f.seek(0)
    img_data = f.read()
    msg = EmailMessage()
    msg["FROM"] = USER
    msg["TO"] = mail_addr
    msg["Subject"] = f"DIVI Update {pretty_date} um {pretty_time} - {pretty_cat}"
    msg.add_attachment(img_data, maintype='image', subtype=img_format,
                       filename=f"{category}_latest_update.png")
    s = smtplib.SMTP("smtp.mail.yahoo.com")
    s.starttls()
    s.login(USER, PASSWORD)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print("done.")


if __name__ == "__main__":
    mail_addr = input("Email: ")
    print("Options:\n+ 1: High Care\n+ 2: High Care and ECMO\n+ 3: High Care and Low Care\n+ 4: All three\n")
    options = input("Choose Option: ")
    if input("Include average report status? (y/n) ").lower() == "y":
        rep_stat = True
    else:
        rep_stat = False
    if mail_addr == "" or "@" not in mail_addr or "." not in mail_addr:
        mail_addr = TO_ADDR
    if options == "2":
        read_create_send(category="hicare", status_average=rep_stat)
        read_create_send(category="ecmo", status_average=rep_stat)
    elif options == "3":
        read_create_send(category="hicare", status_average=rep_stat)
        read_create_send(category="locare", status_average=rep_stat)
    elif options == "4":
        read_create_send(category="hicare", status_average=rep_stat)
        read_create_send(category="locare", status_average=rep_stat)
        read_create_send(category="ecmo", status_average=rep_stat)
    else:
        read_create_send(status_average=rep_stat)
