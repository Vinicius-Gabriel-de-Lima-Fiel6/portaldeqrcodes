import streamlit as st
from supabase import create_client


supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def t(val): 
   
    return val if val and str(val).strip() != "" else "Sem informação"

def mostrar_ficha():
    params = st.query_params
    
    # Se não houver nenhum dos parâmetros conhecidos, mostra a tela de espera
    if not any(key in params for key in ["id"]):
        st.info("👋 SynapseLab: Aguardando leitura de um Qr Code")
        return

  
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
if __name__ == "__main__":
    mostrar_ficha()
