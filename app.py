import streamlit as st
from supabase import create_client

# Conexão
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def t(val): 
    """Função para tratar valores nulos ou vazios"""
    return val if val and str(val).strip() != "" else "Sem informação"

def mostrar_ficha():
    params = st.query_params
    
    # Se não houver nenhum dos parâmetros conhecidos, mostra a tela de espera
    if not any(key in params for key in ["id", "vid", "proj"]):
        st.info("👋 LabSmartAI: Aguardando leitura de um QR Code (Substância, Vidraria ou Projeto).")
        return

    # --- 1. LEITURA DE SUBSTÂNCIAS (id) ---
    if "id" in params:
        try:
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
                st.error(f"Substância ID {params['id']} não encontrada.")
        except Exception as e:
            st.error(f"Erro ao acessar tabela de substâncias: {e}")

    # --- 2. LEITURA DE VIDRARIAS (vid) ---
    if "vid" in params:
        try:
            res = supabase.table("vidrarias").select("*").eq("id", params["vid"]).execute()
            if res.data:
                vid = res.data[0]
                if "id" in params: st.divider() # Separa se houver mais de um item na tela
                st.title(f"⚗️ {vid['tipo']}")
                st.write(f"**Patrimônio/Nº:** {vid['numeracao']}")
                
                c1, c2 = st.columns(2)
                c1.info(f"**Capacidade:** {t(vid.get('capacidade'))}")
                c2.info(f"**Laboratório:** {t(vid.get('org_name'))}")
            else:
                st.error(f"Vidraria ID {params['vid']} não encontrada.")
        except Exception as e:
            st.error(f"Erro ao acessar tabela de vidrarias: {e}")

    # --- 3. LEITURA DE PROJETOS (proj) ---
    if "proj" in params:
        try:
            res = supabase.table("projetos").select("*").eq("id", params["proj"]).execute()
            if res.data:
                proj = res.data[0]
                if any(k in params for k in ["id", "vid"]): st.divider()
                st.title(f"📂 Projeto: {proj['nome']}")
                st.write(f"**Status:** {t(proj.get('status'))}")
                
                st.write(f"**Responsável:** {t(proj.get('responsavel'))}")
                st.write(f"**Organização:** {t(proj.get('org_name'))}")
                
                if proj.get('status') == "Ativo":
                    st.success("🚀 Este projeto está em andamento.")
            else:
                st.error(f"Projeto ID {params['proj']} não encontrada.")
        except Exception as e:
            st.error(f"Erro ao acessar tabela de projetos: {e}")

if __name__ == "__main__":
    mostrar_ficha()
