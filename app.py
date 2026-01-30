import streamlit as st
from supabase import create_client

# Conexão
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def t(val): 
    """Função para tratar valores nulos ou vazios"""
    return val if val and str(val).strip() != "" else "Sem informação"

def mostrar_ficha():
    params = st.query_params
    
    # --- 1. LÓGICA PARA SUBSTÂNCIAS (?id=...) ---
    if "id" in params:
        res = supabase.table("substancias").select("*").eq("id", params["id"]).execute()
        if res.data:
            item = res.data[0]
            st.title(f"🧪 {item['nome']}")
            st.write(f"**Organização:** {t(item.get('org_name'))}")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Finalidade:** {t(item.get('finalidade'))}")
                st.write(f"**Concentração:** {t(item.get('concentracao'))}")
                st.write(f"**Nº CAS:** {t(item.get('cas'))}")
            with col2:
                # Mostra quantidade com a unidade de medida que criamos
                unidade = item.get('unidade_medida', '')
                st.write(f"**Estoque Atual:** {t(item.get('quantidade'))} {unidade}")
                st.write(f"**Validade:** {t(item.get('validade'))}")
                st.write(f"**Estoque Mínimo:** {t(item.get('estoque_minimo'))}")

            st.subheader("🛡️ Segurança (NFPA 704)")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Saúde", t(item.get('saude')))
            c2.metric("Fogo", t(item.get('fogo')))
            c3.metric("Reat.", t(item.get('reatividade')))
            c4.metric("Esp.", t(item.get('especial')))

            st.warning(f"**⚠️ Instruções de Emergência:**\n\n{t(item.get('instrucoes'))}")
        else:
            st.error("Substância não encontrada.")

    # --- 2. LÓGICA PARA VIDRARIAS (?vid=...) ---
    elif "vid" in params:
        res = supabase.table("vidrarias").select("*").eq("id", params["vid"]).execute()
        if res.data:
            vid = res.data[0]
            st.title(f"⚗️ {vid['tipo']}")
            st.write(f"**Patrimônio/Nº:** {vid['numeracao']}")
            st.divider()
            
            c1, c2 = st.columns(2)
            c1.info(f"**Capacidade:** {t(vid.get('capacidade'))}")
            c2.info(f"**Laboratório:** {t(vid.get('org_name'))}")
            
            st.success("✅ Vidraria verificada no sistema.")
        else:
            st.error("Vidraria não encontrada.")

    # --- 3. LÓGICA PARA PROJETOS (?proj=...) ---
    elif "proj" in params:
        res = supabase.table("projetos").select("*").eq("id", params["proj"]).execute()
        if res.data:
            proj = res.data[0]
            st.title(f"📂 Projeto: {proj['nome']}")
            st.write(f"**Status:** {t(proj.get('status'))}")
            st.divider()

            st.write(f"**Responsável:** {t(proj.get('responsavel'))}")
            st.write(f"**Data de Abertura:** {t(proj.get('created_at'))}")
            
            if proj.get('status') == "Ativo":
                st.success("🚀 Este projeto está em andamento.")
            else:
                st.warning(f"📢 Status atual: {proj.get('status')}")
        else:
            st.error("Projeto não encontrado.")

    else:
        st.info("👋 SynapseLab: Aguardando leitura de um QR Code de Substância, Vidraria ou Projeto.")

if __name__ == "__main__":
    mostrar_ficha()
