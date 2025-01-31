import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._selectedYear = None
        self._selectedCountry = None
        self._selectedIndustry = None
        self._selectedCompany = None

    def fillDDYear(self):
        years = self._model.getYears()

        for y in years:
            self._view._ddYear.options.append(ft.dropdown.Option(data=int(y), text=f"{y}", on_click=self.choiseYear))

        self._view.update_page()

    def handleBuildGraph(self, e):
        try:
            numEmployee = int(self._view._txtNumEmployee.value)
        except ValueError:
            self._view.create_alert("Inserire un numero intero!")
            return

        if self._selectedYear is None:
            self._view.create_alert("Selezionare un anno!")
            return

        self._model.buildGraph(int(self._selectedYear), numEmployee)

        self._view.lstOutGraph.controls.clear()
        self._view.lstOutGraph.controls.append(ft.Text(f"Trovate {self._model.getNumNodes()} aziende fondate dopo il {self._selectedYear}, le quali si collegano tra loro tramite {self._model.getNumEdges()} archi."))

        # SBLOCCARE TUTTI GLI OGGETTI NELLA VIEW
        self._view._ddCompany.disabled = False
        self._view._btnCercaSimili.disabled = False
        self._view._ddCountry.disabled = False
        self._view._ddIndustry.disabled = False
        self._view._btnVolumeVendite.disabled = False
        self._view._btnComponenteConnessa.disabled = False
        self._view._txtMarketValue.disabled = False
        self._view._btnMassimizzaProfitti.disabled = False

        # RIEMPIRE I DROPDOWN
        self._view._ddCompany.value = None
        self._view._ddCountry.value = None
        self._view._ddIndustry.value = None
        self._view._ddCompany.options.clear()
        self._view._ddCountry.options.clear()
        self._view._ddIndustry.options.clear()

        companies = sorted(self._model._graph.nodes, key=lambda x: x.OrganizationName)
        for c in companies:
            self._view._ddCompany.options.append(
                ft.dropdown.Option(data=c, text=f"{c.OrganizationName}", on_click=self.choiseCompany))
        countries = self._model.getCountry(self._selectedYear)
        for co in countries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(data=co, text=f"{co}", on_click=self.choiseCountry))
        industry = self._model.getIndustry(self._selectedYear)
        for i in industry:
            self._view._ddIndustry.options.append(
                ft.dropdown.Option(data=i, text=f"{i}", on_click=self.choiseIndustry))

        self._view.update_page()

    def handleCercaSimili(self, e):
        if self._selectedCompany is None:
            self._view.create_alert("Selezionare un'azienda!")
            return

        simili = self._model.getSimili(self._selectedCompany)
        self._view.lstOutAnalisi.controls.clear()
        self._view.lstOutAnalisi.controls.append(ft.Text(f"Le aziende che operano nello stesso settore di {self._selectedCompany} sono:", weight=ft.FontWeight.BOLD))
        for s in simili:
            self._view.lstOutAnalisi.controls.append(ft.Text(f"{s[0]} con media dei profitti generati tra le imprese: {s[1]:.2f}B$."))

        self._view.update_page()

    def handleVolumeVendite(self, e):
        if self._selectedIndustry is None:
            self._view.create_alert("Selezionare un settore!")
            return
        if self._selectedCountry is None:
            self._view.create_alert("Selezionare uno stato!")
            return

        totStato, totSettore, arrStato, arrSettore = self._model.getVolumeAffari(self._selectedCountry, self._selectedIndustry)

        self._view.lstOutAnalisi.controls.clear()

        self._view.lstOutAnalisi.controls.append(ft.Text(spans=[ft.TextSpan(f"I profitti totali generati dalle imprese nello Stato {self._selectedCountry} sono: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                                                ft.TextSpan(f"{totStato:.2f}B$", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="green"))]))
        self._view.lstOutAnalisi.controls.append(ft.Text(f"Le imprese che maggiormente influiscono sono:"))
        for st in arrStato:
            self._view.lstOutAnalisi.controls.append(ft.Text(f"{st[0]} con {st[1]}B$"))

        self._view.lstOutAnalisi.controls.append(ft.Text(f""))

        self._view.lstOutAnalisi.controls.append(ft.Text(spans=[ft.TextSpan(f"I profitti totali generati dalle imprese nel settore {self._selectedIndustry} sono: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                                                ft.TextSpan(f"{totSettore:.2f}B$", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="green"))]))

        self._view.lstOutAnalisi.controls.append(ft.Text(f"Le imprese che maggiormente influiscono sono:"))
        for se in arrSettore:
            self._view.lstOutAnalisi.controls.append(ft.Text(f"{se[0]} con {se[1]}B$"))

        self._view.update_page()

    def handleComponenteConnessa(self, e):
        clusters = self._model.trovaCluster()
        miglioriClusters = clusters[:3]

        self._view.lstOutAnalisi.controls.clear()
        self._view.lstOutAnalisi.controls.append(ft.Text(f"Sono state trovate {len(clusters)} componenti connesse.", weight=ft.FontWeight.BOLD))
        self._view.lstOutAnalisi.controls.append(ft.Text(f"Le migliori sono:"))
        for i, (num, settore, reddito) in enumerate(miglioriClusters, 1):
            self._view.lstOutAnalisi.controls.append(ft.Text(f"{i}. Cluster con {num} aziende, settore dominante: {settore}, reddito totale: {reddito:.2f}B$"))

        self._view.update_page()

    def handleMassimizzaProfitti(self, e):
        try:
            valMercato = int(self._view._txtMarketValue.value)
        except ValueError:
            self._view.create_alert("Inserire un numero intero!")
            return

        path, val = self._model.getPercorso(valMercato)

        self._view.lstOutRicorsione.controls.clear()
        self._view.lstOutRicorsione.controls.append(ft.Text(spans=[ft.TextSpan(f"Il percorso con profitti più alti ammonta a: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                                                   ft.TextSpan(f"{val:.2f}B$.", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color="green"))]))
        self._view.lstOutRicorsione.controls.append(ft.Text(f"E' attraversato da:"))
        for i in range(0, len(path)-1):
            self._view.lstOutRicorsione.controls.append(ft.Text(f"{path[i]} --> {path[i+1]}, peso: {self._model._graph[path[i]][path[i+1]]["weight"]}B$"))

        self._view.update_page()

    def choiseYear(self, e):
        if e.control.data is None:
            self._selectedYear = None
        else:
            self._selectedYear = e.control.data
            print(self._selectedYear)

    def choiseCompany(self, e):
        if e.control.data is None:
            self._selectedCompany = None
        else:
            self._selectedCompany = e.control.data
            print(self._selectedCompany)

    def choiseCountry(self, e):
        if e.control.data is None:
            self._selectedCountry = None
        else:
            self._selectedCountry = e.control.data
            print(self._selectedCountry)

    def choiseIndustry(self, e):
        if e.control.data is None:
            self._selectedIndustry = None
        else:
            self._selectedIndustry = e.control.data
            print(self._selectedIndustry)
