import os
import xmltodict
import pandas as pd
from datetime import datetime

xml_errors = []

def process_xml_files(xml_directory):
    df_final = pd.DataFrame()

    for nome_arquivo in os.listdir(xml_directory):
        try:
            if nome_arquivo.endswith('.xml'):
                caminho_arquivo = os.path.join(xml_directory, nome_arquivo)

                with open(caminho_arquivo, 'r') as xml_file:
                    xml_dict = xmltodict.parse(xml_file.read())

                    NFe = xml_dict['ConsultarNfseResposta']['ListaNfse']['CompNfse']['Nfse']['InfNfse']

                    data_emissao = NFe['DataEmissao'].replace('Z', '')  # Remove 'Z' da string
                    data_formatada = datetime.strptime(data_emissao, '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y')

                    codigo_verificacao = NFe['CodigoVerificacao']
                    numero_nfse = NFe['Numero']
                    razao_social_tomador = NFe['TomadorServico']['RazaoSocial']
                    cpf_cnpj_tomador = NFe['TomadorServico']['IdentificacaoTomador']['CpfCnpj']['Cnpj']
                    codigo_municipio_tomador = NFe['TomadorServico']['Endereco']['CodigoMunicipio']
                    razao_social_prestador = NFe['PrestadorServico']['RazaoSocial']
                    optante_simples_nacional = NFe['OptanteSimplesNacional']
                    cpf_cnpj_prestador = NFe['PrestadorServico']['IdentificacaoPrestador']['Cnpj']
                    codigo_municipio_prestador = NFe['PrestadorServico']['Endereco']['CodigoMunicipio']
                    inscricao_municipal_prestador = NFe['PrestadorServico']['IdentificacaoPrestador'][
                        'InscricaoMunicipal']
                    codigo_tributacao = NFe['Servico']['CodigoTributacaoMunicipio']
                    descricao_codigo_tributacao = NFe['Servico']['Discriminacao']

                    # Se diferente de vazio armazene o dado, se não retorne 0
                    valor_servicos = NFe['Servico']['Valores']['ValorServicos']
                    if valor_servicos is not None:
                        valor_servicos = float(valor_servicos)
                    else:
                        valor_servicos = 0

                    valor_iss = NFe['Servico']['Valores'].get('ValorIss')
                    if valor_iss is not None:
                        valor_iss = float(valor_iss)
                    else:
                        valor_iss = 0

                    valor_ir = NFe['Servico']['Valores'].get('ValorIr')
                    if valor_ir is not None:
                        valor_ir = float(valor_ir)
                    else:
                        valor_ir = 0

                    valor_csll = NFe['Servico']['Valores'].get('ValorCsll')
                    if valor_csll is not None:
                        valor_csll = float(valor_csll)
                    else:
                        valor_csll = 0

                    valor_iss_retido = NFe['Servico']['Valores'].get('IssRetido')
                    if valor_iss_retido is not None:
                        valor_iss_retido = float(valor_iss_retido)
                    else:
                        valor_iss_retido = 0

                    aliquota = NFe['Servico']['Valores'].get('Aliquota')
                    if aliquota is not None:
                        aliquota = float(aliquota)
                    else:
                        aliquota = 0

                    valor_liquido_nfse = NFe['Servico']['Valores'].get('ValorLiquidoNfse')
                    if valor_liquido_nfse is not None:
                        valor_liquido_nfse = float(valor_liquido_nfse)
                    else:
                        valor_liquido_nfse = 0

                print(f'Registrado com sucesso para o {nome_arquivo}')

                # Cria a estrutura da planilha
                df = pd.DataFrame({
                    'Empresa': [razao_social_tomador],
                    'DataEmissao': [data_formatada],
                    'NotaFiscal': [numero_nfse],
                    'CnpjPrestador': [cpf_cnpj_prestador],
                    'CodigoServicoMunicipal': [codigo_tributacao],
                    'Descrição': [descricao_codigo_tributacao],
                    'CnpjFilial': [cpf_cnpj_tomador],
                    'Fornecedor': [razao_social_prestador],
                    'ValorServico': [valor_servicos],
                    'ValorIss': [valor_iss],
                    'ValorIr': [valor_ir],
                    'ValorCsll': [valor_csll],
                    'ValorIssRetido': [valor_iss_retido],
                    'AliquotaIss': [aliquota],
                    'MunicipioPrestadorId': [codigo_municipio_prestador],
                    'OptantePeloSimples': [optante_simples_nacional]
                })

                # Define o nome do arquivo
                nome_arquivo_xlsx = f"{os.path.splitext(nome_arquivo)[0]}.xlsx"
                caminho_arquivo_xlsx = os.path.join(xml_directory, nome_arquivo_xlsx)
                # df.to_excel(caminho_arquivo_xlsx, encoding='utf-8', index=False)

                # df_final.fillna(0, inplace=True)
                df_final = pd.concat([df_final, df])

        except Exception as e:
            print(f'Não processado {nome_arquivo}')

    # Gera um arquivo Excel com todas as informações processadas
    df_final.to_excel('todos.xlsx', index=False)

# Chamada da função com o diretório desejado
if __name__ == "__main__":
    diretorio_xml = r"C:\Users\wallingson.silva\Downloads\XMLLLL\importados"
    process_xml_files(diretorio_xml)