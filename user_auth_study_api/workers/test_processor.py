import data_processor

print("--- INICIANDO TESTE DO PROCESSADOR ---")
data_processor.processar_simba_extrato("./ExtratoDetalhado.csv", caso_id=1)
data_processor.processar_sittel_drt("./Detalhamento dos Registros Telef nicos.csv", caso_id=1)
data_processor.processar_sittel_cadastro("./Cadastros dos Assinantes.csv", caso_id=1)
data_processor.processar_rif_envolvidos("./RIF999888_Envolvidos.csv", caso_id=1, nome_arquivo="RIF999888_Envolvidos.csv")