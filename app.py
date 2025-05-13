from conexao import ConexaoNeo4j

# Substitua pelos dados do Neo4j Aura
uri = neo4j+s://93e6131b.databases.neo4j.io
user = camila.silva@edu.pe.senac.br
password = 93e6131b

db = ConexaoNeo4j(uri, user, password)

def criar_pessoa():
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    profissao = input("Profissão: ")
    query = """
    CREATE (p:Pessoa {nome: $nome, idade: $idade, profissao: $profissao})
    """
    db.executar_query(query, {"nome": nome, "idade": idade, "profissao": profissao})
    print("Pessoa criada com sucesso.")

def listar_pessoas():
    query = "MATCH (p:Pessoa) RETURN p.nome AS nome, p.idade AS idade, p.profissao AS profissao"
    resultados = db.executar_query(query)
    for r in resultados:
        print(f"Nome: {r['nome']}, Idade: {r['idade']}, Profissão: {r['profissao']}")

def atualizar_pessoa():
    nome = input("Nome da pessoa que deseja atualizar: ")
    nova_idade = int(input("Nova idade: "))
    nova_profissao = input("Nova profissão: ")
    query = """
    MATCH (p:Pessoa {nome: $nome})
    SET p.idade = $idade, p.profissao = $profissao
    """
    db.executar_query(query, {"nome": nome, "idade": nova_idade, "profissao": nova_profissao})
    print("Pessoa atualizada com sucesso.")

def deletar_pessoa():
    nome = input("Nome da pessoa a ser deletada: ")
    query = "MATCH (p:Pessoa {nome: $nome}) DELETE p"
    db.executar_query(query, {"nome": nome})
    print("Pessoa deletada com sucesso.")

def menu():
    while True:
        print("\n--- MENU CRUD NEO4J ---")
        print("1 - Criar Pessoa")
        print("2 - Listar Pessoas")
        print("3 - Atualizar Pessoa")
        print("4 - Deletar Pessoa")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_pessoa()
        elif opcao == "2":
            listar_pessoas()
        elif opcao == "3":
            atualizar_pessoa()
        elif opcao == "4":
            deletar_pessoa()
        elif opcao == "5":
            db.close()
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
