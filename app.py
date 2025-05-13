from neo4j import GraphDatabase

# --- CONFIGURAÇÃO DA INSTÂNCIA NEO4J ---
URI = neo4j+s://93e6131b.databases.neo4j.io
USERNAME = camila.silva@edu.pe.senac.br  
PASSWORD = 93e6131b  

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# --- CRIAÇÃO DE NÓS ---
def criar_bairro(tx, nome):
    tx.run("CREATE (:Bairro {nome: $nome})", nome=nome)

def criar_doenca(tx, nome):
    tx.run("CREATE (:Doenca {nome: $nome})", nome=nome)

def criar_incidente(tx, id, doenca, bairro):
    query = """
    MATCH (d:Doenca {nome: $doenca})
    MATCH (b:Bairro {nome: $bairro})
    CREATE (i:IncidenteDeSaude {id: $id})-[:RELACIONADO_A]->(d)
    CREATE (i)-[:REGISTRADO_EM]->(b)
    """
    tx.run(query, id=id, doenca=doenca, bairro=bairro)

# --- LEITURA ---
def listar_incidentes(tx):
    result = tx.run("""
        MATCH (i:IncidenteDeSaude)-[:RELACIONADO_A]->(d:Doenca),
              (i)-[:REGISTRADO_EM]->(b:Bairro)
        RETURN i.id AS incidente, d.nome AS doenca, b.nome AS bairro
    """)
    print("\n📊 Incidentes registrados em Recife:\n")
    for record in result:
        print(f"🦠 Caso {record['incidente']} de {record['doenca']} em {record['bairro']}")

# --- ATUALIZAÇÃO ---
def atualizar_nome_bairro(tx, antigo, novo):
    tx.run("MATCH (b:Bairro {nome: $antigo}) SET b.nome = $novo", antigo=antigo, novo=novo)

# --- DELETE ---
def deletar_incidente(tx, id):
    tx.run("MATCH (i:IncidenteDeSaude {id: $id}) DETACH DELETE i", id=id)

# --- MENU INTERATIVO ---
def menu():
    with driver.session() as session:
        while True:
            print("\n🌆 Recife Saúde & Transporte - CRUD Ratosa")
            print("1. Cadastrar bairro")
            print("2. Cadastrar doença")
            print("3. Registrar incidente de saúde")
            print("4. Listar incidentes")
            print("5. Atualizar nome de bairro")
            print("6. Deletar incidente")
            print("0. Sair")

            escolha = input("Escolhe aí, visse? ")

            if escolha == "1":
                nome = input("Nome do bairro (ex: Brasília Teimosa): ")
                session.write_transaction(criar_bairro, nome)
                print(f"✅ Bairro {nome} cadastrado com sucesso!")

            elif escolha == "2":
                nome = input("Nome da doença (ex: Dengue): ")
                session.write_transaction(criar_doenca, nome)
                print(f"✅ Doença {nome} cadastrada com sucesso!")

            elif escolha == "3":
                id = input("ID do incidente (ex: 001): ")
                doenca = input("Nome da doença: ")
                bairro = input("Nome do bairro: ")
                session.write_transaction(criar_incidente, id, doenca, bairro)
                print("✅ Incidente registrado, tomara que melhore!")

            elif escolha == "4":
                session.read_transaction(listar_incidentes)

            elif escolha == "5":
                antigo = input("Nome atual do bairro: ")
                novo = input("Novo nome do bairro: ")
                session.write_transaction(atualizar_nome_bairro, antigo, novo)
                print("✅ Nome atualizado com sucesso!")

            elif escolha == "6":
                id = input("ID do incidente a ser removido: ")
                session.write_transaction(deletar_incidente, id)
                print("✅ Deletado, foi-se embora!")

            elif escolha == "0":
                print("🌴 Valeu, cabra! Até a próxima!")
                break

            else:
                print("❌ Escolha inválida. Tente de novo!")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    try:
        menu()
    finally:
        driver.close()
