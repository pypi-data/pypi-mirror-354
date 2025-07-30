import pytest
from csv_stringify.core import (
    CSVStringifier, stringify, stringify_sync, 
    stringify_records, stringify_rows
)

class TestCSVStringifier:
    
    def setup_method(self):
        self.stringifier = CSVStringifier()
        self.sample_data = [["John", "25", "New York"], ["Jane", "30", "London"]]
        self.sample_headers = ["Name", "Age", "City"]
        self.sample_dicts = [
            {"Name": "John", "Age": "25", "City": "New York"},
            {"Name": "Jane", "Age": "30", "City": "London"}
        ]
    
    def test_stringify_list_of_lists_without_headers(self):
        result = self.stringifier.stringify(self.sample_data, header=False)
        expected = "John,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_stringify_list_of_lists_with_headers(self):
        result = self.stringifier.stringify(self.sample_data, 
                                          columns=self.sample_headers, 
                                          header=True)
        expected = "Name,Age,City\nJohn,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_stringify_list_of_dicts_with_header(self):
        result = self.stringifier.stringify(self.sample_dicts, header=True)
        expected = "Name,Age,City\nJohn,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_stringify_list_of_dicts_without_header(self):
        result = self.stringifier.stringify(self.sample_dicts, header=False)
        expected = "John,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_stringify_empty_data(self):
        result = self.stringifier.stringify([])
        assert result == ""
    
    def test_stringify_records(self):
        result = self.stringifier.stringify_records(self.sample_dicts)
        expected = "Name,Age,City\nJohn,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_stringify_rows(self):
        result = self.stringifier.stringify_rows(self.sample_data, 
                                               columns=self.sample_headers)
        expected = "Name,Age,City\nJohn,25,New York\nJane,30,London\n"
        assert result == expected
    
    def test_custom_delimiter(self):
        stringifier = CSVStringifier(delimiter=';')
        result = stringifier.stringify(self.sample_data, header=False)
        expected = "John;25;New York\nJane;30;London\n"
        assert result == expected
    
    def test_custom_quote_char(self):
        stringifier = CSVStringifier(quote_char="'")
        data = [["John, Jr.", "25"], ["Jane", "30"]]
        result = stringifier.stringify(data, header=False)
        expected = "'John, Jr.',25\nJane,30\n"
        assert result == expected
    
    def test_quote_mode_all(self):
        stringifier = CSVStringifier(quote_mode='all')
        result = stringifier.stringify(self.sample_data, header=False)
        expected = '"John","25","New York"\n"Jane","30","London"\n'
        assert result == expected

class TestConvenienceFunctions:
    
    def setup_method(self):
        self.sample_data = [["1", "2", "3"], ["a", "b", "c"]]
        self.sample_dicts = [{"col1": "1", "col2": "2"}, {"col1": "a", "col2": "b"}]
    
    def test_stringify(self):
        result = stringify(self.sample_data, header=False)
        expected = "1,2,3\na,b,c\n"
        assert result == expected
    
    def test_stringify_sync(self):
        result = stringify_sync(self.sample_data, header=False)
        expected = "1,2,3\na,b,c\n"
        assert result == expected
    
    def test_stringify_records(self):
        result = stringify_records(self.sample_dicts)
        expected = "col1,col2\n1,2\na,b\n"
        assert result == expected
    
    def test_stringify_rows(self):
        result = stringify_rows(self.sample_data, columns=["A", "B", "C"])
        expected = "A,B,C\n1,2,3\na,b,c\n"
        assert result == expected
    
    def test_stringify_with_options(self):
        result = stringify(self.sample_data, delimiter=';', header=False)
        expected = "1;2;3\na;b;c\n"
        assert result == expected

class TestEdgeCases:
    
    def test_single_row(self):
        data = [["single", "row"]]
        result = stringify(data, header=False)
        expected = "single,row\n"
        assert result == expected
    
    def test_single_column(self):
        data = [["a"], ["b"], ["c"]]
        result = stringify(data, header=False)
        expected = "a\nb\nc\n"
        assert result == expected
    
    def test_mixed_types(self):
        data = [["text", 123, True], ["more", 456, False]]
        result = stringify(data, header=False)
        expected = "text,123,True\nmore,456,False\n"
        assert result == expected
    
    def test_with_commas_and_quotes(self):
        data = [['John, Jr.', 'Says "Hello"'], ['Jane', 'Normal text']]
        result = stringify(data, header=False)
        expected = '"John, Jr.","Says ""Hello"""\nJane,Normal text\n'
        assert result == expected