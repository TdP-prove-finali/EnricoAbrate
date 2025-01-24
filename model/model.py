import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def buildGraph(self, year, numEmployee):
        self._graph.clear()
        self._idMap = {}

        companies = DAO.getCompanies(year)
        self._graph.add_nodes_from(companies)
        for c in companies:
            self._idMap[c.ID] = c

        edges = DAO.getEdges(year, numEmployee, self._idMap)
        for e in edges:
            e.peso = DAO.getPeso(e.company1.ID, e.company2.ID)
            self._graph.add_edge(e.company1, e.company2, weight=e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getYears(self):
        return DAO.getYears()

    def getCountry(self, year):
        return DAO.getCountry(year)

    def getIndustry(self, year):
        return DAO.getIndustry(year)
