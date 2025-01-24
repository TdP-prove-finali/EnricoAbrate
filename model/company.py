from dataclasses import dataclass

@dataclass
class Company:
    ID: int
    OrganizationName: str
    Industry: str
    Country: str
    YearFounded: int
    CEO: str
    Revenue: float
    Profits: float
    Assets: float
    MarketValue: float
    TotalEmployees: int

    def __hash__(self):
        return hash(self.ID)

    def __str__(self):
        return f"{self.OrganizationName}"
