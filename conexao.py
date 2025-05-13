from neo4j import GraphDatabase

class ConexaoNeo4j:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def executar_query(self, query, parametros=None):
        with self.driver.session() as session:
            return session.run(query, parametros or {})
