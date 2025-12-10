from litestar import Litestar
from .routes.parsers_routes import *

app = Litestar(route_handlers=[get_candles, get_pe_pb, get_dividends, get_news])