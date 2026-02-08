import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

class UserDB:
    def __init__(self):
        # Configurações de conexão obtidas das variáveis de ambiente (.env)
        self.db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }
    
    def _get_connection(self):
        """Método privado para estabelecer conexão com o banco"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            print("Dica: Verifique se o arquivo .env está criado e a conexão com o banco está ativa.")
            raise

    def create_tables(self):
        """
        Lê o arquivo schema.sql e executa no banco para criar as tabelas.
        Utilizado para a configuração inicial (setup) das tabelas.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Caminho dinâmico para encontrar o arquivo educasolidario_database.sql na mesma pasta deste script
            sql_path = Path(__file__).parent / 'educasolidario_database.sql'
            
            print(f"--- Lendo arquivo de schema: {sql_path} ---")
            with open(sql_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            cursor.execute(sql_script)
            conn.commit()
            print("Tabelas, Types e Triggers criados com sucesso!")
            
        except Exception as e:
            conn.rollback()
            print(f"Erro ao criar tabelas: {e}")
        finally:
            cursor.close()
            conn.close()

    def save(self, user):
        """
        Persiste um objeto User (Doador ou Instituição) no banco de dados.
        Realiza o mapeamento dos atributos do objeto para as colunas da tabela.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            print(f"--- Conectando ao PostgreSQL... ---")
            
            # Query SQL unificada para inserir dados nas colunas de ambos os perfis (Doador e Instituição)
            sql = """
                INSERT INTO users (
                    user_role, email, password_hash, endereco, telefone, 
                    cpf, donor_name, date_birth, 
                    cnpj, institution_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id;
            """
            
            # Preparando as variáveis (definindo NULL/None para o que não for do tipo do usuário)
            cpf = None
            donor_name = None
            date_birth = None
            cnpj = None
            institution_name = None

            # Lógica de mapeamento baseada no tipo de usuário (Polimorfismo)
            if user.user_type == 'donor':
                cpf = user.cpf
                donor_name = user.name
                date_birth = user.date_birth
                print(f"Salvando Doador: {donor_name}")
                
            elif user.user_type == 'institution':
                cnpj = user.cnpj
                institution_name = user.institution_name
                print(f"Salvando Instituição: {institution_name}")

            # Executa o comando INSERT com os parâmetros tratados
            cursor.execute(sql, (
                user.user_type,      
                user.email,
                user.password,       
                user.endereco,
                user.telefone,
                cpf,
                donor_name,
                date_birth,
                cnpj,
                institution_name
            ))
            
            # Recupera o ID gerado automaticamente pelo banco (RETURNING user_id)
            new_id = cursor.fetchone()[0] 
            conn.commit()
            
            print(f"Usuário salvo com sucesso! ID gerado: {new_id}\n")
            return True
            
        except psycopg2.Error as e:
            conn.rollback() # Desfaz a transação em caso de erro no banco
            print(f"Erro de Banco de Dados: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Bloco de execução direta para setup do banco
    db = UserDB()
    print("Iniciando setup do banco de dados...")
    db.create_tables()