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
        # title
        self._title = ft.Text("Analisi migliori aziende mondiali", color="blue", size=24)
        self._page.controls.append(self._title)

        # row 1
        self._ddYear = ft.Dropdown(label='Anno fondazione', width=200)
        self._txtNumEmployee = ft.TextField(label='Numero impiegati min', width=200)
        self._btnBuildGraph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleBuildGraph, width=200)
        row1 = ft.Row([self._ddYear, self._txtNumEmployee, self._btnBuildGraph], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._controller.fillDDYear()

        # List View per output del grafo creato
        self.lstOutGraph = ft.ListView(expand=0, spacing=5, padding=20, height=100, auto_scroll=False)
        self._page.controls.append(self.lstOutGraph)

        # row 2
        self._ddCompany = ft.Dropdown(label='Azienda', width=320, disabled=True)
        self._btnCercaSimili = ft.ElevatedButton(text="Cerca Simili", on_click=self._controller.handleCercaSimili, width=200, disabled=True)
        row2 = ft.Row([self._ddCompany, self._btnCercaSimili], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # row 3
        self._ddCountry = ft.Dropdown(label='Stato', width=320, disabled=True)
        self._ddIndustry = ft.Dropdown(label='Settore', width=320, disabled=True)
        self._btnVolumeVendite = ft.ElevatedButton(text="Volume Vendite", on_click=self._controller.handleVolumeVendite, width=200, disabled=True)
        row3 = ft.Row([self._ddCountry, self._ddIndustry, self._btnVolumeVendite], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # row 4
        self._btnComponenteConnessa = ft.ElevatedButton(text="Trova Cluster di Aziende", on_click=self._controller.handleComponenteConnessa, width=250, disabled=True)
        row4 = ft.Row([self._btnComponenteConnessa], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)

        # List View per output della parte di analisi
        self.lstOutAnalisi = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self.lstOutAnalisi)

        # row 5
        self._txtMarketValue = ft.TextField(label='Valore di mercato (miliardi)', width=250, disabled=True)
        self._btnMassimizzaProfitti = ft.ElevatedButton(text="Massimizza Profitti", on_click=self._controller.handleMassimizzaProfitti, width=200, disabled=True)
        row5 = ft.Row([self._txtMarketValue, self._btnMassimizzaProfitti], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row5)

        # List View per output della ricorsione
        self.lstOutRicorsione = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self.lstOutRicorsione)
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
