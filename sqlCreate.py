import zipfile
from io import BytesIO
import os
import static.properties.variaveis as var

url_dev_sup = 'static/convertidos/'

def createZip(urlPath, filesList):
    zipName = ""
    if urlPath == "views": zipName = "viewsAws.zip"
    elif urlPath == "insert": zipName = "insert.zip"

    zipFinal = BytesIO()
    zipFinal.name = zipName
    with zipfile.ZipFile(zipFinal, 'w') as zipf:
        for file in filesList:
            if file is not None:
                zipf.writestr(file.name, file.read())
                #print(f'{file.name} adicionado ao zipIO com sucesso!')
        return zipFinal

###########################################VIEWS###########################################

def runViews():
    fileList = [integracaoClienteAtivo()
                ,flagCliente()
                ,filaPedidos()
                ,erroPedidos()
                ,vendedorVersaoApp()
                ,empresaUsuarioClienteModulo()
                ,migracaoErro()
                ,MigracaoClienteInativo()
                ,flagAux()]
    return createZip("views", fileList)

def gravandoIoFile (viewName, result):
        file = BytesIO()
        file.write(result.encode('utf-8'))
        file.seek(0)
        file.name = fr'{viewName}.sql'
        #print(fr'ByteIO {file.name} criada com sucesso!')
        return file


def integracaoClienteAtivo():
    caseTipoIntegracao = fr'{var.newLine}CASE {var.newLine}'
    for key, value in var.tipo_integracao.items():
        caseTipoIntegracao += fr"    WHEN a.emTipoIntegracao = {key} THEN '{value}'{var.newLine}"
    caseTipoIntegracao += fr"END AS Integracao{var.newLine}"
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.integracao_cliente_ativo} AS {var.newLine}"
    result += fr"""SELECT T.conta AS Id, a.identificadorConta, a.emTipoIntegracao, {caseTipoIntegracao}FROM ({var.newLine}"""

    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"   (SELECT {conta.split('_')[1]} as conta FROM {conta}.pedido_temp p WHERE p.statuspedido in (4,11) AND p.dataEnvioPedido > {var.timer_cliente_ativo} LIMIT 1) {union}{var.newLine}"

    result += fr") T INNER JOIN cerbero_artnew.conta a on T.conta = a.id ORDER BY a.emTipoIntegracao, T.conta"

    return gravandoIoFile(fr'{var.integracao_cliente_ativo}', result=result)

def flagCliente():
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.flag_cliente} AS {var.newLine}"
    result += fr"""SELECT DISTINCT t.conta AS id, c.identificadorConta,
    SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(flag, '|-|', t.id),'|-|', -1), '=', 1) AS flag,
    SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(flag, '|-|', t.id),'|-|', -1), '=', -1) AS valor
FROM ({var.newLine}"""
    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"""    SELECT {conta.split('_')[1]} AS conta, t.id, REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(configuracaoafv, '#.*\n', ''), '\n', '|-|'), '|-||-|', '|-|') AS flag
	FROM {conta}.configuracao_modulo cm CROSS JOIN cerbero_artnew.{var.initView}{var.flag_aux} t WHERE cm.modulo_id = 8 
		AND t.id <= (LENGTH(REGEXP_REPLACE(REGEXP_REPLACE(configuracaoafv, '#.*\n', ''), '\n', '|-|')) - LENGTH(REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(configuracaoafv, '#.*\n', ''), '\n', '|-|'), '|-|', ''))) / LENGTH('|-|') {union}{var.newLine}"""
    result += fr") t INNER JOIN cerbero_artnew.conta c ON c.id = t.conta AND SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(flag, '|-|', t.id),'|-|', -1), '=', 1) <> ''"
    
    return gravandoIoFile(fr'{var.flag_cliente}', result=result)

def filaPedidos():
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.fila_pedidos} AS {var.newLine}"
    result += fr"SELECT t.conta, a.identificadorConta, COUNT(t.id) AS Qtd_Fila, MIN(CAST(t.dataenviopedido AS DATE)) AS Primeiro, MAX(CAST(t.dataenviopedido AS DATE)) AS Ultimo  FROM ({var.newLine}"
    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"SELECT {conta.split('_')[1]} as conta ,p.id, p.dataenviopedido FROM {conta}.pedido_temp p WHERE p.statuspedido in (8) {union}{var.newLine}"
    result += fr") t INNER JOIN cerbero_artnew.conta a on t.conta = a.id WHERE t.dataenviopedido > {var.timer_fila_pedidos} GROUP BY t.conta, a.identificadorConta ORDER BY Primeiro ASC"

    return gravandoIoFile(fr'{var.fila_pedidos}', result=result)

def erroPedidos():
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.erro_pedidos} AS {var.newLine}"
    result += fr"SELECT t.conta, a.identificadorConta, COUNT(t.id) AS Qtd_Erros, MIN(CAST(t.dataenviopedido AS DATE)) AS Primeiro, MAX(CAST(t.dataenviopedido AS DATE)) AS Ultimo  FROM ({var.newLine}"
    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"SELECT {conta.split('_')[1]} as conta ,p.id, p.dataenviopedido FROM {conta}.pedido_temp p WHERE p.statuspedido in (12) {union}{var.newLine}"
    result += fr") t INNER JOIN cerbero_artnew.conta a on t.conta = a.id WHERE t.dataenviopedido > {var.timer_erro_pedidos} GROUP BY t.conta, a.identificadorConta ORDER BY Primeiro ASC"

    return gravandoIoFile(fr'{var.erro_pedidos}', result=result)

def vendedorVersaoApp():
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.vendedor_versao_app} AS {var.newLine}"
    result += fr"SELECT a.id AS Id, a.identificadorConta AS identificadorConta, T.vendedor_id, T.vendedor_nome, T.versao_aplicativo, T.is_Beta FROM ({var.newLine}"
    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"""SELECT {conta.split('_')[1]} AS conta, v.vendedor_id, vend.nome AS vendedor_nome, MAX(SUBSTRING(v.versaoaplicativo,1,8)) AS versao_aplicativo, CASE WHEN MAX(SUBSTRING(v.versaoaplicativo,9,5)) <> '' THEN TRUE ELSE FALSE END AS is_Beta
FROM {conta}.versao v INNER JOIN {conta}.vendedor vend ON vend.codigoVendedor = v.vendedor_id WHERE v.dataregistro = 
(SELECT max(v2.dataregistro) FROM {conta}.versao v2 WHERE v2.vendedor_id = v.vendedor_id) AND SUBSTRING(v.versaoaplicativo,1,1) = '8'
group by vend.nome, v.vendedor_id {union}{var.newLine}"""
    result += fr") T INNER JOIN cerbero_artnew.conta a ON a.id = T.conta ORDER BY a.id, T.versao_aplicativo DESC"

    return gravandoIoFile(fr'{var.vendedor_versao_app}', result=result)

def empresaUsuarioClienteModulo():
    count = 0
    union = var.union
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.empresa_usuario_cliente_modulo} AS {var.newLine}"
    result += fr"SELECT T.conta, ca.identificadorConta, ca.Integracao, m.id as modulo_id, m.chave, u.id AS usuario_id, u.email, u.nome, T.cliente_id, T.cpfCnpj, T.razaoSocial FROM ({var.newLine}"
    for conta in var.dbList:
        count += 1
        if count == len(var.dbList):
            union = ''
        result += fr"""     SELECT {conta.split('_')[1]} AS conta, ucm.cliente_id, c.cpfCnpj, c.razaoSocial, ucm.usuario_id, ucm.modulo_id  
	    FROM {conta}.usuario_cliente_modulo ucm
	    INNER JOIN {conta}.cliente c ON ucm.cliente_id = c.id {union}{var.newLine}"""
    result += fr""") T 	INNER JOIN cerbero_artnew.usuario u ON T.usuario_id = u.id
	INNER JOIN cerbero_artnew.modulo m ON m.id = T.modulo_id
	INNER JOIN cerbero_artnew.vw_integracao_cliente_ativo ca ON T.conta = ca.id
	ORDER BY ca.Integracao, T.conta, m.chave, u.id, T.cliente_id"""

    return gravandoIoFile(fr'{var.empresa_usuario_cliente_modulo}', result=result)

def migracaoErro():
    caseTipoMigracao = fr'{var.newLine}CASE {var.newLine}'
    for key, value in var.tipo_migracao.items():
        caseTipoMigracao += fr"    WHEN m.emTipoMigracao = {key} THEN '{value}'{var.newLine}"
    caseTipoMigracao += fr"    ELSE m.emTipoMigracao {var.newLine}END AS emTipoMigracao,"

    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.migracao_erro} AS {var.newLine}"
    result += fr"""SELECT a.id AS Id, a.identificadorConta AS identificadorConta, {caseTipoMigracao}
count(m.emTipoMigracao) AS qtd_Erros, 
CAST(max(m.dataRegistro) AS date) AS ultimoErro
FROM cerbero_artnew.conta a
INNER JOIN cerbero_artnew.auditoria_migracao m ON a.id = m.conta_id AND m.action = 1 AND m.dataRegistro >= {var.timer_migracao_erro}
WHERE a.id IN (SELECT v.Id FROM cerbero_artnew.{var.initView}{var.integracao_cliente_ativo} v)
GROUP BY a.id, a.identificadorConta, m.emTipoMigracao
ORDER BY a.id, m.emTipoMigracao;"""
    
    return gravandoIoFile(fr'{var.migracao_erro}', result=result)

def MigracaoClienteInativo():
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.migracao_cliente_inativo} AS {var.newLine}"
    result += fr"""SELECT a.id AS Id, a.identificadorConta AS identificadorConta, count(m.conta_id) AS Qtd_Agendamento
FROM cerbero_artnew.conta a
JOIN cerbero_artnew.agendamento_migracao m ON a.id = m.conta_id
WHERE a.id NOT IN (SELECT cerbero_artnew.v.Id FROM cerbero_artnew.{var.initView}{var.integracao_cliente_ativo} v)
GROUP BY a.id, a.identificadorConta
ORDER BY a.id;"""
    
    return gravandoIoFile(fr'{var.migracao_cliente_inativo}', result=result)

def flagAux():
    count = 0
    union = var.unionAll
    flagmax = var.flag_max
    result = fr"#CREATE OR REPLACE ALGORITHM = UNDEFINED VIEW cerbero_artnew.{var.initView}{var.flag_aux} AS {var.newLine}"
    result += fr"SELECT 1 AS id {union}{var.newLine}"
    for i in range(2, flagmax + 1):
        count += 1
        if count == (flagmax - 1):
            union = ''
        result += fr"SELECT {i} AS id {union}{var.newLine}" 

    return gravandoIoFile(fr'{var.flag_aux}', result=result)

###########################################INSERT###########################################

def RunInserts():
    fileList = [divimedClientes()]
    return createZip("insert", fileList)

def divimedClientes():
    count = 0
    arrayLength = 0
    countNewLine = 0
    union = fr','
    result = fr"""DROP TABLE IF EXISTS {var.divimed_db}{var.divimed_table};{var.newLine}CREATE TABLE {var.divimed_db}{var.divimed_table} (cnpj varchar(20));"""
    result += fr"{var.newLine}INSERT INTO {var.divimed_db}{var.divimed_table} (cnpj) VALUES{var.newLine}"
    for conta in var.divimed_cnpj:
        count += 1
        arrayLength += 1
        countNewLine += 1
        if count == len(var.divimed_cnpj):
            union = ''
        if arrayLength == var.divimed_max_array:
            arrayLength = 0
            countNewLine = 0
            result += fr"""('{conta}');{var.newLine}"""
            result += fr"{var.newLine}INSERT INTO {var.divimed_db}{var.divimed_table} (cnpj) VALUES{var.newLine}"
        elif countNewLine == 10 and count != len(var.divimed_cnpj):
            countNewLine = 0
            result += fr"""('{conta}'){union}{var.newLine}"""
        else:
            result += fr"""('{conta}'){union}"""
    result += fr";"
    
    return gravandoIoFile(fr'{var.divimed_table}', result=result)

###########################################PROPERTIES###########################################

def defaultProperties():
    var.setDefault()
    print("Propriedades resetadas para o padrão.")