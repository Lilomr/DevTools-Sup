dbList_default =   ['cerbero_1',   'cerbero_2',   'cerbero_3',   'cerbero_4',   'cerbero_5', 
                    'cerbero_6',   'cerbero_7',   'cerbero_8',   'cerbero_9',   'cerbero_10', 
                    'cerbero_11',  'cerbero_12',  'cerbero_20',  'cerbero_22',  'cerbero_23', 
                    'cerbero_24',  'cerbero_25',  'cerbero_26',  'cerbero_28',  'cerbero_29', 
                    'cerbero_30',  'cerbero_31',  'cerbero_33',  'cerbero_34',  'cerbero_40', 
                    'cerbero_41',  'cerbero_42',  'cerbero_43',  'cerbero_45',  'cerbero_46', 
                    'cerbero_47',  'cerbero_49',  'cerbero_50',  'cerbero_54',  'cerbero_56', 
                    'cerbero_57',  'cerbero_61',  'cerbero_62',  'cerbero_65',  'cerbero_66', 
                    'cerbero_68',  'cerbero_70',  'cerbero_71',  'cerbero_73',  'cerbero_75', 
                    'cerbero_76',  'cerbero_77',  'cerbero_80',  'cerbero_83',  'cerbero_86', 
                    'cerbero_88',  'cerbero_89',  'cerbero_90',  'cerbero_93',  'cerbero_94', 
                    'cerbero_98',  'cerbero_99',  'cerbero_102', 'cerbero_103', 'cerbero_104', 
                    'cerbero_106', 'cerbero_107', 'cerbero_108', 'cerbero_109', 'cerbero_110', 
                    'cerbero_111', 'cerbero_112', 'cerbero_113', 'cerbero_114', 'cerbero_115', 
                    'cerbero_116', 'cerbero_117', 'cerbero_118', 'cerbero_119', 'cerbero_120', 
                    'cerbero_121', 'cerbero_122', 'cerbero_123', 'cerbero_124', 'cerbero_125', 
                    'cerbero_126', 'cerbero_127', 'cerbero_128', 'cerbero_129', 'cerbero_130', 
                    'cerbero_131', 'cerbero_132', 'cerbero_133', 'cerbero_134', 'cerbero_135', 
                    'cerbero_136', 'cerbero_137', 'cerbero_138', 'cerbero_139', 'cerbero_140', 
                    'cerbero_141', 'cerbero_142', 'cerbero_143', 'cerbero_144', 'cerbero_145', 
                    'cerbero_146', 'cerbero_147', 'cerbero_148', 'cerbero_149', 'cerbero_150', 
                    'cerbero_151', 'cerbero_152', 'cerbero_153', 'cerbero_154', 'cerbero_155', 
                    'cerbero_156', 'cerbero_157', 'cerbero_158', 'cerbero_159', 'cerbero_160', 
                    'cerbero_161', 'cerbero_162', 'cerbero_163', 'cerbero_164', 'cerbero_165', 
                    'cerbero_166', 'cerbero_167', 'cerbero_168', 'cerbero_169', 'cerbero_170', 
                    'cerbero_171', 'cerbero_172', 'cerbero_173', 'cerbero_174']

tipo_integracao_default = {
    0: "DELAGE",
    1: "VIA_LOGICA",
    2: "INFARMA",
    3: "GESTCOM",
    5: "DUAL",
    6: "EFW",
    7: "ENSIS",
    8: "FOX_DATA",
    10: "INFARMA_MULTI_EMPRESAS",
    11: "WINTHOR",
    12: "PROTON",
    13: "SEMPRE_SISTEMAS",
    14: "SOLUMA",
    15: "ST",
    16: "AVISNET",
    17: "ALLY_WEB",
    18: "SAP",
    19: "PRATS-PROTHEUS",
    20: "SANKYA",
    21: "POTI",
    23: "POTY_MULTI_EMPRESAS",
    24: "OLIMPUS",
    25: "FLUXIS",
    26: "WIIZI"
}

tipo_migracao_default = {
    0: "COMPLETA",
    1: "CLIENTE",
    2: "ESTOQUE",
    3: "PEDIDO",
    4: "ARTVENDAS",
    5: "RETORNO",
    6: "REPOSICAO_PRODUTO",
    7: "KIT"
}

tipo_migracao = tipo_migracao_default
tipo_integracao = tipo_integracao_default
dbList = dbList_default

union = 'UNION'
unionAll = 'UNION ALL'
newLine = '\n'
flag_max = 200

initView = 'vw_'
integracao_cliente_ativo = 'integracao_cliente_ativo'
flag_cliente = 'flag_cliente'
fila_pedidos = 'fila_pedidos'
erro_pedidos = 'erro_pedidos'
vendedor_versao_app = 'vendedor_versao_app'
empresa_usuario_cliente_modulo = 'empresa_usuario_cliente_modulo'
migracao_erro = 'migracao_erro'
migracao_cliente_inativo = 'agendamento_migracao_cliente_inativo'
flag_aux = 'flag_aux'

timer_cliente_ativo = 'SYSDATE() - INTERVAL 90 DAY'
timer_fila_pedidos = 'SYSDATE() - INTERVAL 10 DAY'
timer_erro_pedidos = 'SYSDATE() - INTERVAL 30 DAY'
timer_migracao_erro = 'SYSDATE() - INTERVAL 10 DAY'

divimed_db = 'artnew.dbo.'
divimed_table = 'clientes_filtro_neoquimica'

divimed_cnpj = []
#with open('txt/clientes.txt', 'r') as f:
    #divimed_cnpj = f.read().splitlines()

divimed_max_array = 500

############################################MODIFICAVEIS###########################################

def setDefault():
    dbList = dbList_default
    flag_max = 200
    timer_cliente_ativo = 'SYSDATE() - INTERVAL 90 DAY'
    timer_fila_pedidos = 'SYSDATE() - INTERVAL 10 DAY'
    timer_erro_pedidos = 'SYSDATE() - INTERVAL 30 DAY'
    timer_migracao_erro = 'SYSDATE() - INTERVAL 10 DAY'
    divimed_cnpj = []
    #with open('txt/clientes.txt', 'r') as f:
        #divimed_cnpj = f.read().splitlines()

    divimed_max_array = 500