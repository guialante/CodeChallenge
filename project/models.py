from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, NoReturn


@dataclass
class Client:
    """
    This class represents any Client that can be part of any AirCompany

    Attributes
    ----------
    name: str
        The name of the client
    """

    name: str


class Package:
    """
    This class represents a Package that is transported by an AirCompany

    Attributes
    ----------
    is_transported: bool
        True if the package has been already transported by the AirCompany

    ship_date: str
        The date the package was transported by the AirCompany

    client: Client
        The client who sent the package

    origin: str
        The origin of the package

    destination: str
        The destination of the package

    shipping_date_format: str
        Allow formatting of the shipping date to validate whether a shipping date is correct or not.
    """

    def __init__(self, origin: str, destination: str, client: Client) -> None:
        self.origin: str = origin
        self.destination: str = destination
        self.client: Client = client
        self._ship_date: str = ""
        self._is_transported: bool = False
        self._shipping_date_format: str = "%Y-%m-%d"

    def validate_origin_destination(self) -> bool:
        """
        :return: Boolean value indicating whether the origin and destination are the same or not
        """
        return self.origin != self.destination

    def validate_ship_date(self, ship_date: str) -> bool:
        """
        :param ship_date: Shipping date
        :return: Boolean value indicating whether the ship date is valid or not.
        """
        is_valid = True
        try:
            datetime.strptime(ship_date, self._shipping_date_format)
        except ValueError:
            is_valid = False
        return is_valid

    @property
    def ship_date(self) -> str:
        """
        :return: The shipping date of the package
        """
        return self._ship_date

    @ship_date.setter
    def ship_date(self, ship_date: str) -> None:
        """
        :param ship_date: Shipping date
        Set the shipping date of the package
        """
        self._ship_date = ship_date

    @property
    def is_transported(self) -> bool:
        """
        :return: Boolean value indicating whether the package has been already transported or not
        """
        return self._is_transported

    @is_transported.setter
    def is_transported(self, is_transported: bool) -> None:
        """
        :param is_transported: Boolean value indicating whether the package has been already transported or not
        Set the is_transported attribute of the package
        """
        self._is_transported = is_transported


class AirCompany:
    """
    This class represents an AirCompany in charge to transport packages

    Attributes
    ----------
    name: str
        The name of the AirCompany

    packages: lst
        Packages transported by the company will be stored in this list

    clients: lst
        List of clients belongs to the AirCompany that can send the packages through the AirCompany.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self._packages: list = []
        self._clients: list = []

    def add_client(self, client: Client) -> None:
        """:param client: Client
        Add the client to the AirCompany
        """
        self._clients.append(client)

    def transport_package(self, package: Package, ship_date: str) -> None | NoReturn:
        """
        :param package: Package
        :param ship_date: Shipping date
        :return: None if package can be transported or error message in string format in case not
        """
        is_valid_ship_date = package.validate_ship_date(ship_date)
        can_transport_package = self.validate_can_transport_package(package)
        if (
            is_valid_ship_date
            and can_transport_package
            and package.validate_origin_destination()
        ):
            package.is_transported = True
            package.ship_date = ship_date
            self._packages.append(package)
        else:
            if not is_valid_ship_date and not can_transport_package:
                raise Exception(
                    f"Invalid Shipping date and client: {package.client.name} is not a Client"
                )
            elif not is_valid_ship_date:
                raise Exception("Invalid Shipping Date")
            elif not can_transport_package:
                raise Exception(f"Client: {package.client.name} is not a Client")
            elif not package.validate_origin_destination():
                raise Exception("Origin and destination are the same.")

    def validate_can_transport_package(self, package: Package) -> bool:
        """
        :param package: Package
        :return: Boolean value indicating if the package belong to a client of the AirCompany
        """
        client_names = [c.name for c in self._clients]
        can_transport = package.client.name in client_names
        return can_transport

    def get_packages(self) -> list:
        """
        :return: List of packages transported by the AirCompany
        """
        return self._packages


class Report:
    """
    This class represents a Report that can be generated by an AirCompany

    Attributes
    ----------
    company: AirCompany
        The AirCompany that generates the report

    ship_date: str
        The date the report is generated
    """

    def __init__(self, company: AirCompany) -> None:
        self.company: AirCompany = company

    def generate_report(self, ship_date: str) -> Tuple[int, int]:
        """
        :param ship_date: Shipping date
        :return: the total packages transported by a specific ship date and the total value collected by that ship date
        """
        packages = self.company.get_packages()

        total_packages_per_date = list(
            filter(lambda p: p.ship_date == ship_date, packages)
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
        packages = self.company.get_packages()

        total_packages_per_date = list(
            filter(lambda p: start_ship_date <= p.ship_date < end_ship_date, packages)
        )
        total_packages = len(total_packages_per_date)
        total_collected = total_packages * 10
        return total_packages, total_collected
