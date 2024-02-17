from datetime import datetime
from typing import Tuple


class Client:
    """
    This class represents any Client that can be part of any AirCompany
    """

    def __init__(self, name) -> None:
        self.name = name


class Package:
    """
    This class represents a Package that is transported by an AirCompany


    Attributes
    ----------
    is_transported: bool
        True if the package has been already transported by the AirCompany

    ship_date: str
        The date the package was transported by the AirCompany

    client: Client | None
        The client who sent the package
    """

    def __init__(self) -> None:
        self.is_transported: bool = False
        self.ship_date: str = ""
        self.client: Client | None = None


class AirCompany:
    """
    This class represents an AirCompany in charge to transport packages

    Attributes
    ----------
    packages: lst
        Packages transported by the company will be stored in this list

    clients: lst
        List of clients belongs to the AirCompany that can send the packages through the AirCompany.

    shipping_date_format: str
        Allow formatting of the shipping date to validate whether a shipping date is correct or not.
    """

    def __init__(self) -> None:
        self.packages: list = []
        self.clients: list = []
        self.shipping_date_format: str = "%Y-%m-%d"

    def add_client(self, client: Client) -> None:
        """:param client: Client

        Add the client to the AirCompany
        """
        self.clients.append(client)

    def transport_package(self, package: Package, ship_date: str) -> None | str:
        """
        :param package: Package
        :param ship_date: Shipping date
        :return: None if package can be transported or error message in string format in case not
        """
        is_valid_ship_date = self.validate_ship_date(ship_date)
        can_transport_package = self.validate_can_transport_package(package)
        if is_valid_ship_date and can_transport_package:
            package.is_transported = True
            package.ship_date = ship_date
            self.packages.append(package)
        else:
            if not is_valid_ship_date and not can_transport_package:
                return f"Invalid Shipping date and client: {package.client.name} is not a Client"
            elif not can_transport_package:
                return f"Client: {package.client.name} is not a Client"
            else:
                return "Invalid Shipping Date"

    def generate_report(self, ship_date: str) -> Tuple[int, int]:
        """
        :param ship_date: Shipping date
        :return: the total packages transported by a specific ship date and the total value collected by that ship date
        """
        total_packages_per_date = list(
            filter(lambda p: p.ship_date == ship_date, self.packages)
        )
        total_packages = len(total_packages_per_date)
        total_collected = total_packages * 10
        return total_packages, total_collected

    def generate_report_by_dates(
        self, start_ship_date: str, end_ship_date: str
    ) -> Tuple[int, int]:
        """
        :param start_ship_date: Start ship date
        :param end_ship_date: End ship date
        :return: the total packages transported by the range between start_ship_date and end_ship_date and the total
        value collected by that range.
        """
        total_packages_per_date = list(
            filter(
                lambda p: start_ship_date <= p.ship_date < end_ship_date, self.packages
            )
        )
        total_packages = len(total_packages_per_date)
        total_collected = total_packages * 10
        return total_packages, total_collected

    def validate_ship_date(self, ship_date: str) -> bool:
        """
        :param ship_date: Shipping date
        :return: Boolean value indicating whether the ship date is valid or not.
        """
        is_valid = True
        try:
            datetime.strptime(ship_date, self.shipping_date_format)
        except ValueError:
            is_valid = False
        return is_valid

    def validate_can_transport_package(self, package: Package) -> bool:
        """
        :param package: Package
        :return: Boolean value indicating if the package belong to a client of the AirCompany
        """
        client_names = [c.name for c in self.clients]
        can_transport = package.client.name in client_names
        return can_transport
