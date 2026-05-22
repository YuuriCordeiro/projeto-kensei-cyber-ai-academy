import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Kensei Home Care", page_icon="🏠", layout="centered")

# Inicialização de dados fictícios no Session State para persistência durante a sessão
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"categoria": "Limpeza", "tarefa": "Limpar o chão", "frequencia": "Diária", "ultima_realizacao": datetime.now() - timedelta(days=1)},
        {"categoria": "Limpeza", "tarefa": "Lavar louça", "frequencia": "Diária", "ultima_realizacao": datetime.now()},
        {"categoria": "Limpeza", "tarefa": "Limpar janelas", "frequencia": "Mensal", "ultima_realizacao": datetime.now() - timedelta(days=32)},
        {"categoria": "Manutenção/Reparos", "tarefa": "Limpar filtro do ar-condicionado", "frequencia": "Mensal", "ultima_realizacao": datetime.now() - timedelta(days=45)},
        {"categoria": "Manutenção/Reparos", "tarefa": "Trocar filtro de água", "frequencia": "Mensal", "ultima_realizacao": datetime.now() - timedelta(days=10)},
        {"categoria": "Manutenção/Reparos", "tarefa": "Revisar lâmpadas", "frequencia": "Semanal", "ultima_realizacao": datetime.now() - timedelta(days=5)},
        {"categoria": "Organização", "tarefa": "Organizar despensa", "frequencia": "Semanal", "ultima_realizacao": datetime.now() - timedelta(days=8)},
        {"categoria": "Organização", "tarefa": "Arrumar guarda-roupa", "frequencia": "Mensal", "ultima_realizacao": datetime.now() - timedelta(days=20)},
    ]

if "completed_today" not in st.session_state:
    st.session_state.completed_today = []

st.title("🏠 Kensei Home Care")
st.markdown("Gerencie as rotinas da sua casa de forma inteligente.")

# --- SEÇÃO DE ALERTAS DE MANUTENÇÃO ---
st.subheader("⚠️ Alertas de Manutenção")

alertas_encontrados = False
hoje = datetime.now()

for task in st.session_state.tasks:
    atraso = hoje - task["ultima_realizacao"]
    is_overdue = False
    
    if task["frequencia"] == "Diária" and atraso.days >= 1:
        is_overdue = True
    elif task["frequencia"] == "Semanal" and atraso.days >= 7:
        is_overdue = True
    elif task["frequencia"] == "Mensal" and atraso.days >= 30:
        is_overdue = True
        
    if is_overdue:
        st.error(f"**ATRASADO:** {task['tarefa']} (Frequência: {task['frequencia']}) - Última vez: {task['ultima_realizacao'].strftime('%d/%m/%Y')}")
        alertas_encontrados = True

if not alertas_encontrados:
    st.success("Tudo em dia por aqui! Nenhuma manutenção crítica atrasada. ✅")

st.divider()

# --- BARRA DE PROGRESSO ---
total_tasks = len(st.session_state.tasks)
completed_count = len(st.session_state.completed_today)
progress = completed_count / total_tasks

st.write(f"### Progresso de Conclusão")
st.progress(progress, text=f"{int(progress*100)}% das tarefas realizadas")

# --- CATEGORIAS EM ABAS ---
tab_limpeza, tab_manutencao, tab_org = st.tabs(["🧹 Limpeza", "🔧 Manutenção/Reparos", "📦 Organização"])

def render_task_list(categoria):
    tasks_filtradas = [t for t in st.session_state.tasks if t["categoria"] == categoria]
    
    for i, task in enumerate(tasks_filtradas):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            # Identificador único para o checkbox baseado no nome da tarefa
            is_done = st.checkbox(task["tarefa"], key=f"check_{task['tarefa']}")
            
            # Lógica para atualizar o progresso
            if is_done and task["tarefa"] not in st.session_state.completed_today:
                st.session_state.completed_today.append(task["tarefa"])
                st.rerun()
            elif not is_done and task["tarefa"] in st.session_state.completed_today:
                st.session_state.completed_today.remove(task["tarefa"])
                st.rerun()
                
        with col2:
            st.write(f"⏱️ {task['frequencia']}")
            
        with col3:
            st.write(f"📅 {task['ultima_realizacao'].strftime('%d/%m/%Y')}")

with tab_limpeza:
    st.write("### Rotinas de Limpeza")
    render_task_list("Limpeza")

with tab_manutencao:
    st.write("### Manutenção e Reparos")
    render_task_list("Manutenção/Reparos")

with tab_org:
    st.write("### Organização Geral")
    render_task_list("Organização")

# --- TABELA RESUMO ---
st.divider()
with st.expander("🔍 Visualizar Tabela Completa"):
    df = pd.DataFrame(st.session_state.tasks)
    # Formata a data para exibição na tabela
    df["ultima_realizacao"] = df["ultima_realizacao"].dt.strftime('%d/%m/%Y')
    st.dataframe(df, use_container_width=True)

if st.button("🔄 Resetar Sessão"):
    st.session_state.completed_today = []
    st.rerun()

with st.sidebar:
    st.header("Sobre")
    st.info("App de Gerenciamento Doméstico desenvolvido na Aula 7 para prática de UI Reativa.")