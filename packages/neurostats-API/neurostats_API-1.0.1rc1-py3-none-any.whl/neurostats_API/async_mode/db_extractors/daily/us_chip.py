from datetime import datetime, timedelta
from pymongo import ASCENDING, DESCENDING
from .base import BaseDailyTechDBExtractor
from neurostats_API.utils import (
    NotSupportedError, StatsProcessor
)


class AsyncUS_F13DBExtractor(BaseDailyTechDBExtractor):

    def __init__(self, ticker, client, managerTicker=None):
        """
        ticker: Issuer Ticker, 被持有的股票代碼
        managerTicker: 持有者的股票代碼
        """
        super().__init__(ticker, client)
        self.issuerTicker = ticker
        self.managerTicker = managerTicker

        if (self.get_zone() not in ['us']):
            raise NotSupportedError("Supports US Company Only")

    def _get_collection_name(self):
        self.collection_name_map = {"us": "us_F13"}

        return self.collection_name_map.get(self.zone, None)

    def _prepare_query(self, start_date=None, end_date=None, get_latest=False):
        query = {"issuerTicker": self.issuerTicker}

        if (self.managerTicker):
            query.update(
                {
                    "managerTicker": self.managerTicker
                }
            )

        query = self._update_query_with_date(query, start_date, end_date)

        projection = {
            "_id": 0,
        }

        if (get_latest):
            sort = [("reportDate", DESCENDING)]
        else:
            sort = [("reportDate", ASCENDING)]

        return query, projection, sort

    def _update_query_with_date(self, query, start_date, end_date):
        start_date = self._transform_date(start_date)
        end_date = self._transform_date(end_date)

        date_range = {"$gte": start_date, "$lte": end_date}

        query.update({"reportDate": date_range})

        return query

    async def query_data(
        self, start_date=None, end_date=None, get_latest=False
    ):
        result = await super().query_data(start_date, end_date, get_latest)

        return result
