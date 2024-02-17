import unittest
import random

from project.models import Client, Package, AirCompany


class TestAirCompany(unittest.TestCase):

    def test_transport_package(self):

        client = Client('client a')
        company = AirCompany()
        company.add_client(client)
        package = Package()
        package.client = client

        self.assertFalse(package.is_transported)
        self.assertEqual(len(company.packages), 0)
        company.transport_package(package, ship_date="2024-02-01")
        self.assertTrue(package.is_transported)
        self.assertEqual(len(company.packages), 1)
        self.assertIn(package, company.packages)

    def test_transport_package_invalid_ship_date(self):
        client = Client('client a')
        company = AirCompany()
        company.add_client(client)
        package = Package()
        package.client = client

        self.assertEqual(company.transport_package(package, ship_date="2024-02-30"), "Invalid Shipping Date")

    def test_transport_package_invalid_client(self):
        client = Client('client a')
        client2 = Client('client b')
        company = AirCompany()
        company.add_client(client)
        package = Package()
        package.client = client2

        self.assertEqual(
            company.transport_package(package, ship_date="2024-02-01"),
            f"Client: {package.client.name} is not a Client"
        )

    def test_transport_package_invalid_client_and_ship_date(self):
        client = Client('client a')
        client2 = Client('client b')
        company = AirCompany()
        company.add_client(client)
        package = Package()
        package.client = client2

        self.assertEqual(
            company.transport_package(package, ship_date="2024-02-30"),
            f"Invalid Shipping date and client: {package.client.name} is not a Client"
        )

    def test_generate_report(self):
        company = AirCompany()
        client = Client('client a')
        client2 = Client('client b')
        client3 = Client('client c')
        company.add_client(client)
        company.add_client(client2)
        company.add_client(client3)

        ship_dates = ["2024-02-01", "2024-02-02"]
        clients = [client, client2, client3]

        for i in range(101):
            package = Package()
            package.client = clients[random.randint(0, len(clients) - 1)]
            ship_date = ship_dates[0] if i % 2 == 0 else ship_dates[1]
            company.transport_package(package, ship_date=ship_date)

        total_packages, total_collected = company.generate_report(ship_date=ship_dates[0])
        self.assertEqual(total_packages, 51)
        self.assertEqual(total_collected, 510)

        total_packages1, total_collected1 = company.generate_report(ship_date=ship_dates[1])
        self.assertEqual(total_packages1, 50)
        self.assertEqual(total_collected1, 500)

        total_packages2, total_collected2 = company.generate_report_by_dates(
            start_ship_date="2024-02-01", end_ship_date="2024-03-01")

        self.assertEqual(total_packages2, 101)
        self.assertEqual(total_collected2, 1010)

        total_packages3, total_collected3 = company.generate_report_by_dates(
            start_ship_date="2024-03-01", end_ship_date="2024-04-01")

        self.assertEqual(total_packages3, 0)
        self.assertEqual(total_collected3, 0)



if __name__ == "__main__":
    unittest.main()
