import io
import re
import zipfile
import streamlit as st
from datetime import datetime, timedelta
import yaml
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import requests
import json


TABLE_COLUMNS = ("Datum", "Název", "Zdroje", "Odkaz na kvíz", "Řešení příkladů")
PAGE_TITLE = "Kurzy Pythonu"


st.title(PAGE_TITLE)
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()


@st.cache_data
def all_courses_data():
    with open("course_data.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@st.cache_data
def get_solutions(url):
    return io.BytesIO(requests.get(url).content)


def title_page():
    def format_link(link):
        return f"<a href='{link}'>odkaz</a>"

    for _, row in df.iterrows():
        course_id = row["course_id"]
        form_links = [link.strip() for link in row["google_form_list"].split(",")]
        course_data = all_courses_data().get(course_id)
        if not course_data:
            continue
        start_date = datetime(*map(int, row["start_date"].split("-")))
        st.subheader(row["run_title"])

        markdown_output = []
        for i, lecture in enumerate(course_data["lectures"]):
            lecture_date = start_date + timedelta(weeks=i)
            markdown_output.append(
                [
                    lecture_date.strftime("%Y-%m-%d"),
                    lecture["title"],
                    ", ".join([format_link(link) for link in lecture["resources"]]),
                    form_links[i] if i < len(form_links) else "",
                    (
                        f"[Řešení](?page=solution&course_id={course_id}&lecture_id={i}&run_id={row["run_id"]})"
                        if lecture["resources"]
                        and lecture_date + timedelta(days=int(row["show_solution_days"])) < datetime.now()
                        else ""
                    ),
                ]
            )

        markdown_table = f"| {"|".join(TABLE_COLUMNS)} |\n"
        markdown_table += f"| {"|".join(["-" * 5 for _ in range(len(TABLE_COLUMNS))])} |\n"
        for markdown_row in markdown_output:
            markdown_table += f"| {"|".join(markdown_row)} |\n"
        st.markdown(markdown_table, unsafe_allow_html=True)


def format_solution(content):
    if match := re.search(r"^title:\s*(.*)$", content, re.MULTILINE):
        title = match.group(1)
    else:
        title = ""
    content = re.sub(r"---.*?---", "", content, flags=re.DOTALL)
    return f"#### {title}{content}"


def solution(course_id, lecture_id):
    course_data = all_courses_data().get(course_id)
    if not course_data:
        return
    lecture = course_data["lectures"][int(lecture_id)]
    st.subheader(lecture["title"])
    if "repository" not in lecture:
        return
    url = f"{lecture["repository"]}/raw/refs/heads/main/solutions.zip"
    solution_file = get_solutions(url)
    with zipfile.ZipFile(solution_file, "r") as zip_file:
        metadata_str = zip_file.read("metadata.json").decode("utf-8")
        file_metadata = json.loads(metadata_str)
    lecture_names = [res.split("/")[-2] for res in lecture["resources"]]
    lecture_solution_files = [
        f"{sol["dirpath"].strip("/")}/{sol["filename"]}"
        for sol in file_metadata
        if sol["dirpath"].split("/")[-2] in lecture_names
    ]
    with zipfile.ZipFile(solution_file, "r") as zip_file:
        zip_file_infos = [i for i in zip_file.infolist() if i.filename.replace(".sol", "") in lecture_solution_files]
        for file_info in zip_file_infos:
            content = zip_file.read(file_info).decode("utf-8")
            st.markdown(format_solution(content))


def solution_check(course_id, run_id, lecture_id):
    df_course = df[df["run_id"] == run_id]
    if df_course.shape[0] != 1:
        return
    run_data = df_course.iloc[0]
    if run_data["run_id"] not in st.session_state or st.session_state[run_data["run_id"]] != run_data["password"]:
        with st.form("login_form"):
            st.write("Zadej heslo pro zobrazení řešení.")
            password = st.text_input("Heslo", type="password")
            submit_button = st.form_submit_button("Uložit")

            if submit_button:
                print(run_data)
                if password == run_data["password"]:
                    st.session_state[run_data["run_id"]] = password
                    st.rerun()
                else:
                    st.error("Nesprávné heslo!")
    else:
        solution(course_id, lecture_id)


if st.query_params.get("page") is None:
    title_page()
elif st.query_params.get("page") == "solution":
    solution_check(st.query_params.get("course_id"), st.query_params.get("run_id"), st.query_params.get("lecture_id"))
