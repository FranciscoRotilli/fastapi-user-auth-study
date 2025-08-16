import pandas as pd
import numpy as np

def _read_csv_robust(file_path: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(file_path, delimiter=';')
    except UnicodeDecodeError:
        print(f"DEBUG: Encoding UTF-8 falhou para {file_path}. Tentando latin1.")
        try:
            return pd.read_csv(file_path, delimiter=';', encoding='latin1')
        except Exception as e:
            print(f"ERRO: Falha ao ler o arquivo CSV {file_path} com todos os encodings. Erro: {e}")
            return None
    except Exception as e:
        print(f"ERRO: Falha ao ler o arquivo CSV {file_path}. Erro: {e}")
        return None
    
def processar_simba_extrato(file_path: str, caso_id: int):
    print(f"\n--- Processando SIMBA Extrato para o Caso {caso_id} ---")
    df = _read_csv_robust(file_path)
    if df is None:
        return

    colunas_essenciais = ['CPF_CNPJ_TITULAR', 'CPF_CNPJ_OD']
    df_vinculos = df[colunas_essenciais]

    df_limpo = df_vinculos.dropna(subset=colunas_essenciais)

    df_filtrado = df_limpo[df_limpo['CPF_CNPJ_TITULAR'] != df_limpo['CPF_CNPJ_OD']]

    vinculos_agregados = df_filtrado.groupby(colunas_essenciais).size().reset_index(name='forca')

    print(f"Encontrados {len(vinculos_agregados)} vínculos únicos de transação.")
    
    for index, row in vinculos_agregados.iterrows():
        origem = row['CPF_CNPJ_TITULAR']
        destino = row['CPF_CNPJ_OD']
        forca = row['forca']
        
        # TODO: Chamada para o banco
        print(f"  > Vínculo SIMBA: ({origem}) -[TRANSFERIU {{forca: {forca}}}]-> ({destino})")


def processar_sittel_drt(file_path: str, caso_id: int):
    print(f"\n--- Processando SITTEL DRT para o Caso {caso_id} ---")
    df = _read_csv_robust(file_path)
    if df is None:
        return

    df.replace('-', np.nan, inplace=True)

    df['Participante_Origem'] = df['Atribuído a'].fillna(df['Assinante (A)'])
    df['Participante_Destino'] = df['Atribuído a.1'].fillna(df['Assinante (A).1'])

    df_ligacoes = df[['Participante_Origem', 'Participante_Destino']].dropna()
    print(f"Encontrados {len(df_ligacoes)} vínculos de ligação.")
    for index, row in df_ligacoes.iterrows():
        origem = row['Participante_Origem']
        destino = row['Participante_Destino']
        
        # TODO: Chamada para o banco
        print(f"  > Vínculo de Ligação: ({origem}) -[:LIGOU_PARA]-> ({destino})")
        
    df_posse = df[['Assinante (A)', 'Atribuído a', 'Terminal']].dropna(subset=['Terminal'])
    print(f"Encontradas {len(df_posse)} relações de posse/uso de terminal.")
    for index, row in df_posse.iterrows():
        terminal = row['Terminal']
        assinante = row['Assinante (A)']
        atribuido = row['Atribuído a']

        if pd.notna(assinante):
            # TODO: Chamada para o banco
            print(f"  > Vínculo de Posse: ({assinante}) -[:É_ASSINANTE_DE]-> ({terminal})")
        if pd.notna(atribuido):
            # TODO: Chamada para o banco
            print(f"  > Vínculo de Uso: ({atribuido}) -[:UTILIZA]-> ({terminal})")


def processar_sittel_cadastro(file_path: str, caso_id: int):
    print(f"\n--- Processando SITTEL Cadastros para o Caso {caso_id} ---")
    df = _read_csv_robust(file_path)
    if df is None:
        return

    df_filtrado = df[~df['Investigado'].str.contains('CGI', na=False)]
    
    print(f"Encontrados {len(df_filtrado)} registros de cadastro válidos (sem CGI).")

    for index, row in df_filtrado.iterrows():
        assinante = row['Assinante']
        cpf_cnpj = row['CPF/CNPJ']
        terminal = row['Terminal']

        # TODO: Chamada para o banco
        print(f"  > Vínculo Cadastral: ({assinante}) -[:TEM_CPF_CNPJ]-> ({cpf_cnpj})")
        print(f"  > Vínculo Cadastral: ({assinante}) -[:É_ASSINANTE_DE]-> ({terminal})")


def processar_rif_envolvidos(file_path: str, caso_id: int, nome_arquivo: str):
    print(f"\n--- Processando RIF Envolvidos para o Caso {caso_id} ---")
    df = _read_csv_robust(file_path)
    if df is None:
        return

    num_rif = ''.join(filter(str.isdigit, nome_arquivo)) or df['Nº RIF'].iloc[0]
    
    print(f"Encontrados {len(df)} envolvidos no RIF Nº {num_rif}.")

    for index, row in df.iterrows():
        cpf_cnpj = row['cpfCnpjEnvolvido']
        nome = row['nomeEnvolvido']
        tipo_envolvimento = row['tipoEnvolvido']

        # TODO: Chamada para o banco
        print(f"  > Vínculo RIF: ({cpf_cnpj} - {nome}) -[:ENVOLVIDO_NO_RIF {{tipo: '{tipo_envolvimento}'}}]-> (RIF {num_rif})")
