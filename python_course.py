import streamlit as st
from datetime import datetime, timedelta

# Original data
course_data = [
    ["Úvod, slicing, metody, moduly", ["https://kodim.cz/programovani/uvod-do-progr-2/uvod-do-programovani-2/slicing-metody-moduly/slicing"], "https://forms.gle/pKGqqRKp7i4JwWEcA"],
    ["Funkce, slovníky", ["https://kodim.cz/czechitas/uvod-do-progr-2/uvod-do-programovani-2/vlastni-funkce/funkce"], "https://forms.gle/smo9LFs9YZKipb6d9"],
    ["Slovníky", ["https://kodim.cz/czechitas/uvod-do-progr-2/uvod-do-programovani-2/slovniky/n-tice"], "https://forms.gle/D5Je3iy72M5DeXcc7"],
    ["Objektově orientované programování", ["https://kodim.cz/czechitas/python-oop/lekce/tridy/tridy"], "https://forms.gle/fCop4zQTSLUioPaNA"],
    ["Objektově orientované programování", ["https://kodim.cz/czechitas/python-oop/lekce/dedicnost/dedicnost"], "https://forms.gle/5naC236BLov34GkW7"],
    ["Objektově orientované programování", ["https://kodim.cz/czechitas/python-oop/lekce/dedicnost/dalsi-funkce"], "https://forms.gle/j2zDJed3KXmTbua29"],
    ["Datum a čas, instalace balíčků pomocí pip", ["https://kodim.cz/czechitas/uvod-do-progr-2/uvod-do-programovani-2/datum/datum", "https://kodim.cz/czechitas/uvod-do-progr-2/uvod-do-programovani-2/balicky-z-internetu/lesson"], "https://forms.gle/22c5KH81ZtwRhWS88"],
    ["Čtení a zápis textových souborů", ["https://kodim.cz/czechitas/uvod-do-progr-2/uvod-do-programovani-2/soubory/cteni-souboru"], "https://forms.gle/ahehRYyzb71wbV53A"],
    ["JSON a API", [], ""],
    ["Obsluha výjimek", [], ""],
    ["Regulární výrazy", [], ""],
    ["Rezerva", [], ""]
]

# Update course start date and lecture dates
start_date = datetime(2025, 1, 29)
updated_course_data = []

def format_link(link):
    return f"<a href='{link}'>odkaz</a>"

for i, lecture in enumerate(course_data):
    lecture_date = start_date + timedelta(weeks=i)
    updated_course_data.append([
        lecture_date.strftime("%Y-%m-%d"),
        lecture[0],
        ", ".join([format_link(link) for link in lecture[1]]),
        format_link(lecture[2]) if lecture[2] else "",
    ])

# Streamlit app
st.title("Programování v Pythonu")

# Build the Markdown table
markdown_table = "| Datum | Obsah lekce | Odkaz na materiály | Odkaz na kvíz |\n"
markdown_table += "|-------|-------------|--------------------|---------------|\n"

for row in updated_course_data:
    markdown_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |\n"

# Render the Markdown table in the app
st.markdown(markdown_table, unsafe_allow_html=True)
