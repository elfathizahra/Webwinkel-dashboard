from pathlib import Path
from zipfile import ZipFile, BadZipFile
import streamlit as st

st.set_page_config(page_title="Webwinkel · prestaties", page_icon="🛍️", layout="wide")

base = Path(__file__).resolve().parent
html_path = base / "Webwinkel_Dashboard_Excel.html"
archive_path = base / "Webwinkel_Streamlit.zip"

try:
    if html_path.is_file():
        dashboard_html = html_path.read_text(encoding="utf-8")
    elif archive_path.is_file():
        with ZipFile(archive_path) as archive:
            pages = [name for name in archive.namelist()
                     if Path(name).name == "Webwinkel_Dashboard_Excel.html"]
            if len(pages) != 1:
                st.error("Het ZIP-bestand moet één Webwinkel_Dashboard_Excel.html bevatten.")
                st.stop()
            dashboard_html = archive.read(pages[0]).decode("utf-8")
    else:
        st.error("Voeg Webwinkel_Dashboard_Excel.html of Webwinkel_Streamlit.zip toe aan deze repository.")
        st.stop()
except (OSError, BadZipFile, UnicodeError) as error:
    st.error(f"Het dashboard kan niet worden gelezen: {error}")
    st.stop()

if callable(getattr(st, "iframe", None)):
    st.iframe(dashboard_html, height="content", alt="Webwinkel-dashboard met grafieken, antwoorden en filters")
else:
    import streamlit.components.v1 as components
    components.html(dashboard_html, height=1200, scrolling=True)
