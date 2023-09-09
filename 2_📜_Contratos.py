import streamlit as st
import requests
import pandas as pd
import datetime
import numpy as np
from PIL import Image
import plotly.express as px

st.set_page_config(
    page_title='bússola imobi',
    page_icon='🧭',
    layout='wide'
)

logo = Image.open('Bússola (2).png')
url = 'http://apps.superlogica.net/imobiliaria/api/contratos'

if 'access_token' in st.session_state:

    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'app_token': 'f3079a0b-a2d5-4eec-9d32-5eb0c2887b17',
            'access_token': st.session_state.access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        @st.cache_data
        def atualiza_contratos():
            # Faz a consulta à API da Superlogica
            response = requests.get(url, headers=headers).json()
            contratos = pd.DataFrame(response['data'])

            def ids_inquilinos(row):
                num_inquilinos = len(row['inquilinos'])
                inquilinos = []
                for inquilino in range(0, num_inquilinos):
                    nome = row['inquilinos'][inquilino]['id_pessoa_pes']
                    inquilinos.append(nome)
                return inquilinos

            def ids_beneficiarios(row):
                num_beneficiarios = len(row['proprietarios_beneficiarios'])
                beneficiarios = []
                for beneficiario in range(0, num_beneficiarios):
                    nome = row['proprietarios_beneficiarios'][beneficiario]['id_pessoa_pes'].title()
                    beneficiarios.append(nome)
                return beneficiarios

            def id_proprietario(row):
                proprietario = row['proprietarios_beneficiarios'][0]['id_pessoa_pes'].title()
                return proprietario

            def nomes_inquilinos(row):
                num_inquilinos = len(row['inquilinos'])
                inquilinos = []
                for inquilino in range(0, num_inquilinos):
                    nome = row['inquilinos'][inquilino]['st_nomeinquilino']
                    inquilinos.append(nome)
                return inquilinos

            def nome_proprietario(row):
                proprietario = row['proprietarios_beneficiarios'][0]['st_nome_pes'].title()
                return proprietario

            def conta_inquilinos(row):
                return len(row['inquilinos'])

            def conta_proprietarios(row):
                return len(row['proprietarios_beneficiarios'])

            contratos['numero_inquilinos'] = contratos.apply(conta_inquilinos, axis=1)
            contratos['nomes_inquilinos'] = contratos.apply(nomes_inquilinos, axis=1)
            contratos['numero_proprietarios'] = contratos.apply(conta_proprietarios, axis=1)
            contratos['nomes_proprietarios'] = contratos.apply(nome_proprietario, axis=1)
            contratos['id_proprietario'] = contratos.apply(id_proprietario, axis=1)

            contratos = contratos.loc[:, [
                'st_imovel_imo',
                'nome_proprietario',
                'proprietarios_beneficiarios',
                'st_bairro_imo',
                'st_cidade_imo',
                'st_estado_imo',
                'numero_inquilinos',
                'nomes_inquilinos',
                'numero_proprietarios',
                'nomes_proprietarios',
                'id_proprietario',
                'id_tipo_con',
                'st_tipo_imo',
                'vl_aluguel_con',
                'tx_adm_con',
                'tx_locacao_con',
                'fl_txadmvalorfixo_con',
                'fl_txlocacaovalorfixo_con',
                'dt_inicio_con',
                'dt_fim_con',
                'vl_venda_imo',
                'inquilinos',
                'dt_rescisao_con',
                'fl_ativo_con',
                'dt_garantiainicio_con',
                'dt_garantiafim_con',
                'nm_garantiaparcelas_con',
                'vl_garantiaparcela_con',
                'dt_seguroincendioinicio_con',
                'dt_seguroincendiofim_con',
                'vl_seguroincendio_con',
                'fl_seguroincendio_con',
                'nm_locacoesimovel_con',
                'dt_ultimoreajuste_con',
                'nm_parcelastxlocacao_con',
                'nm_repassegarantido_con',
                'fl_suspenso_con',
                'fl_renovacaoautomatica_con',
                'codigo_contrato',
                'gerente_comercial'
            ]]

            colunasdatas = [
                'dt_inicio_con',
                'dt_fim_con',
                'dt_rescisao_con',
                'dt_garantiainicio_con',
                'dt_garantiafim_con',
                'dt_seguroincendioinicio_con',
                'dt_seguroincendiofim_con',
                'dt_ultimoreajuste_con'
            ]

            colunasvalores = [
                'vl_aluguel_con',
                'tx_adm_con',
                'tx_locacao_con',
                'vl_venda_imo',
                'vl_garantiaparcela_con',
                'vl_seguroincendio_con'
            ]

            colunasinteiras = [
                'nm_garantiaparcelas_con',
                'nm_locacoesimovel_con',
                'nm_parcelastxlocacao_con'
            ]

            contratos[colunasdatas] = contratos[colunasdatas].apply(pd.to_datetime)
            contratos[colunasinteiras] = contratos[colunasinteiras].apply(pd.to_numeric)
            contratos[colunasvalores] = contratos[colunasvalores].apply(pd.to_numeric)

            colunas_maiusculas = [
                'st_imovel_imo',
                'nome_proprietario',
                'st_bairro_imo',
                'st_cidade_imo',
            ]
            contratos[colunas_maiusculas] = contratos[colunas_maiusculas].applymap(
                lambda x: x.title() if isinstance(x, str) else x)

            # Tratando categorias de tipos de imovel
            codigos_tipos_imoveis = [
                '1', '8', '4', '14', '33', '11', '23', '5', '36', '3', '38', '9', '24', '20', '13',
                '12', '39', '22', '44', '25', '1000', '2', '10', '16', '6', '42', '29', '21', '40'
            ]
            tipo_imovel = [
                'Casa', 'Garagem', 'Apartamento', 'Chácara', 'Apartamento duplex', 'Sala comercial',
                'Sítio', 'Cobertura', 'Rancho', 'Casa comercial', 'Apartamento triplex', 'Área comum',
                'Sobrado', 'Fazenda', 'Barracão', 'Loja', 'Edícula', 'Prédio', 'Casa assombrada', 'Conjunto',
                'Outro', 'Casa em condomínio', 'Escritório', 'Galpão', 'Flat', 'Andar corporativo', 'Bangalô',
                'Haras', 'Box/Garagem'
            ]
            tiposimoveis = {'st_tipo_imo': codigos_tipos_imoveis, 'tipo_imovel': tipo_imovel}
            tiposimoveis = pd.DataFrame(tiposimoveis)

            contratos = pd.merge(contratos, tiposimoveis, on='st_tipo_imo', how='left')

            # Tratando categorias de tipos de contrato
            codigos_tipos_contrato = ['1', '2', '3', '4', '5', '7']
            tipo_contrato = ['Residencial', 'Não residencial', 'Comercial', 'Indústria', 'Temporada', 'Misto']
            tiposcontrato = {'id_tipo_con': codigos_tipos_contrato, 'tipo_contrato': tipo_contrato}
            tiposcontrato = pd.DataFrame(tiposcontrato)

            contratos = pd.merge(contratos, tiposcontrato, on='id_tipo_con', how='left')
            contratos = contratos.drop(columns=['id_tipo_con', 'st_tipo_imo'])

            def booleanos(dado):
                if dado == '1':
                    return 'Sim'
                elif dado == '2':
                    return 'Sim'
                elif dado == '4':
                    return 'Suspenso'
                elif dado == '0':
                    return 'Não'

            # Tratando booleanos da base
            contratos['fl_txadmvalorfixo_con'] = contratos['fl_txadmvalorfixo_con'].apply(booleanos)
            contratos['fl_txlocacaovalorfixo_con'] = contratos['fl_txlocacaovalorfixo_con'].apply(booleanos)
            contratos['fl_ativo_con'] = contratos['fl_ativo_con'].apply(booleanos)
            contratos['fl_suspenso_con'] = contratos['fl_suspenso_con'].apply(booleanos)
            contratos['fl_renovacaoautomatica_con'] = contratos['fl_renovacaoautomatica_con'].apply(booleanos)

            hoje = pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'))
            contratos['tempo_contrato'] = (hoje - contratos['dt_inicio_con']).dt.days
            contratos['tempo_fim_contrato'] = (contratos['dt_fim_con'] - hoje).dt.days

            contratos['valor_taxa_administracao'] = np.where(contratos['fl_txadmvalorfixo_con'] == 'Sim',contratos['tx_adm_con'],(contratos['tx_adm_con'] / 100) * contratos['vl_aluguel_con'])
            contratos['valor_taxa_locacao'] = np.where(contratos['fl_txlocacaovalorfixo_con'] == 'Sim',contratos['tx_locacao_con'],(contratos['tx_locacao_con'] / 100) * contratos['vl_aluguel_con'])
            contratos.drop(columns=['proprietarios_beneficiarios', 'id_proprietario', 'dt_garantiainicio_con', 'dt_garantiafim_con',
            'nm_garantiaparcelas_con', 'vl_garantiaparcela_con', 'inquilinos','dt_seguroincendioinicio_con', 'dt_seguroincendiofim_con',
            'vl_seguroincendio_con', 'fl_seguroincendio_con', 'nm_parcelastxlocacao_con','nm_repassegarantido_con', 'fl_renovacaoautomatica_con'], inplace=True)

            contratos.columns = ['Nome do imóvel',
                                 'Nome do proprietário',
                                 'Bairro',
                                 'Cidade',
                                 'Estado',
                                 'Número de inquilinos',
                                 'Nome(s) do(s) inquilino(s)',
                                 'Número de proprietários/beneficiários',
                                 'Nomes dos proprietários/beneficíarios',
                                 'Valor do aluguel',
                                 'Taxa de administração do contrato',
                                 'Taxa de locação do contrato',
                                 'Taxa de administração é valor fixo',
                                 'Taxa de locação é valor fixo',
                                 'Data de início do contrato',
                                 'Data do fim do contrato',
                                 'Valor de venda do imóvel',
                                 'Data de recisão',
                                 'Contrato ativo',
                                 'Número de locações do imóvel',
                                 'Data do último reajuste',
                                 'Contrato suspenso',
                                 'Código do contrato',
                                 'Gerente comercial',
                                 'Tipo de imóvel',
                                 'Tipo de contrato',
                                 'Tempo de contrato',
                                 'Tempo para fim do contrato',
                                 'Valor taxa de administração',
                                 'Valor taxa de locação']
            contratos = contratos.set_index('Código do contrato')
            return contratos

        def dataframedados(colunas, dataframe):
            dados = dataframe[colunas]
            st.dataframe(dados)

        contratos = atualiza_contratos()

        # Sidebar
        with st.sidebar:
            col1, col2, col3 = st.columns(spec=[2,6,1])
            with col2:
                st.image(logo, width=150)

        if isinstance(contratos, pd.DataFrame):
            contratosativos = contratos.loc[contratos['Contrato ativo'] == 'Sim']
            vgl = round(contratosativos.loc[contratosativos['Contrato ativo'] == 'Sim']['Valor do aluguel'].sum(), 2)
            receita_prevista = round(contratosativos.loc[contratosativos['Contrato ativo'] == 'Sim']['Taxa de administração do contrato'].sum(), 2)
            contratos_ativos = contratosativos.loc[contratosativos['Contrato ativo'] == 'Sim']['Nome do imóvel'].count()
            media_aluguel = round(contratosativos.loc[contratosativos['Contrato ativo'] == 'Sim']['Valor do aluguel'].mean(),2)
            contratos_residenciais = contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Residencial')]['Nome do imóvel'].count()
            media_aluguel_residencial = round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Residencial')]['Valor do aluguel'].mean(), 2)
            contratos_comerciais = contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Comercial')]['Nome do imóvel'].count()
            media_aluguel_comercial = round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Comercial')]['Valor do aluguel'].mean(), 2)
            contratos_outros = contratos.loc[(contratos['Contrato ativo'] == 'Sim') & (contratos['Tipo de contrato'] != 'Residencial') & (contratos['Tipo de contrato'] != 'Comercial')]['Nome do imóvel'].count()
            media_aluguel_outros = round(contratos.loc[(contratos['Contrato ativo'] == 'Sim') & (contratos['Tipo de contrato'] != 'Residencial') & (contratos['Tipo de contrato'] != 'Comercial')]['Valor do aluguel'].mean(), 2)
            contratosativos['Bairro / Cidade / Estado'] = contratosativos['Bairro'] + ', ' + contratosativos['Cidade'] + '- ' + contratosativos['Estado']

            hoje = pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'))
            inicio_mes_atual = pd.to_datetime(datetime.date(hoje.year, hoje.month, 1))
            inicio_proximo_mes = pd.to_datetime(datetime.date(hoje.year, hoje.month + 1, 1))
            contratosiniciados_estemes = contratos.loc[(contratos['Data de início do contrato'] >= inicio_mes_atual) & (contratos['Data de início do contrato'] < hoje)]
            contratosterminando_estemes = contratos.loc[(contratos['Data do fim do contrato'] >= inicio_mes_atual) & (contratos['Data do fim do contrato'] < hoje)]
            saldo_contratos = int(contratosiniciados_estemes['Nome do imóvel'].count() - contratosterminando_estemes['Nome do imóvel'].count())
            saldo_receita = round(float(contratosiniciados_estemes['Valor taxa de administração'].count() - contratosterminando_estemes['Valor taxa de administração'].count()),1)
            saldo_aluguel = round(float(contratosiniciados_estemes['Valor do aluguel'].sum() - contratosterminando_estemes['Valor do aluguel'].sum()),1)
            saldo_media_aluguel = round(float(contratosiniciados_estemes['Valor do aluguel'].mean() - contratosterminando_estemes['Valor do aluguel'].mean()),1)

        def histogramas(variavel, ranking):
          medias = contratosativos.groupby(by=variavel, as_index=False).mean(numeric_only=True)
          medias = medias.loc[:,[variavel, 'Valor do aluguel']]
          contagem = contratosativos.groupby(by=variavel, as_index=False).count()
          contagem = contagem.loc[:,[variavel, 'Valor do aluguel']]
          contagem['percentual_contratos'] = (contagem['Valor do aluguel']/contagem['Valor do aluguel'].sum())*100
          contagem['percentual_contratos'] = contagem['percentual_contratos'].round(2)
          soma = contratosativos.groupby(by=variavel, as_index=False).sum(numeric_only=True)
          soma = soma.loc[:,[variavel, 'Valor do aluguel']]
          soma['percentual_aluguel'] = (soma['Valor do aluguel']/soma['Valor do aluguel'].sum())*100
          soma['percentual_aluguel'] = soma['percentual_aluguel'].round(2)
          histograma = pd.merge(contagem, medias, on=variavel, how='left')
          histograma = pd.merge(histograma, soma, on=variavel, how='left')
          histograma.columns = [variavel, 'Contratos', '% contratos', 'Média de aluguel', 'Aluguel total', '% aluguel']
          histograma['Média de aluguel'] = histograma['Média de aluguel'].apply(lambda x: '{:.2f}'.format(float(x)))
          histograma['Aluguel total'] = histograma['Aluguel total'].apply(lambda x: '{:.2f}'.format(float(x)))
          histograma = histograma.sort_values(by=ranking, ascending=False)
          return histograma

        # Aba de escolhas
        visaogeral, segmentado, dados, mapa = st.tabs(["Visão geral", "Análises segmentadas", "Dados", "Visão de mapa"])

        # Aba de visão geral da carteira
        with visaogeral:
            if isinstance(contratos, pd.DataFrame):
                st.header("Visão geral da carteira")
                col1, col2, col3, col4 = st.columns(spec=[1,1.5,1.5,1.5])
                with col1:
                    st.metric("Contratos ativos", contratos_ativos, saldo_contratos)

                with col2:
                    st.metric("Receita prevista", f"R$ {receita_prevista}", f"R$ {saldo_receita}")

                with col3:
                    st.metric("VGL",f"R$ {vgl}", f"R$ {saldo_aluguel}")

                with col4:
                    st.metric("Média de aluguel", f"R$ {media_aluguel}", f"R$ {saldo_media_aluguel}")

                st.write("#### Contratos por tipo de imóvel")

                df1 = histogramas('Tipo de imóvel', 'Contratos')
                coluna1, coluna2 = st.columns(spec=[2, 3])
                with coluna1:
                    st.write(df1[['Tipo de imóvel', 'Contratos']])
                with coluna2:
                    donut = px.pie(df1[['Tipo de imóvel', 'Contratos']], names='Tipo de imóvel', values='Contratos', height=400, hole=0.6)
                    donut.update_traces(textinfo='none')
                    st.plotly_chart(donut, use_container_width=True)

                st.write("#### Taxas de administração")
                coluna1, coluna2, coluna3, coluna4 = st.columns(4)
                with coluna1:
                    st.metric("Taxa de administração", f"{round(receita_prevista*100/vgl,2)} %", f"{round(saldo_receita*100/saldo_aluguel,2)} %")
                with coluna2:
                    st.metric("Taxa (residenciais)", f"{round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Residencial')]['Valor taxa de administração'].sum()/contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Residencial')]['Valor do aluguel'].sum(),2)} %", f"{round(saldo_receita*100/saldo_aluguel,2)} %")
                with coluna3:
                    st.metric("Taxa (comerciais)", f"{round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Comercial')]['Valor taxa de administração'].sum()/contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Comercial')]['Valor do aluguel'].sum(),2)} %", f"{round(saldo_receita*100/saldo_aluguel,2)} %")
                with coluna4:
                    st.metric("Taxa (outros)", f"{round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] != 'Residencial') & (contratosativos['Tipo de contrato'] != 'Comercial')]['Valor taxa de administração'].sum()/contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] != 'Residencial') & (contratosativos['Tipo de contrato'] != 'Comercial')]['Valor do aluguel'].sum(),2)} %", f"{round(saldo_receita*100/saldo_aluguel,2)} %")

                st.write("#### Contratos por tipo de contrato")

                df1 = histogramas('Tipo de contrato', 'Contratos')
                coluna1, coluna2 = st.columns(spec=[2,3])
                with coluna1:
                    st.write(df1[['Tipo de contrato', 'Contratos']])
                with coluna2:
                    donut = px.pie(df1[['Tipo de contrato', 'Contratos']], names='Tipo de contrato', values='Contratos', height=400, hole=0.6)
                    st.plotly_chart(donut, use_container_width=True)

                st.write("#### Médias de aluguel")
                coluna1, coluna2, coluna3, coluna4 = st.columns(4)
                with coluna1:
                    st.metric("Média de aluguel", f"RS {round(contratosativos['Valor do aluguel'].mean(), 2)}")
                with coluna2:
                    st.metric("Média aluguel (residenciais)",
                              f"R$ {round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Residencial')]['Valor do aluguel'].mean(), 2)}")
                with coluna3:
                    st.metric("Média aluguel (comerciais)",
                              f"R$ {round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] == 'Comercial')]['Valor do aluguel'].mean(), 2)}")
                with coluna4:
                    st.metric("Média aluguel (outros)",
                              f"R$ {round(contratosativos.loc[(contratosativos['Contrato ativo'] == 'Sim') & (contratosativos['Tipo de contrato'] != 'Residencial') & (contratosativos['Tipo de contrato'] != 'Comercial')]['Valor do aluguel'].mean(), 2)}")

                st.write("#### Top contratos (resumido)")
                st.write("Abaixo você verá uma relação dos clientes rankeados em relação a taxa de administração (valor total), para alterar o critério de rankeamento, basta **clicar na coluna** que deseja usar como prioridade. Essa é uma versão resumida dos contratos, caso você deseje ter acesso a uma versão mais completa com seus dados, basta clicar na aba Dados, no topo desta página.")
                df = contratosativos.loc[:,['Nome do proprietário', 'Bairro', 'Valor do aluguel', 'Valor taxa de administração']].sort_values(by='Valor taxa de administração', ascending=False)
                st.dataframe(df)


            else:
                st.write("Insira seus dados na barra lateral e salve")


        with segmentado:
            if isinstance(contratos, pd.DataFrame):
                st.header("Análises segmentadas")
                resumo_receita = contratosativos['Valor taxa de administração'].describe()
                resumo_vgl = contratosativos['Valor do aluguel'].describe()
                resumo_tempo = contratosativos['Tempo de contrato'].describe()
                st.write("#### Análise de quartis")
                st.write("Análise detalhada de quartis de **Receita de taxa de locação, aluguel e tempo de contrato**")
                coluna1, coluna2, coluna3 = st.columns(spec=[1.5,1,1])
                with coluna1:
                    st.write(resumo_receita)
                with coluna2:
                    st.write(resumo_vgl)
                with coluna3:
                    st.write(resumo_tempo)

                st.write("#### Análise de relação entre valor do aluguel e taxa de administração")
                scatterplot = px.scatter(
                    x=contratosativos['Valor taxa de administração'],
                    y=contratosativos['Valor do aluguel'],
                    color=contratosativos['Tipo de contrato']
                )
                st.plotly_chart(scatterplot, theme="streamlit", use_container_width=True)

                bairros = histogramas('Bairro / Cidade / Estado', 'Contratos')
                tipo_contrato = histogramas('Tipo de contrato', 'Contratos')
                tipo_imovel = histogramas('Tipo de imóvel', 'Contratos')

                fig = px.bar(
                    bairros.head(10),
                    title= 'Top 10 bairros em número de contratos',
                    x="Contratos",
                    y="Bairro / Cidade / Estado",
                    orientation='h'
                )
                fig.update_layout(yaxis_categoryorder='total ascending')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                st.write("#### Dados detalhados por bairro (todos os bairros)")
                st.write(bairros)
                fig2 = px.bar(
                    tipo_contrato.head(10),
                    title='Top 10 tipos de contrato em número de contratos',
                    x="Contratos",
                    y="Tipo de contrato",
                    orientation='h'
                )
                fig2.update_layout(yaxis_categoryorder='total ascending')
                st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

                st.write("#### Dados detalhados por tipo de contrato (todos os tipos)")
                st.write(tipo_contrato)
                fig3 = px.bar(
                    tipo_imovel.head(10),
                    title='Top 10 tipos de imóveis em número de contratos',
                    x="Contratos",
                    y="Tipo de imóvel",
                    orientation='h'
                )
                fig3.update_layout(yaxis_categoryorder='total ascending')
                st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

                st.write("#### Dados detalhados por tipo de imóvel (todos os tipos)")
                st.write(tipo_imovel)

        # Aba de dados
        with dados:
            if isinstance(contratos, pd.DataFrame):
                st.header("Dados dos contratos")
                st.write("Aqui você encontra todos os dados dos seus contratos. Você pode filtrar as colunas desejadas, colocar em tela cheia ou até mesmo fazer o download dos dados em formato de planilha.")

                colunas = contratos.columns.tolist()
                colunas_selecionadas = st.multiselect("Escolha os dados que deseja ver", colunas, colunas)
                dataframedados(colunas_selecionadas, contratos)

                if st.button('Baixar CSV'):
                    contratos = atualiza_contratos()
                    # Cria um link para o download do CSV
                    csv = contratos.to_csv("contratos.csv")
                    st.download_button(label="Clique para baixar CSV", data=csv, key='csv')
else:
    st.header("Conecte sua licença Superlógica")
    st.write('Clique ao lado em Minha conta e leia as instruções.')

