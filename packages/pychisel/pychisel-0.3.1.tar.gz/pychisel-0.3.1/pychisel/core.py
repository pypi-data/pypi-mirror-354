import pandas as pd
from typing import Dict, List, Tuple, Union, Optional
from .exceptions import SplittingError

class Splitter:
    def __init__(self,
                 drop_original: bool = True,
                 ref_prefix: str = 'ref_',
                 id_suffix: str = '_id',):
        """
        Initalise the splitter with config options
        :param drop_original: Wether to drop original columns after splitting
        :param ref_prefix: prefix for reference tables names
        :param id_suffix: suffix for ID columns
        """

        self.drop_original = drop_original
        self.ref_prefix = ref_prefix
        self.id_suffix = id_suffix

    def split(self,
                df: pd.DataFrame,
                # Accepts strings or list as dtype
                columns: Union[str, List[str]],
                inplace: bool = False) ->  Tuple[pd.DataFrame,Dict[str, pd.DataFrame]]:
        """
        Split columns in a dataframe, creating a reference column in the
        original dataframe and the description value in another dataframe.

        Args:
            df: Input Dataframe
            columns: Columns to split
            inplace: Inplace operation

        Return:
             Tuple of (splitted Dataframe, dictionary of reference tables)

        """
        # If the user wants it to do not touch the dataframe (very unlikely)
        if not inplace:
            df = df.copy()

        # Checks if the column name is a string, and make it a list of one item
        if isinstance(columns, str):
            columns = [columns]

        ref_tables = {}

        for col in columns:
            if col not in df.columns:
                raise SplittingError(f'Column {col} not found in dataframe')

            # Create reference table
            ref_df = df[[col]].drop_duplicates()
            # Resets the index and name it
            ref_df.index.name =  f'{col}{self.id_suffix}'
            ref_df =  ref_df.reset_index()

            # Store reference table ind dict (like ref_municipio)
            ref_tables[f'{self.ref_prefix}{col}'] = ref_df

            # Merge ID back to original dataframe
            df = df.merge(ref_df[[col, f'{col}{self.id_suffix}']],
                          on=col,
                          how='left')

            if self.drop_original:
                df.drop(col, axis=1, inplace=True)

        return df, ref_tables

def split(df: pd.DataFrame,
          columns: Union[str, List[str]],
          **kwargs) -> Tuple[pd.DataFrame,Dict[str, pd.DataFrame]]:
    """
    Convenience function for eventual usage of Splitter.
    Basically it is a wrapper, so you don't have to instantiate Splitter
    directly.
    """
    splitter = Splitter(**kwargs)
    return splitter.split(df, columns)
