from django.db import connection

# =====================================================================
# 1. TABELAS AUXILIARES (CHAVES ESTRANGEIRAS)
# =====================================================================

def listar_tipos_utilizador():
    """Procura os tipos de utilizador na tabela 'UserTypes'"""
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_tipo, designacao FROM "UserTypes";')
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

def listar_empresas():
    """Procura as empresas na tabela 'companies' mapeando o id e o nome corretos"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT id AS id_empresa, nome FROM companies;")
        colunas = [col.name for col in cursor.description]
        # CORRIGIDO: mudou 'tabular' para 'linha' para bater certo com o zip
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]



# =====================================================================
# 2. CRUD DA TABELA USERS (TOTALMENTE ALINHADO COM A SUA IMAGEM)
# =====================================================================

# C - CREATE
def criar_utilizador(email, password, name, telephone, active, id_tipo, id_empresa):
    """Insere um novo utilizador respeitando a estrutura de tipos exata"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO "Users" (email, password, name, telephone, active, "Date_created", id_tipo, id_empresa)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s);
            """,
            [email, password, name, telephone, active, id_tipo, id_empresa]
        )

# R - READ ALL
def listar_todos_utilizadores():
    """Lista todos os utilizadores usando aspas duplas nas colunas mistas"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT "id_Utilizador", email, password, name, telephone, active, "Date_created", id_tipo, id_empresa 
            FROM "Users";
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

# R - READ ONE
def obtener_utilizador_por_id(id_utilizador):
    """Procura um utilizador específico pelo seu ID"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT "id_Utilizador", email, password, name, telephone, active, "Date_created", id_tipo, id_empresa 
            FROM "Users" 
            WHERE "id_Utilizador" = %s;
            """, 
            [id_utilizador]
        )
        linha = cursor.fetchone()
        if linha:
            colunas = [col.name for col in cursor.description]
            return dict(zip(colunas, linha))
        return None

# U - UPDATE
def atualizar_utilizador(id_utilizador, email, name, telephone, active, id_tipo, id_empresa):
    """Atualiza os dados de um utilizador existente na tabela 'Users'"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE "Users"
            SET email = %s, name = %s, telephone = %s, active = %s, id_tipo = %s, id_empresa = %s
            WHERE "id_Utilizador" = %s;
            """,
            [email, name, telephone, active, id_tipo, id_empresa, id_utilizador]
        )

# D - DELETE
def eliminar_utilizador(id_utilizador):
    """Remove permanentemente o utilizador da tabela 'Users'"""
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM "Users" WHERE "id_Utilizador" = %s;', [id_utilizador])
