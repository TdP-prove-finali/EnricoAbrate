import copy
import networkx as nx
from database.DAO import DAO
from collections import Counter
import matplotlib.pyplot as plt


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
        company = next(c for c in self._graph.nodes if c == azienda)
        settore = company.Industry

        for v in self._graph.neighbors(azienda):
            if v.Industry == azienda.Industry:
                result.append( (v.OrganizationName, self._graph[azienda][v]["weight"]) )

        return settore, sorted(result, key=lambda x: x[1], reverse=True)

    def calcolaROI(self, azienda):
        result = []

        company = next(c for c in self._graph.nodes if c == azienda)
        settore = company.Industry
        profitti = company.Profits
        assets = company.Assets

        ROIazienda = (profitti/assets) * 100

        for c in self._graph.nodes:
            if c.Industry == company.Industry:
                ROIcalcolato = (c.Profits/c.Assets)*100
                result.append( (c.OrganizationName, ROIcalcolato) )

        result = sorted(result, key=lambda x: x[1], reverse=True)

        # Genero il grafico prima di fare return, con i valori ricavati
        self.generaGraficoROI(azienda, settore, ROIazienda, result)

        return settore, ROIazienda, result

    def generaGraficoROI(self, azienda, settore, roiAzienda, altreAziende):
        # Ordina le aziende per ROI in ordine decrescente
        aziende = [a[0] for a in altreAziende]
        rois = [a[1] for a in altreAziende]

        # Aggiungi l'azienda selezionata
        aziende.insert(0, azienda)
        rois.insert(0, roiAzienda)

        # Colore differenziato per l'azienda selezionata
        colori = ['red'] + ['blue'] * (len(rois) - 1)

        # Crea il grafico a barre orizzontali
        plt.figure(figsize=(10, 6))
        plt.barh(aziende, rois, color=colori)
        plt.xlabel('ROI (%)')
        plt.title(f'Confronto ROI nel settore: {settore}')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Salva il grafico come immagine
        plt.savefig("grafico_roi.png")
        plt.close()

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

        statiMagg = sorted(arrStato, key=lambda x: x[1], reverse=True)
        settoriMagg = sorted(arrSettore, key=lambda x: x[1], reverse=True)

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

    def getPercorso(self, valMercato):
        self._bestPath = []
        self._bestVal = 0

        for n in self._graph.nodes:
            if n.MarketValue > valMercato:
                parziale = [n]
                self.ricorsione(parziale, valMercato, 0)

        return self._bestPath, self._bestVal

    def ricorsione(self, parziale, valMercato, profittoAttuale):
        if profittoAttuale > self._bestVal:
            self._bestVal = profittoAttuale
            self._bestPath = copy.deepcopy(parziale)

        for node in self._graph.neighbors(parziale[-1]):
            if node not in parziale and node.MarketValue > valMercato:
                peso = self._graph[parziale[-1]][node]["weight"]
                parziale.append(node)
                self.ricorsione(parziale, valMercato, profittoAttuale+peso)
                parziale.pop()

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
