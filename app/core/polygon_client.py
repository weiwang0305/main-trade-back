from polygon import RESTClient

from app.core.config import Settings

polygon_client = None


def initialize_polygon_client():
    global polygon_client
    polygon_client = RESTClient(Settings.POLYGON_API_KEY)


def get_polygon_client():
    return polygon_client
