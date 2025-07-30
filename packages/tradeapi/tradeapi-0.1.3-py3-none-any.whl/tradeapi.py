
import grpc
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timezone, timedelta

import pandas as pd

from finamgrpc.tradeapi.v1.auth.auth_service_pb2_grpc import AuthServiceStub
from finamgrpc.tradeapi.v1.assets.assets_service_pb2_grpc import AssetsServiceStub
from finamgrpc.tradeapi.v1.marketdata.marketdata_service_pb2_grpc import MarketDataServiceStub
from finamgrpc.tradeapi.v1.accounts.accounts_service_pb2_grpc import AccountsServiceStub
from finamgrpc.tradeapi.v1.orders.orders_service_pb2_grpc import OrdersServiceStub

from finamgrpc.tradeapi.v1.auth import auth_service_pb2
from finamgrpc.tradeapi.v1.assets import assets_service_pb2
from finamgrpc.tradeapi.v1.marketdata import marketdata_service_pb2
from finamgrpc.tradeapi.v1.accounts import accounts_service_pb2
from finamgrpc.tradeapi.v1.orders import orders_service_pb2

from finamgrpc.tradeapi.v1 import side_pb2

from google.protobuf.timestamp_pb2 import Timestamp
from google.type.interval_pb2 import Interval

from google.type.decimal_pb2 import Decimal

from datetime import datetime, timezone





class FinamApi: 
    def __init__(self,token):
        self.token = token 
        self.channel = grpc.secure_channel('ftrr01.finam.ru:443', grpc.ssl_channel_credentials())
        self.auth()

        re_tkn = auth_service_pb2.TokenDetailsRequest(token = self.jwc_token)
        acc = self.auth_stub.TokenDetails(re_tkn,metadata = (self.metadata,))
        self.account_inf = acc
        assets_stub  = AssetsServiceStub(self.channel)
        assets_request = assets_service_pb2.AssetsRequest()
        assets = assets_stub.Assets(assets_request, metadata=(self.metadata,))

        data = []
        for asset in assets.assets:
            data.append({
                "symbol": asset.symbol,
                "id": asset.id,
                "ticker": asset.ticker,
                "mic": asset.mic,
                "isin": asset.isin,
                "type": asset.type,
                "name": asset.name,
            })
        self.assets = pd.DataFrame(data)

        exchange_request = assets_service_pb2.ExchangesRequest()
        exchanges = assets_stub.Exchanges(exchange_request, metadata=(self.metadata,))
        exc = exchanges.exchanges
        data = [MessageToDict(e, preserving_proto_field_name=True) for e in exc]
        self.exchanges = pd.DataFrame(data=data)

        self.status_order = {
                0: "Неопределенное значение",
                1: "NEW",
                2: "PARTIALLY_FILLED",
                3: "FILLED",
                4: "DONE_FOR_DAY",
                5: "CANCELED",
                6: "REPLACED",
                7: "PENDING_CANCEL",
                9: "REJECTED",
                10: "SUSPENDED",
                11: "PENDING_NEW",
                13: "EXPIRED",
                16: "FAILED",
                17: "FORWARDING",
                18: "WAIT",
                19: "DENIED_BY_BROKER",
                20: "REJECTED_BY_EXCHANGE",
                21: "WATCHING",
                22: "EXECUTED",
                23: "DISABLED",
                24: "LINK_WAIT",
                27: "SL_GUARD_TIME",
                28: "SL_EXECUTED",
                29: "SL_FORWARDING",
                30: "TP_GUARD_TIME",
                31: "TP_EXECUTED",
                32: "TP_CORRECTION",
                33: "TP_FORWARDING",
                34: "TP_CORR_GUARD_TIME",
            }

    def auth(self): 
        self.auth_stub = AuthServiceStub(self.channel)
        request = auth_service_pb2.AuthRequest(secret= self.token)
        response = self.auth_stub.Auth(request)
        self.jwc_token = response.token
        self.metadata =  ('authorization', self.jwc_token)
    
    def account(self,account_id): 
        acc_stub = AccountsServiceStub(self.channel)
        request = accounts_service_pb2.GetAccountRequest(account_id = account_id)
        response = acc_stub.GetAccount(request,metadata = (self.metadata,))
        return response

    def acc_trades(self,account_id, interval: list): 
        acc_stub = AccountsServiceStub(self.channel)
        interval_v = self.make_interval_from_strings(interval[0], interval[1])
        request = accounts_service_pb2.	TradesRequest(account_id = account_id,interval = interval_v)
        response = acc_stub.Trades(request,metadata = (self.metadata,))
        data = MessageToDict(response)
        df = pd.DataFrame(data['trades'])
        for col in ['price', 'size']:
            df[col] = df[col].apply(lambda x: float(x['value']))
        return df

    def transactions(self,account_id, interval: list): 
        acc_stub = AccountsServiceStub(self.channel)
        interval_v = self.make_interval_from_strings(interval[0], interval[1])
        request = accounts_service_pb2.TransactionsRequest(account_id = account_id,interval = interval_v)
        response = acc_stub.Transactions(request,metadata = (self.metadata,))
        data = MessageToDict(response)
        data = [self.flatten_dict(j) for j in data['transactions']]
        df = pd.DataFrame(data)
        return df 
    
    def option_chain(self,symbol): 
        option_stub = AssetsServiceStub(self.channel)
        request = assets_service_pb2.OptionsChainRequest(underlying_symbol = symbol) 
        option_chain = option_stub.OptionsChain(request,metadata = (self.metadata,))
        return option_chain
    
    def orderbook(self, symbol): 
        orderbook_stub = MarketDataServiceStub(self.channel)
        request_orderbook = marketdata_service_pb2.OrderBookRequest(symbol = symbol)
        orderbook = orderbook_stub.OrderBook(request_orderbook,metadata = (self.metadata,))
        bid = []
        offer = []
        for row in orderbook.orderbook.rows:
            volume = float(row.buy_size.value) if row.buy_size.value !='' else float(row.sell_size.value) 
            if row.buy_size.value !='':
                bid.append({
                    "price": float(row.price.value),
                    "volume": volume,
                    "side": 'BID'
                })     
            else:
                offer.append({
                    "price": float(row.price.value),
                    "volume": volume,
                    "side": 'OFFER'
                })
        offer = pd.DataFrame(offer)
        bid = pd.DataFrame(bid)

        offer.sort_values('price',inplace=True,ignore_index=True)
        bid.sort_values('price', ascending=False, inplace=True,ignore_index=True)
        
        return {'bid':bid,'offer':offer}
    
    def Quotes(self,symbol): 
       quotes_stub = MarketDataServiceStub(self.channel)
       request_quotes = marketdata_service_pb2.QuoteRequest(symbol = symbol)
       quotes = quotes_stub.LastQuote(request_quotes,metadata = (self.metadata,))
       d = MessageToDict(quotes.quote, preserving_proto_field_name=True)
       d2 = self.flatten_dict(d)
       quotes = pd.DataFrame([d2])
       quotes['timestamp'] = pd.to_datetime(quotes['timestamp'],format='mixed').dt.tz_convert('Europe/Moscow')
       return quotes
    
    def Trades(self,symbol):
       quotes_stub = MarketDataServiceStub(self.channel)
       request_trades = marketdata_service_pb2.LatestTradesRequest(symbol = symbol)
       trades = quotes_stub.LatestTrades(request_trades,metadata = (self.metadata,))
       rows = []
       for trade in trades.trades:
            d = MessageToDict(trade, preserving_proto_field_name=True)
            flat = self.flatten_dict(d)
            rows.append(flat)
       trades = pd.DataFrame(rows)
       trades['timestamp'] = pd.to_datetime(trades['timestamp'],format='mixed').dt.tz_convert('Europe/Moscow')

       return trades

    def Bars(self,symbol,interval:list, timeframe = "TIME_FRAME_H1"):
       interval_v = self.make_interval_from_strings(interval[0], interval[1])
       quotes_stub = MarketDataServiceStub(self.channel)
       request_bars= marketdata_service_pb2.BarsRequest(symbol = symbol, interval = interval_v,timeframe = timeframe)
       bars = quotes_stub.Bars(request_bars,metadata = (self.metadata,))
    
       data = []
       for br in bars.bars: 
           br = MessageToDict(br)
           br = self.flatten_dict(br)
           data.append(br)

       df = pd.DataFrame(data)
       df['timestamp'] = pd.to_datetime(df['timestamp'],format='mixed').dt.tz_convert('Europe/Moscow')

       return df

    def flatten_dict(self,d, parent_key='', sep='_'):
        """Рекурсивно превращает вложенные dict в плоские с объединёнными ключами"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                # Если внутри только {'value': ...}
                if set(v.keys()) == {'value'}:
                    try:
                        items.append((new_key, float(v['value'])))
                    except ValueError:
                        items.append((new_key, v['value']))
                else:
                    # Вложенный словарь — рекурсия
                    items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def make_interval_from_strings(self,start_str, end_str, fmt='%Y-%m-%d'):
        # Parse string to datetime (always use UTC for proto)
        dt_start = datetime.strptime(start_str, fmt).replace(tzinfo=timezone.utc)
        dt_end = datetime.strptime(end_str, fmt).replace(tzinfo=timezone.utc)
        ts_start = Timestamp()
        ts_start.FromDatetime(dt_start)
        ts_end = Timestamp()
        ts_end.FromDatetime(dt_end)
        return Interval(start_time=ts_start, end_time=ts_end)

    def place_order(self, symbol,account_id, quantity, limit_price,side = 0, type = orders_service_pb2.ORDER_TYPE_MARKET):
        quantity = Decimal(value=str(quantity))  
        if limit_price: 
            limit_price = Decimal(value=str(limit_price))
        
        side = side_pb2.SIDE_BUY if side == 0 else side_pb2.SIDE_SELL

        order_stub = OrdersServiceStub(self.channel)
        request = orders_service_pb2.Order(symbol = symbol,account_id = account_id,quantity = quantity,type =type,limit_price = limit_price,side = side)
        order_place = order_stub.PlaceOrder(request,metadata = (self.metadata,))
        order_id = order_place.order_id
        status = self.status_order[order_place.status]
        transact = order_place.transact_at
        dt_utc = datetime.fromtimestamp(transact.seconds + transact.nanos / 1e9, tz=timezone.utc)
        moscow_tz = timezone(timedelta(hours=3))
        dt_msk = dt_utc.astimezone(moscow_tz)
        return {'order_id':order_id,'status':status,'time':dt_msk}

    def cancel_order(self,order_id,account_id):
        order_stub = OrdersServiceStub(self.channel)
        cancel_order = orders_service_pb2.CancelOrderRequest(account_id = account_id,order_id = order_id)
        order_cancel = order_stub.CancelOrder(cancel_order,metadata = (self.metadata,))
        order_id = order_cancel.order_id
        status = self.status_order[order_cancel.status]
        transact = order_cancel.transact_at
        dt_utc = datetime.fromtimestamp(transact.seconds + transact.nanos / 1e9, tz=timezone.utc)
        moscow_tz = timezone(timedelta(hours=3))
        dt_msk = dt_utc.astimezone(moscow_tz)
        return {'order_id':order_id,'status':status,'time':dt_msk}

    def orders_info(self,account_id):
        order_stub = OrdersServiceStub(self.channel)
        order_req = orders_service_pb2.OrdersRequest(account_id = account_id)
        order_info = order_stub.GetOrders(order_req,metadata = (self.metadata,))
        result = list()
        for el in order_info.orders: 
            el_dict = MessageToDict(el)
            result.append(self.flatten_dict(el_dict))
        orders = pd.DataFrame(result)
        orders['transactAt'] = pd.to_datetime(orders['transactAt'],format='mixed').dt.tz_convert('Europe/Moscow')
        return orders
    
    def order_info(self,account_id,order_id): 
        order_stub = OrdersServiceStub(self.channel)
        order_req = orders_service_pb2.GetOrderRequest(account_id = account_id,order_id = order_id)
        order_info = order_stub.GetOrder(order_req,metadata = (self.metadata,))
        ord = MessageToDict(order_info.order)
        order_status = self.status_order[order_info.status]
        ord['status'] = order_status
        return self.flatten_dict(ord)
    
    def stream_trades(self,symbol): 
       quotes_stub = MarketDataServiceStub(self.channel)
       request_trades = marketdata_service_pb2.SubscribeLatestTradesRequest(symbol = symbol)
       stream = quotes_stub.SubscribeLatestTrades(request_trades,metadata = (self.metadata,))
       return stream
       try:
        for trade in stream:
            print(trade)
       except KeyboardInterrupt:
            print("Получен Ctrl+C — отменяем подписку...")
       finally:
            # 4) Отмена RPC
            stream.cancel()
            print("Стрим остановлен и канал закрыт.")

