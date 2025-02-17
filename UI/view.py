import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None


    def load_interface(self):
        # titolo della pagina
        self._title = ft.Text("Analisi migliori aziende mondiali", color="blue", size=24)
        self._page.controls.append(self._title)

        # SEZIONE IN CIMA: CREAZIONE GRAFO

        # Dropdown Anno Fondazione e Numero Minimo di Impiegati
        self._ddYear = ft.Dropdown(label='Anno fondazione', width=200)
        self._txtNumEmployee = ft.TextField(label='Numero impiegati min', width=200)
        self._btnBuildGraph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleBuildGraph,
                                                width=200)

        row1 = ft.Row([self._ddYear, self._txtNumEmployee, self._btnBuildGraph], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Output del Grafo Creato
        self.lstOutGraph = ft.ListView(expand=0, spacing=5, padding=20, height=100, auto_scroll=False)
        self._page.controls.append(self.lstOutGraph)

        self._controller.fillDDYear()

        # SEZIONE TABS

        # Tab 1: Singola Azienda
        self._ddCompany = ft.Dropdown(label='Azienda', width=320, disabled=True)
        self._btnCercaSimili = ft.ElevatedButton(text="Cerca Simili", on_click=self._controller.handleCercaSimili,
                                                 width=200, disabled=True)
        self._btnCalcolaROI = ft.ElevatedButton(text="Calcola ROI", on_click=self._controller.handleCalcolaROI,
                                                width=200, disabled=True)

        # List View per output della parte di analisi della singola azienda
        self.lstOutSingolaAzienda = ft.ListView(expand=1, spacing=10, padding=20, height=400, auto_scroll=True)

        tab1 = ft.Column([
            ft.Row([ft.Text("Analisi di una singola azienda", size=20, color="blue")],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._ddCompany], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._btnCercaSimili], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._btnCalcolaROI], alignment=ft.MainAxisAlignment.CENTER),
            self.lstOutSingolaAzienda
        ])

        # Tab 2: Tutte le Aziende
        self._ddCountry = ft.Dropdown(label='Stato', width=320, disabled=True)
        self._ddIndustry = ft.Dropdown(label='Settore', width=320, disabled=True)
        self._btnVolumeVendite = ft.ElevatedButton(text="Volume Vendite", on_click=self._controller.handleVolumeVendite,
                                                   width=225, disabled=True)
        self._btnComponenteConnessa = ft.ElevatedButton(text="Trova Cluster di Aziende",
                                                        on_click=self._controller.handleComponenteConnessa, width=225,
                                                        disabled=True)

        # List View per output della parte di analisi di tutte le aziende
        self.lstOutTutteAziende = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        tab2 = ft.Column([
            ft.Row([ft.Text("Analisi su tutte le aziende", size=20, color="blue")],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._ddCountry, self._ddIndustry], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._btnVolumeVendite], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._btnComponenteConnessa], alignment=ft.MainAxisAlignment.CENTER),
            self.lstOutTutteAziende
        ])

        # Tab 3: Ricerca Ricorsiva
        self._txtMarketValue = ft.TextField(label='Valore di mercato (miliardi)', width=250, disabled=True)
        self._btnMassimizzaProfitti = ft.ElevatedButton(text="Massimizza Profitti",
                                                        on_click=self._controller.handleMassimizzaProfitti, width=200,
                                                        disabled=True)

        # List View per output della parte di ricorsione
        self.lstOutRicorsione = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        tab3 = ft.Column([
            ft.Row([ft.Text("Ricerca Ricorsiva", size=20, color="blue")], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._txtMarketValue], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([self._btnMassimizzaProfitti], alignment=ft.MainAxisAlignment.CENTER),
            self.lstOutRicorsione
        ])

        # Tabs (inizialmente disabilitati)
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Singola Azienda", content=tab1),
                ft.Tab(text="Tutte le Aziende", content=tab2),
                ft.Tab(text="Ricerca Ricorsiva", content=tab3)
            ], visible=False
        )

        self._page.controls.append(self.tabs)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
