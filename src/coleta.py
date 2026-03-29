import requests
import pandas as pd
import time

# 1. Mapeamento de Instituições
INSTITUICOES = {
    'Banco Master': '33923798',
    'Itaú Unibanco': '60701190',
    'BTG Pactual': '30306294',
    'Banco do Brasil': '00000000',
    'Bradesco': '60746948',
    'Santander': '90400888'
}

# 2. Definição de Parâmetros
TRIMESTRES = [202203, 202206, 202209, 202212, 202303, 202306, 202309, 202312, 202403, 202406, 202409, 202412]
TIPOS_INSTITUICAO = [1, 2, 3]
REPORT_IDS = ['1', '2', '3', '4', '5']
BASE_URL = "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/"

dados_consolidados_lista = []

print("🚀 Iniciando Pipeline de Extração Unificado...")

# 3. Pipeline de Extração
for nome_banco, cod_inst in INSTITUICOES.items():
    print(f"\nExtraindo dados para: {nome_banco} ({cod_inst})")
    contador_banco = 0

    for trimestre in TRIMESTRES:
        for tipo in TIPOS_INSTITUICAO:
            for rel in REPORT_IDS:
                endpoint = f"IfDataValores(AnoMes={trimestre},TipoInstituicao={tipo},Relatorio='{rel}')"
                filtros = f"?$filter=CodInst eq '{cod_inst}'&$format=json"
                url = BASE_URL + endpoint + filtros

                try:
                    # 4. Tratamento de erros e timeouts
                    response = requests.get(url, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        resultados = data.get('value', [])

                        if resultados:
                            # 5. Armazenamento com Identificador
                            for item in resultados:
                                item['Instituicao'] = nome_banco
                                item['Trimestre'] = trimestre
                                item['RelatorioID'] = rel
                                dados_consolidados_lista.append(item)
                            contador_banco += len(resultados)
                except Exception:
                    # Continuidade em caso de falha pontual
                    continue

    print(f"✅ {nome_banco}: {contador_banco} registros recuperados.")

# 6. Conversão e Resumo Final
df_consolidado = pd.DataFrame(dados_consolidados_lista)

print("\n--- Resumo da Consolidação ---")
if not df_consolidado.empty:
    resumo = df_consolidado.groupby('Instituicao').size().reset_index(name='Total Registros')
    print(resumo)
    print(f"\nTotal Geral de Registros: {len(df_consolidado)}")
else:
    print("Nenhum dado foi extraído. Verifique os parâmetros ou a conexão.")


for instituicao in df_consolidado['Instituicao'].unique():
    df_instituicao = df_consolidado[df_consolidado['Instituicao'] == instituicao].copy()

    # Sanitizar o nome do arquivo para evitar caracteres especiais
    file_name = f"extracao_{instituicao.replace(' ', '_').replace('/', '_')}.csv"
    file_path = f"/content/{file_name}"

    df_instituicao.to_csv(file_path, index=False, encoding='utf-8')
    print(f'✅ Arquivo {file_name} exportado com sucesso para {file_path}')

print('\n--- Exportação Concluída ---')
print('Todos os arquivos CSV foram gerados com sucesso.')