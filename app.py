import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def carregar_recursos():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_recursos()
params = st.query_params

if "id" in params and "org" in params:
    res = supabase.table("substancias").select("*").eq("id", params["id"]).eq("org_name", params["org"]).execute()
    if res.data:
        item = res.data[0]
        with open("index.html") as f:
            html = f.read()
            html = html.replace("{{nome}}", item['nome'])\
                       .replace("{{org}}", item['org_name'])\
                       .replace("{{fogo}}", str(item['fogo']))\
                       .replace("{{reat}}", str(item['reatividade']))\
                       .replace("{{saude}}", str(item['saude']))\
                       .replace("{{especial}}", str(item['especial']))\
                       .replace("{{instrucoes}}", item['instrucoes'])
            st.markdown(html, unsafe_allow_html=True)
else:
    st.error("Escaneie um QR Code válido da empresa.")
