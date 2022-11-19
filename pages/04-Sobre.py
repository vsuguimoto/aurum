import streamlit as st
import os

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Análise',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

st.markdown('# Sobre o Projeto')
st.info('“Everything that happens once can never happen again. But everything that happens twice will surely happen a third time.” ― Paulo Coelho')
st.subheader('''
Visão Geral
''')
st.markdown('''
Aurum Praesagio em tradução direta do Latim significa Ouro e Pressentimento, desenvolvemos esse projeto como uma alternativa a analise quantitativa clássica realizada pelas pessoas físicas.

Nosso objetivo é dar acesso a estratégias quantitativas de forma simplificada e transparente.

É comum encontrar pessoas que ainda seguem cegamente gurus do mercado financeiro que possuem um *setup* milagroso que irá te fazer ganhar rios de dinheiro, mas o que eles não te contam é que essas estratégias não são generalizáveis e muitas vezes não passam de um *overfitting* dos indicadores utilizados.


''')

st.subheader('''
Limitações
''')
st.markdown('''
 - **Entrada da operação**: utilizamos como entrada em uma posição de um ativo o preço de fechamento do dia, contudo não é possível abrir uma posição se o mercado está fechado, para tornar a entrada viável é necessário ter acesso a dados intradiários que em sua maioria são pagos. Dado as implicações legais do projeto, preferimos manter a limitação.
 - **Não podemos prever o futuro só olhando o passado**: todos os modelos treinados partem do principio que a partir dos dados hitóricos de um único ativo podemos prever a direção que aquele ativo irá ter, o que não é verdade.
 - **Feriados**: nossa análise considera apenas dias úteis, isso pode ser uma fonte de confusão, imagine que abra uma posição terça-feira 08/11/2022, pela estratégia o cliente deve manter o ativo sob custódia por 5 dias úteis, ou uma semana, contudo dia 15/11/2022 é feriado nacional e a posição deve ser mantida até quarta-feira, essa confusão dura ao menos 5 dias úteis.
''')


st.subheader('''
Performance
''')
AUDITAR_MODELO = st.multiselect(
        'Escolha o ativo',
        options=os.listdir('models'),
        format_func=lambda x: x.split('.')[0],
        max_selections=1 # Limita o número de ativos a serem escolhidos
    )
st.subheader('''
Feedback
''')

st.markdown('Fique a vontade para entrar em contato conosco, nossas redes sociais:')
col1, col2, col3 = st.columns(3)
        
with col1:
    st.markdown('**Jeong Lee**')
    st.markdown('[Linkedin](https://www.linkedin.com/in/jeong-lee-b04937117/)')
    st.markdown('[Github](https://github.com/jeongleeds)')
    
with col2:
    st.markdown('**Rodrigo Figueiredo**')
    st.markdown('[Linkedin](https://www.linkedin.com/in/rodrigo-figueiredo-73056732)')
    st.markdown('[Github](https://github.com/FIGUEIREDOGITHUB)')

with col3:
    st.markdown('**Vinicius Suguimoto**')
    st.markdown('[Linkedin](https://www.linkedin.com/in/suguimotovinicius/)')
    st.markdown('[Github](https://github.com/vsuguimoto/)')