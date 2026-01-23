import streamlit as st
from supabase import create_client

# Conexão
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def mostrar_ficha():
    params = st.query_params
    if "id" in params:
        res = supabase.table("substancias").select("*").eq("id", params["id"]).execute()
        
        if res.data:
            item = res.data[0]
            
            # Função para tratar None
            def t(val): return val if val and str(val).strip() != "" else "Sem informação"

            st.title(f"🧪 {item['nome']}")
            st.write(f"**Empresa:** {item.get('org_name', 'Sem informação')}")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Finalidade:** {t(item.get('finalidade'))}")
                st.write(f"**Concentração:** {t(item.get('concentracao'))}")
                st.write(f"**Nº CAS:** {t(item.get('cas'))}")
            with col2:
                st.write(f"**Quantidade em Estoque:** {t(item.get('quantidade'))}")
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
    else:
        st.info("Aguardando leitura de QR Code...")

if __name__ == "__main__":
    mostrar_ficha()
