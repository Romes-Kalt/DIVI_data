# DIVI_data

**For usage of acquired data** please contact the [webite's contact](https://divi.de/register/anprechpartner-register). 

Acquiring data and visualization of this data provided bei the Deutsche Interdisziplinäre Vereinigung für Intensiv- und Notfallmedizin.

## automatic_run.py

Using the [API](https://www.intensivregister.de/api/public/intensivregister) to create up to three different plots for availability at hospitals in Germany per county (Bundesland) and sending the plots per email to address (simple command line dialogue when starting the programm). 

<img src="https://github.com/Romes-Kalt/DIVI_data/blob/main/plots/2022_03_20at13-37_hicare.png" alt="availability" width="600"/>

## rki_weekly_xlsx.py

Downloading the weekly published XLSX file provided by RKI (incl. moving and replacing the previous file in project's source folder) and generating plots accordingly. Parameters will be changed in python file. 

<img src="https://github.com/Romes-Kalt/DIVI_data/blob/main/data/xlsx_data/plots/2022_03_14_inc_of_5_bl_last_28days.png" alt="weekly_rki" width="600"/>

## zeitreihe-csv.py

Downloading the daily updated csv file containing numbers for current ICS patients and active COVID cases in hospitals (incl. moving and replacing the previous file in project's source folder).

<img src="https://github.com/Romes-Kalt/DIVI_data/blob/main/plots/csv_plots/Aktuelle_COVID_Faelle_ITS.png" alt="zeitreihe" width="600"/>
