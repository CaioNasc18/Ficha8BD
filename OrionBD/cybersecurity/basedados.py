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
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


# =====================================================================
# 2. CRUD DA TABELA USERS (TOTALMENTE ALINHADO COM A SUA IMAGEM)
# =====================================================================

# C - CREATE
def criar_utilizador(email, password, name, telephone, active, id_tipo, id_empresa):
    """Insere um novo utilizador salvaguardando a sensibilidade de maiúsculas"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO "Users" (email, password, name, telephone, active, "Date_created", id_tipo, id_empresa)
            VALUES (%s, %s, %s, %s, %s::boolean, NOW(), %s, %s);
            """,
            [email, password, name, telephone, active, id_tipo, id_empresa]
        )
        connection.commit()

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
            SET email = %s, name = %s, telephone = %s, active = %s::boolean, id_tipo = %s, id_empresa = %s
            WHERE "id_Utilizador" = %s;
            """,
            [email, name, telephone, active, id_tipo, id_empresa, id_utilizador]
        )
        connection.commit()

# D - DELETE
def eliminar_utilizador(id_utilizador):
    """Remove permanentemente o utilizador da tabela 'Users'"""
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM "Users" WHERE "id_Utilizador" = %s;', [id_utilizador])
        connection.commit()


# =====================================================================
# 3. TABELAS AUXILIARES DE PEDIDOS
# =====================================================================

def listar_tipos_pedido():
    """Procura os tipos de pedido na tabela 'RequestTypes'"""
    with connection.cursor() as cursor:
        cursor.execute('SELECT id AS id_tipo_pedido, name FROM public."RequestTypes";')
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


# =====================================================================
# 4. CRUD DA TABELA REQUESTS
# =====================================================================

# C - CREATE
def criar_pedido(title, description, status, creator_id, id_tipo_pedido=None, assigned_to_id=None):
    """Insere um novo pedido com chaves estrangeiras dinâmicas e limpa o contador de IDs"""
    with connection.cursor() as cursor:
        cursor.execute('SELECT setval(pg_get_serial_sequence(\'public.requests\', \'id\'), COALESCE(MAX(id), 1)) FROM public.requests;')
        cursor.execute(
            """
            INSERT INTO public.requests ("subject", "description", "status", "openedAt", "creatorId", "requestTypeId", "assignedToId")
            VALUES (%s, %s, %s, NOW(), %s, %s, %s)
            RETURNING id;
            """,
            [title, description, status, creator_id, id_tipo_pedido, assigned_to_id]
        )
        connection.commit()
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

# R - READ ONE
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
        connection.commit()

# D - DELETE
def eliminar_pedido(id_pedido):
    """Remove permanentemente o pedido"""
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM public.requests WHERE id = %s;', [id_pedido])
        connection.commit()

        # =====================================================================
# 5. CRUD DA TABELA DE FICHEIROS (REQUESTFILES)
# =====================================================================

# C - CREATE
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
        connection.commit()

# R - READ ALL BY REQUEST
def listar_ficheiros_de_pedido(id_pedido):
    """Procura todos os ficheiros associados a um pedido específico"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, "fileName", "filePath", "uploadedAt" 
            FROM public."RequestFiles" 
            WHERE "requestId" = %s;
            """,
            [id_pedido]
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


# =====================================================================
# 6. INTERROGAÇÕES SQL (SELECT) PARA O DASHBOARD - FICHA 9
# =====================================================================

def obter_conformidade_nis2():
    """Query 1: Estado de conformidade NIS2 baseado no responsável de segurança"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                nome as nome_da_empresa,
                CASE 
                    WHEN "nomeResponsavelSeg" IS NOT NULL AND "emailResponsavelSeg" IS NOT NULL THEN 'Conforme'
                    WHEN "emailResponsavelSeg" IS NOT NULL AND "nomeResponsavelSeg" IS NULL THEN 'Em avaliação'
                    ELSE 'Com pendências'
                END as estado_nis2
            FROM public.companies
            ORDER BY estado_nis2 ASC, nome_da_empresa ASC;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

def obter_top5_incidentes():
    """Query 2: Top 5 clientes com mais incidentes de segurança (requestTypeId = 1)"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.nome as cliente, COUNT(r.id) as total_incidentes
            FROM public.companies c
            JOIN public."Users" u ON c.id = u.id_empresa
            JOIN public.requests r ON u."id_Utilizador" = r."creatorId"
            WHERE r."requestTypeId" = 1
            GROUP BY c.id, c.nome
            ORDER BY total_incidentes DESC
            LIMIT 5;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

def obter_documentos_por_mes():
    """Query 3: Total de documentos submetidos por cliente e por mês"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                c.nome as cliente,
                TO_CHAR(d."uploadedAt", 'YYYY-MM') as mes,
                COUNT(d.id) as total_documentos
            FROM public.companies c
            JOIN public."Users" u ON c.id = u.id_empresa
            JOIN public.requests r ON u."id_Utilizador" = r."creatorId"
            JOIN public."RequestFiles" d ON r.id = d."requestId"
            GROUP BY c.nome, TO_CHAR(d."uploadedAt", 'YYYY-MM')
            ORDER BY mes DESC, total_documentos DESC;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

def obter_distribuicao_perfis():
    """Query 4: Distribuição de utilizadores por perfil mapeado por ID"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                CASE 
                    WHEN id_tipo = 1 THEN 'Administrador'
                    WHEN id_tipo = 2 THEN 'Cliente'
                    WHEN id_tipo = 3 THEN 'Colaboradores'
                    ELSE 'Outro'
                END as perfil,
                COUNT(*) as total
            FROM public."Users"
            GROUP BY id_tipo
            ORDER BY total DESC;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

def obter_tempo_medio_tickets():
    """Query 5: Estado dos pedidos/tickets de suporte e tempo médio de resolução"""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                status,
                COUNT(*) as total,
                ROUND(AVG(EXTRACT(EPOCH FROM (r."closedAt" - r."openedAt")) / 3600)::numeric, 1) as tempo_medio_horas
            FROM public.requests r
            GROUP BY status
            ORDER BY total DESC;
            """
        )
        colunas = [col.name for col in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
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
