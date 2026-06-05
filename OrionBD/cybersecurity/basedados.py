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

# =====================================================================
# 1. TABELAS AUXILIARES
# =====================================================================

def listar_tipos_pedido():
    """Procura os tipos de pedido na tabela 'RequestTypes'"""
    with connection.cursor() as cursor:
        cursor.execute('SELECT id AS id_tipo_pedido, name FROM public."RequestTypes";')
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


# =====================================================================
# 2. CRUD DA TABELA REQUESTS (TOTALMENTE ALINHADO COM O ESQUEMA REAL)
# =====================================================================

# C - CREATE
def criar_pedido(title, description, status, creator_id, id_tipo_pedido=None, assigned_to_id=None):
    """Insere um novo pedido com chaves estrangeiras dinâmicas e limpa o contador de IDs"""
    with connection.cursor() as cursor:
        # Sincroniza a sequência automática para evitar o IntegrityError
        cursor.execute('SELECT setval(pg_get_serial_sequence(\'public.requests\', \'id\'), COALESCE(MAX(id), 1)) FROM public.requests;')
        
        cursor.execute(
            """
            INSERT INTO public.requests ("subject", "description", "status", "openedAt", "creatorId", "requestTypeId", "assignedToId")
            VALUES (%s, %s, %s, NOW(), %s, %s, %s)
            RETURNING id;
            """,
            [title, description, status, creator_id, id_tipo_pedido, assigned_to_id]
        )
        return cursor.fetchone()[0]
# R - READ ALL
def listar_todos_pedidos():
    """Lista todos os pedidos mapeando os campos para o padrão do HTML"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, "subject" AS title, "description", "status", "openedAt" AS created_at, "creatorId" AS user_id 
            FROM public.requests;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

# R - READ ONE (Modificado para trazer os IDs de associação)
def obter_pedido_por_id(id_pedido):
    """Procura um pedido específico trazendo os IDs de criador e designado"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, "subject" AS title, "description", "status", "openedAt" AS created_at, 
                   "creatorId" AS creator_id, "requestTypeId" AS id_tipo_pedido, "assignedToId" AS assigned_to_id
            FROM public.requests 
            WHERE id = %s;
            """, 
            [id_pedido]
        )
        linha = cursor.fetchone()
        if linha:
            colunas = [col.name for col in cursor.description]
            return dict(zip(colunas, linha))
        return None

# U - UPDATE
def atualizar_pedido(id_pedido, title, description, status, id_tipo_pedido=None, creator_id=None, assigned_to_id=None):
    """Atualiza todas as propriedades e chaves estrangeiras de um pedido"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.requests
            SET "subject" = %s, "description" = %s, "status" = %s, 
                "requestTypeId" = %s, "creatorId" = %s, "assignedToId" = %s
            WHERE id = %s;
            """,
            [title, description, status, id_tipo_pedido, creator_id, assigned_to_id, id_pedido]
        )

# D - DELETE
def eliminar_pedido(id_pedido):
    """Remove permanentemente o pedido"""
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM public.requests WHERE id = %s;', [id_pedido])



# =====================================================================
# 3. CRUD DA TABELA DE FICHEIROS (REQUESTFILES - IMAGEM 2)
# =====================================================================

# C - CREATE (Upload de Ficheiro)
def adicionar_ficheiro_pedido(file_name, file_path, request_id):
    """Insere um novo ficheiro associado a um pedido (RequestFiles)"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO public."RequestFiles" ("fileName", "filePath", "uploadedAt", "requestId")
            VALUES (%s, %s, NOW(), %s);
            """,
            [file_name, file_path, request_id]
        )

# R - READ ALL BY REQUEST (Listar ficheiros de um pedido)
def listar_ficheiros_de_pedido(id_pedido):
    """Procura todos os ficheiros associados a um pedido específico"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, "fileName", "filePath", "uploadedAt", "requestId"
            FROM public."RequestFiles"
            WHERE "requestId" = %s;
            """,
            [id_pedido]
        )
        # CORREÇÃO: Usar fetchall() porque um pedido pode ter vários ficheiros,
        # e mapear corretamente cada linha obtida da BD.
        linhas = cursor.fetchall()
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, row)) for row in linhas]

# D - DELETE (Remover Ficheiro)
def eliminar_ficheiro_pedido(id_ficheiro):
    """Remove o registo de um ficheiro específico da base de dados"""
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM public."RequestFiles" WHERE id = %s;', [id_ficheiro])

# =====================================================================
# 3. CRUD DA TABELA DE EMPRESAS 
# =====================================================================

from django.db import connection

def obter_todas_empresas():
    """Retorna uma lista com todas as empresas da tabela companies"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nome, "nomeResponsavelSeg", "emailResponsavelSeg", 
                   "telefoneResponsavelSeg", "nomeContactoPerm", 
                   "emailContactoPerm", "telefoneContactoPerm"
            FROM companies; -- <--- Atualizado aqui
            """
        )
        return cursor.fetchall()

def criar_empresa(nome, nomeResponsavelSeg, emailResponsavelSeg, telefoneResponsavelSeg, nomeContactoPerm, emailContactoPerm, telefoneContactoPerm):
    """Insere uma nova empresa na tabela companies"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO companies ( -- <--- Atualizado aqui
                nome, "nomeResponsavelSeg", "emailResponsavelSeg", 
                "telefoneResponsavelSeg", "nomeContactoPerm", 
                "emailContactoPerm", "telefoneContactoPerm"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            [nome, nomeResponsavelSeg, emailResponsavelSeg, telefoneResponsavelSeg, nomeContactoPerm, emailContactoPerm, telefoneContactoPerm]
        )
        
connection.commit()

def obter_empresa_por_id(id_empresa):
    """Retorna os dados de uma empresa específica da tabela companies"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nome, "nomeResponsavelSeg", "emailResponsavelSeg", 
                   "telefoneResponsavelSeg", "nomeContactoPerm", 
                   "emailContactoPerm", "telefoneContactoPerm"
            FROM companies -- <--- Atualizado aqui
            WHERE id = %s;
            """,
            [id_empresa]
        )
        return cursor.fetchone()

def atualizar_empresa(id_empresa, nome, nomeResponsavelSeg, emailResponsavelSeg, telefoneResponsavelSeg, nomeContactoPerm, emailContactoPerm, telefoneContactoPerm):
    """Atualiza os dados de uma empresa na tabela companies"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE companies -- <--- Atualizado aqui
            SET 
                nome = %s,
                "nomeResponsavelSeg" = %s,
                "emailResponsavelSeg" = %s,
                "telefoneResponsavelSeg" = %s,
                "nomeContactoPerm" = %s,
                "emailContactoPerm" = %s,
                "telefoneContactoPerm" = %s
            WHERE id = %s;
            """,
            [nome, nomeResponsavelSeg, emailResponsavelSeg, telefoneResponsavelSeg, nomeContactoPerm, emailContactoPerm, telefoneContactoPerm, id_empresa]
        )

def eliminar_empresa(id_empresa):
    """Elimina uma empresa da tabela companies através do ID"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM companies -- <--- Atualizado aqui
            WHERE id = %s;
            """,
            [id_empresa]
        )