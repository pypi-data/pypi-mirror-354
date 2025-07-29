from .base import BaseChipTransformer
from datetime import date, datetime
import inspect
import numpy as np
import pandas as pd
from neurostats_API.utils import StatsProcessor

class US_F13_Transformer(BaseChipTransformer):
    def __init__(self, ticker, company_name, zone):
        super().__init__(ticker, company_name, zone)

    def process_transform(self, fetched_datas):
        """
        fetched_datas:[
            {

            }, ....
        ]
        """
        if not fetched_datas:
            return self._get_empty_structure()    # 若查無資料，回傳空表結構

        def flatten_nested_data(data_dict, key):
            pop_dict = data_dict.pop(key, {})
            for sub_key, value in pop_dict.items():
                data_dict[f"{key}_{sub_key}"] = value
            
            return data_dict

        result = [flatten_nested_data(data, 'votingAuthority') for data in fetched_datas]

        return_dict = {
            "ticker": self.ticker,
            "company_name": self.company_name,
            "chip_data": pd.DataFrame(result)
        }

        return return_dict

        