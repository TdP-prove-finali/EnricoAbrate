import copy
import networkx as nx
from database.DAO import DAO
from collections import Counter


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

    def getSimili(self, azienda):
        result = []

        for v in self._graph.neighbors(azienda):
            if v.Industry == azienda.Industry:
                result.append( (v.OrganizationName, self._graph[azienda][v]["weight"]) )

        return sorted(result, key=lambda x: x[1], reverse=True)

    def getVolumeAffari(self, stato, settore):
        totStato = 0
        totSettore = 0
        arrStato = []
        arrSettore = []

        for c in self._graph.nodes:
            if c.Industry == settore:
                totSettore += c.Profits
                arrSettore.append( (c.OrganizationName, c.Profits) )

            if c.Country == stato:
                totStato += c.Profits
                arrStato.append( (c.OrganizationName, c.Profits) )

        statiMagg = sorted(arrStato, key=lambda x: x[1], reverse=True)[:3]
        settoriMagg = sorted(arrSettore, key=lambda x: x[1], reverse=True)[:3]

        return totStato, totSettore, statiMagg, settoriMagg

    def trovaCluster(self):
        componenti = list(nx.connected_components(self._graph))

        clusters = []

        for comp in componenti:
            numAziende = len(comp)
            settori = []
            redditoTot = 0

            for node in comp:
                settori.append(node.Industry)
                redditoTot += node.Profits

            settorePiuFrequente = Counter(settori).most_common(1)[0][0]

            clusters.append((numAziende, settorePiuFrequente, redditoTot))

        clusters.sort(key=lambda x: x[0], reverse=True)

        return clusters

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
