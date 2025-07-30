from .client import SecClient


def get_company_tickers_exchange() -> dict:
    """
    Fetch the company tickers and their corresponding exchanges from the SEC.

    Returns:
        dict: A dictionary containing CIK, ticker, and exchange information.
    """
    client = SecClient()
    return client.get_company_tickers_exchange()
