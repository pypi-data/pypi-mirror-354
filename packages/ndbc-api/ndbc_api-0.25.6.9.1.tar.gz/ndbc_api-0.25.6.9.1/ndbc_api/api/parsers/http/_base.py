from io import StringIO
from typing import List, Tuple

import pandas as pd

from ndbc_api.exceptions import ParserException


class BaseParser:

    HEADER_PREFIX = '#'
    NAN_VALUES = ['MM']
    DATE_PARSER = '%Y %m %d %H %M'
    PARSE_DATES = [0, 1, 2, 3, 4]
    INDEX_COL = False
    REVERT_COL_NAMES = []

    @classmethod
    def df_from_responses(cls,
                          responses: List[dict],
                          use_timestamp: bool = True) -> pd.DataFrame:
        components = []
        for response in responses:
            if response.get('status') == 200:
                components.append(
                    cls._read_response(response, use_timestamp=use_timestamp))
        df = pd.concat(components)
        if use_timestamp:
            try:
                df = df.reset_index().drop_duplicates(subset='timestamp',
                                                      keep='first')
                df = df.set_index('timestamp').sort_index()
            except KeyError as e:
                raise ParserException from e
        return df

    @classmethod
    def _read_response(cls, response: dict,
                       use_timestamp: bool) -> pd.DataFrame:
        body = response.get('body')
        header, data = cls._parse_body(body)
        names = cls._parse_header(header)
        if not data:
            return pd.DataFrame()
        # check that parsed names match parsed values or revert
        if len([v.strip() for v in data[0].strip('\n').split(' ') if v
               ]) != len(names):
            names = cls.REVERT_COL_NAMES
        if '(' in data[0]:
            data = cls._clean_data(data)

        try:
            parse_dates = False
            date_format = None
            if use_timestamp:
                parse_dates = [cls.PARSE_DATES]
                date_format = cls.DATE_PARSER
            df = pd.read_csv(
                StringIO('\n'.join(data)),
                names=names,
                delim_whitespace=True,
                na_values=cls.NAN_VALUES,
                index_col=cls.INDEX_COL,
                parse_dates=parse_dates,
                date_format=date_format,
            )
            if use_timestamp:
                df.index.name = 'timestamp'

        except (NotImplementedError, TypeError, ValueError) as e:
            print(e)
            return pd.DataFrame()

        # check whether to parse dates
        return df

    @staticmethod
    def _parse_body(body: str) -> Tuple[List[str], List[str]]:
        buf = StringIO(body)
        data = []
        header = []

        line = buf.readline()
        while line:
            if line.startswith('#'):
                header.append(line)
            else:
                data.append(line)
            line = buf.readline()

        return header, data

    @staticmethod
    def _parse_header(header: List[str]) -> List[str]:
        names = ([n for n in header[0].strip('#').strip('\n').split(' ') if n]
                 if isinstance(header, list) and len(header) > 0 else None)
        return names  # pass 'None' to pd.read_csv on error

    @staticmethod
    def _clean_data(data: List[str]) -> List[str]:
        vals = [
            ' '.join([v
                      for v in r.split(' ')
                      if v and '(' not in v])
            for r in data
        ]
        return vals or None  # pass 'None' to pd.read_csv on error
