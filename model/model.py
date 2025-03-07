import copy
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from database.DAO import DAO
from collections import Counter
import time


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

        pesi = DAO.getAllWeights(year, numEmployee)
        for id1, id2, peso in pesi:
            self._graph.add_edge(self._idMap[id1], self._idMap[id2], weight=peso)

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
        # Limita a 10 aziende per evitare sovraccarico
        top_n = 10
        altreAziende = altreAziende[:top_n]

        # Crea una lista di dizionari con i dati necessari
        dati = [{'Azienda': azienda.OrganizationName, 'ROI': roiAzienda, 'Colore': 'red'}]
        for a in altreAziende:
            if a[0] != azienda.OrganizationName:
                dati.append({'Azienda': a[0], 'ROI': a[1], 'Colore': 'blue'})

        # Crea un DataFrame con Pandas
        df = pd.DataFrame(dati)

        # Ordina per ROI decrescente
        df = df.sort_values(by='ROI', ascending=True)

        # Crea il grafico a barre orizzontali con Matplotlib
        plt.figure(figsize=(10, 6))
        plt.barh(df['Azienda'], df['ROI'], color=df['Colore'])
        plt.xlabel('ROI (%)')
        plt.title(f'Confronto ROI nel settore: {settore}')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Salva il grafico come immagine PNG
        plt.savefig("grafici/grafico_roi.png")
        plt.close()

    def getVolumeAffari(self, stato, settore):
        # Somma dei profitti generati per le imprese differenziati per stato e settore
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

            stato = next(iter(comp)).Country

            for node in comp:
                settori.append(node.Industry)
                redditoTot += node.Profits

            settorePiuFrequente = Counter(settori).most_common(1)[0][0]

            clusters.append((numAziende, settorePiuFrequente, redditoTot, stato))

        clusters.sort(key=lambda x: x[0], reverse=True)

        return clusters

    def getPercorso(self, valMercato):
        self._bestPath = []
        self._bestVal = 0
        self._memo = {}
        minPeso = 10  # Peso minimo dell'arco per considerarlo

        for n in self._graph.nodes:
            if n.MarketValue > valMercato:
                parziale = [n]
                self.ricorsione(parziale, valMercato, 0, minPeso)

        return self._bestPath, self._bestVal

    def ricorsione(self, parziale, valMercato, profittoAttuale, minPeso):
        chiaveMemo = (parziale[-1], frozenset(parziale))
        if chiaveMemo in self._memo and self._memo[chiaveMemo] >= profittoAttuale:
            return
        self._memo[chiaveMemo] = profittoAttuale

        # Aggiorna il miglior percorso trovato
        if profittoAttuale > self._bestVal:
            self._bestVal = profittoAttuale
            self._bestPath = copy.deepcopy(parziale)

        for node in self._graph.neighbors(parziale[-1]):
            if node not in parziale and node.MarketValue > valMercato:
                peso = self._graph[parziale[-1]][node]["weight"]

                if peso < minPeso:
                    continue

                max_profitto = profittoAttuale + peso + sum(
                    [self._graph[parziale[-1]][n]["weight"] for n in self._graph.neighbors(parziale[-1])]
                )
                if max_profitto <= self._bestVal:
                    continue

                parziale.append(node)
                self.ricorsione(parziale, valMercato, profittoAttuale + peso, minPeso)
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
