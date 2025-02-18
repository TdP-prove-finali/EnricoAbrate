from database.DB_connect import DBConnect
from model.company import Company
from model.connessa import Connessa


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YearFounded 
                    FROM companies c 
                    ORDER BY c.YearFounded DESC   """

        cursor.execute(query, ())
        for row in cursor:
            result.append((row["YearFounded"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getCompanies(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM companies c 
                    WHERE c.YearFounded > %s   """

        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Company(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getCountry(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT c.Country 
                    FROM companies c 
                    WHERE c.YearFounded > %s
                    ORDER BY c.Country ASC   """

        cursor.execute(query, (year,))
        for row in cursor:
            result.append((row["Country"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getIndustry(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT c.Industry  
                    FROM companies c 
                    WHERE c.YearFounded > %s
                    ORDER BY c.Industry ASC   """

        cursor.execute(query, (year,))
        for row in cursor:
            result.append((row["Industry"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllWeights(year, numEmployee):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT c.ID AS idCompany1, c2.ID AS idCompany2, ROUND(AVG((c.Profits + c2.Profits)/2), 2) as Peso
                    FROM companies c
                    JOIN companies c2 ON c.ID > c2.ID
                    WHERE c.YearFounded > %s AND c2.YearFounded > %s
                        AND ABS(c.YearFounded - c2.YearFounded) <= 10
                        AND c.Country = c2.Country
                        AND c.TotalEmployees > %s AND c2.TotalEmployees > %s
                    GROUP BY c.ID, c2.ID   """

        cursor.execute(query, (year, year, numEmployee, numEmployee))
        for row in cursor:
            result.append((row["idCompany1"], row["idCompany2"], row["Peso"]))

        cursor.close()
        conn.close()

        return result
