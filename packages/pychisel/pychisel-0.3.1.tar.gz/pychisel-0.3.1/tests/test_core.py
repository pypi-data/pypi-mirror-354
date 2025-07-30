# -*- coding: utf-8 -*-
"""
File: test_core.py
Location: pychisel/tests
Created at: 09/06/2025
Author: Anderson Alves Monteiro <https://www.github.com/tekoryu>

Tests for the Splitter class and split function in core.py
"""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pychisel.core import Splitter, split
from pychisel.exceptions import SplittingError


class TestSplitter:
    """Tests for the Splitter class"""

    def setup_method(self):
        """Setup test data for each test method"""
        # Create a sample dataframe for testing
        self.df = pd.DataFrame({
            'city': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Los Angeles'],
            'state': ['NY', 'CA', 'IL', 'NY', 'CA'],
            'population': [8419000, 3980000, 2716000, 8419000, 3980000]
        })

    def test_init_default_params(self):
        """Test Splitter initialization with default parameters"""
        splitter = Splitter()
        assert splitter.drop_original is True
        assert splitter.ref_prefix == 'ref_'
        assert splitter.id_suffix == '_id'

    def test_init_custom_params(self):
        """Test Splitter initialization with custom parameters"""
        splitter = Splitter(drop_original=False, ref_prefix='reference_', id_suffix='_key')
        assert splitter.drop_original is False
        assert splitter.ref_prefix == 'reference_'
        assert splitter.id_suffix == '_key'

    def test_split_single_column(self):
        """Test splitting a single column"""
        splitter = Splitter()
        result_df, ref_tables = splitter.split(self.df, 'city')

        # Check that the original column is dropped
        assert 'city' not in result_df.columns
        assert 'city_id' in result_df.columns

        # Check that the reference table is created correctly
        assert 'ref_city' in ref_tables
        assert len(ref_tables['ref_city']) == 3  # Unique cities: New York, Los Angeles, Chicago
        assert set(ref_tables['ref_city'].columns) == {'city', 'city_id'}

        # Check that the IDs in the result match the reference table
        city_id_map = dict(zip(ref_tables['ref_city']['city'], ref_tables['ref_city']['city_id']))
        expected_ids = [city_id_map[city] for city in self.df['city']]
        assert list(result_df['city_id']) == expected_ids

    def test_split_multiple_columns(self):
        """Test splitting multiple columns"""
        splitter = Splitter()
        result_df, ref_tables = splitter.split(self.df, ['city', 'state'])

        # Check that the original columns are dropped
        assert 'city' not in result_df.columns
        assert 'state' not in result_df.columns
        assert 'city_id' in result_df.columns
        assert 'state_id' in result_df.columns

        # Check that the reference tables are created correctly
        assert 'ref_city' in ref_tables
        assert 'ref_state' in ref_tables
        assert len(ref_tables['ref_city']) == 3  # Unique cities: New York, Los Angeles, Chicago
        assert len(ref_tables['ref_state']) == 3  # Unique states: NY, CA, IL

    def test_split_inplace_false(self):
        """Test splitting with inplace=False"""
        splitter = Splitter()
        original_df = self.df.copy()
        result_df, _ = splitter.split(self.df, 'city', inplace=False)

        # Check that the original dataframe is not modified
        assert_frame_equal(self.df, original_df)

        # Check that the result dataframe is modified
        assert 'city' not in result_df.columns
        assert 'city_id' in result_df.columns

    def test_split_drop_original_false(self):
        """Test splitting with drop_original=False"""
        splitter = Splitter(drop_original=False)
        result_df, _ = splitter.split(self.df, 'city')

        # Check that the original column is kept
        assert 'city' in result_df.columns
        assert 'city_id' in result_df.columns

    def test_split_column_not_found(self):
        """Test splitting a column that doesn't exist"""
        splitter = Splitter()
        with pytest.raises(SplittingError, match="Column nonexistent not found in dataframe"):
            splitter.split(self.df, 'nonexistent')

    def test_split_empty_dataframe(self):
        """Test splitting an empty dataframe"""
        empty_df = pd.DataFrame({'city': []})
        splitter = Splitter()
        result_df, ref_tables = splitter.split(empty_df, 'city')

        assert 'city_id' in result_df.columns
        assert 'ref_city' in ref_tables
        assert len(ref_tables['ref_city']) == 0


def test_split_function():
    """Test the split convenience function"""
    # Create a sample dataframe for testing
    df = pd.DataFrame({
        'city': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Los Angeles'],
        'state': ['NY', 'CA', 'IL', 'NY', 'CA'],
    })

    # Test with default parameters
    result_df, ref_tables = split(df, 'city')

    # Check that the original column is dropped
    assert 'city' not in result_df.columns
    assert 'city_id' in result_df.columns

    # Check that the reference table is created correctly
    assert 'ref_city' in ref_tables

    # Test with custom parameters
    result_df, ref_tables = split(df, 'state', drop_original=False, ref_prefix='reference_', id_suffix='_key')

    # Check that the original column is kept
    assert 'state' in result_df.columns
    assert 'state_key' in result_df.columns

    # Check that the reference table has the custom prefix
    assert 'reference_state' in ref_tables
