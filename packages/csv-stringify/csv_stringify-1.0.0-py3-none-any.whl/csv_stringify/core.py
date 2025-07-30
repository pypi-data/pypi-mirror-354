import csv
import io
from typing import List, Dict, Any, Union, Optional, Callable

class CSVStringifier:
    """Main class for converting data to CSV format."""
    
    def __init__(self, delimiter: str = ',', quote_char: str = '"', 
                 line_terminator: str = '\n', quote_mode: str = 'minimal'):
        """
        Initialize CSV stringifier.
        
        Args:
            delimiter: Field delimiter (default: ',')
            quote_char: Quote character (default: '"')
            line_terminator: Line terminator (default: '\n')
            quote_mode: When to quote fields ('minimal', 'all', 'nonnumeric', 'none')
        """
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.line_terminator = line_terminator
        self.quote_mode = self._get_quote_mode(quote_mode)
    
    def _get_quote_mode(self, mode: str) -> int:
        """Convert string quote mode to csv module constant."""
        modes = {
            'minimal': csv.QUOTE_MINIMAL,
            'all': csv.QUOTE_ALL,
            'nonnumeric': csv.QUOTE_NONNUMERIC,
            'none': csv.QUOTE_NONE
        }
        return modes.get(mode, csv.QUOTE_MINIMAL)
    
    def stringify(self, data: Union[List[List[Any]], List[Dict[str, Any]]], 
                  columns: Optional[List[str]] = None,
                  header: bool = True) -> str:
        """
        Convert data to CSV string.
        
        Args:
            data: List of lists or list of dictionaries to convert
            columns: Column names (for list of lists) or field order (for dicts)
            header: Whether to include header row
            
        Returns:
            CSV string
        """
        if not data:
            return ""
        
        output = io.StringIO()
        
        # Handle list of dictionaries
        if data and isinstance(data[0], dict):
            fieldnames = columns or list(data[0].keys())
            writer = csv.DictWriter(
                output,
                fieldnames=fieldnames,
                delimiter=self.delimiter,
                quotechar=self.quote_char,
                lineterminator=self.line_terminator,
                quoting=self.quote_mode
            )
            
            if header:
                writer.writeheader()
            writer.writerows(data)
        
        # Handle list of lists
        else:
            writer = csv.writer(
                output,
                delimiter=self.delimiter,
                quotechar=self.quote_char,
                lineterminator=self.line_terminator,
                quoting=self.quote_mode
            )
            
            if header and columns:
                writer.writerow(columns)
            writer.writerows(data)
        
        result = output.getvalue()
        output.close()
        return result
    
    def stringify_records(self, records: List[Dict[str, Any]], 
                         columns: Optional[List[str]] = None,
                         header: bool = True) -> str:
        """
        Convert list of dictionaries to CSV string.
        
        Args:
            records: List of dictionaries
            columns: Field order (optional)
            header: Whether to include header row
            
        Returns:
            CSV string
        """
        return self.stringify(records, columns, header)
    
    def stringify_rows(self, rows: List[List[Any]], 
                      columns: Optional[List[str]] = None,
                      header: bool = True) -> str:
        """
        Convert list of lists to CSV string.
        
        Args:
            rows: List of lists (rows)
            columns: Column headers (optional)
            header: Whether to include header row
            
        Returns:
            CSV string
        """
        return self.stringify(rows, columns, header)

# Convenience functions (matching Node.js API style)
def stringify(data: Union[List[List[Any]], List[Dict[str, Any]]], 
              **options) -> str:
    """
    Convert data to CSV string.
    
    Args:
        data: Data to convert (list of lists or list of dicts)
        **options: CSVStringifier options
        
    Returns:
        CSV string
        
    Example:
        >>> data = [["1", "2", "3"], ["a", "b", "c"]]
        >>> result = stringify(data)
        >>> print(result)
        1,2,3
        a,b,c
    """
    stringifier = CSVStringifier(**{k: v for k, v in options.items() 
                                   if k in ['delimiter', 'quote_char', 'line_terminator', 'quote_mode']})
    stringify_options = {k: v for k, v in options.items() 
                        if k in ['columns', 'header']}
    return stringifier.stringify(data, **stringify_options)

def stringify_sync(data: Union[List[List[Any]], List[Dict[str, Any]]], 
                   **options) -> str:
    """
    Synchronous API for converting data to CSV string (alias for stringify).
    
    Args:
        data: Data to convert
        **options: Stringifier options
        
    Returns:
        CSV string
    """
    return stringify(data, **options)

def stringify_records(records: List[Dict[str, Any]], **options) -> str:
    """
    Convert list of dictionaries to CSV string.
    
    Args:
        records: List of dictionaries
        **options: Stringifier options
        
    Returns:
        CSV string
    """
    return stringify(records, **options)

def stringify_rows(rows: List[List[Any]], **options) -> str:
    """
    Convert list of lists to CSV string.
    
    Args:
        rows: List of lists
        **options: Stringifier options
        
    Returns:
        CSV string
    """
    return stringify(rows, **options)