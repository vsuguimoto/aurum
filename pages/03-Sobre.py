import streamlit as st
import pandas as pd
import os

from src.utils.utils import AuditarModelo, st_metric_display, svg_write_html

TITULO_PROJETO = 'Aurum Praesagio'

st.set_page_config(
        page_title=f'{TITULO_PROJETO} - Análise',
        page_icon='🔮',
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)

st.markdown('# Sobre o Projeto')

st.subheader('''
Visão Geral
''')
st.markdown('''
Aurum Praesagio em tradução direta do Latim significa Ouro e Pressentimento, desenvolvemos esse projeto para dar acesso a analise quantitativa de maneira simplificada e responder a principal pergunta de todo investidor:
''')

st.info('**Quando eu devo comprar?**')

st.markdown('''
É comum encontrar pessoas que ao iniciarem no mercado financeiro buscarem formas fáceis de investir e acabarem se deparando ou com taxas abusivas de gestores, ou com falsos gurus que prometem ganhos rápidos, ou com pessoas que falam em códigos de forma que sempre estão corretos.
''')

st.subheader('''
Limitações
''')
st.markdown('''
 - **Entrada da operação**: utilizamos como entrada em uma posição de um ativo o preço de fechamento do dia, contudo não é possível abrir uma posição se o mercado está fechado, para tornar a entrada viável é necessário ter acesso a dados intradiários que em sua maioria são pagos. Dado as implicações legais do projeto, preferimos manter a limitação.
 - **Retornos passados não indicam lucros futuros**: os retornos do modelo e ou da carteira não são garantia de que seguindo nossa ou qualquer outra estratégia obterá lucros. Em todas operações há riscos envolvidos.
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

if st.button('Analisar'):

    INFO_MODELO = AuditarModelo(AUDITAR_MODELO)

    METRIC_COLS = st.columns(5)

    with METRIC_COLS[0]:
        st_metric_display(f'{INFO_MODELO.ACCURACY*100:.2f}%', 'Acurácia<br>&nbsp;')

    with METRIC_COLS[1]:
        st_metric_display(f'{INFO_MODELO.PRECISION*100:.2f}%', 'Precisão<br>&nbsp;')

    with METRIC_COLS[2]:
        st_metric_display(f'{INFO_MODELO.MODEL_CUMULATIVE_RETURN*100 - 100:.2f}%', 'Retorno <br> acumulado')

    with METRIC_COLS[3]:
        st_metric_display(f'{INFO_MODELO.IBOV_BNH_RETURN*100 - 100:.2f}%', 'Retorno <br> IBOVESPA')

    with METRIC_COLS[4]:
        st_metric_display(f'{INFO_MODELO.ADPATED_SHARPE_RATIO:.2f}', 'Sharpe Ratio Adaptado')


    plotly_fig_accuracy = INFO_MODELO.plot_accuracy_over_time()

    st.plotly_chart(plotly_fig_accuracy)

    ARVORE_SVG = INFO_MODELO.plot_decision_tree().svg()
    
    st.download_button('Download - Estratégia do Modelo', data=ARVORE_SVG, file_name=f'Modelo.svg')

METRIC_EXPLANATION_COLS = st.columns(5)

with METRIC_EXPLANATION_COLS[0]:
    st.markdown('**Acurácia:** Proporção entre acertos e erros, nos diz o quanto o modelo está acertando.')

with METRIC_EXPLANATION_COLS[1]:
    st.markdown('**Precisão:** Proporção de vezes que o modelo diz que o preço de uma ação irá subir com o número de vezes que o preço realmente sobe.')

with METRIC_EXPLANATION_COLS[2]:
    st.markdown('**Retorno Acumulado:** Retorno acumulado do modelo para os últimos 6 meses.')

with METRIC_EXPLANATION_COLS[3]:
    st.markdown('**Retorno IBOVESPA:** Retorno acumulado do IBOVESPA para os últimos 6 meses.')

with METRIC_EXPLANATION_COLS[4]:
    st.markdown('**Sharpe Ratio Adaptado:** Relação entre o retorno do modelo comparado com o IBOVESPA ponderado pelo seu risco. Quanto maior, maior o retorno sobre o risco de investir no modelo.')

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