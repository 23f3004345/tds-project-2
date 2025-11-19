import PyPDF2
import pandas as pd
import json
import os
from typing import Any, Union
from PIL import Image
import base64
from io import BytesIO

class DataProcessor:
    """Handles data processing tasks for various file formats"""
    
    def extract_text_from_pdf(self, pdf_path: str, page_number: int = None) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to PDF file
            page_number: Specific page to extract (1-indexed), or None for all pages
            
        Returns:
            Extracted text
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if page_number is not None:
                    # Extract specific page (convert to 0-indexed)
                    page = pdf_reader.pages[page_number - 1]
                    return page.extract_text()
                else:
                    # Extract all pages
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n\n"
                    return text
                    
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
            
    def read_csv(self, csv_path: str) -> pd.DataFrame:
        """Read CSV file into pandas DataFrame"""
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            # Try with different encodings
            try:
                return pd.read_csv(csv_path, encoding='latin-1')
            except:
                return pd.read_csv(csv_path, encoding='utf-8', errors='ignore')
                
    def read_excel(self, excel_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """Read Excel file into pandas DataFrame"""
        try:
            return pd.read_excel(excel_path, sheet_name=sheet_name)
        except Exception as e:
            print(f"Error reading Excel: {e}")
            return pd.DataFrame()
            
    def get_data_summary(self, file_path: str) -> str:
        """
        Get a summary of data from a file
        
        Args:
            file_path: Path to data file (CSV, Excel, JSON)
            
        Returns:
            Summary as string
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.csv':
                df = self.read_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                df = self.read_excel(file_path)
            elif ext == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return json.dumps(data, indent=2)
            else:
                return f"Unsupported file type: {ext}"
                
            # Generate summary for DataFrame
            summary = f"Shape: {df.shape}\n\n"
            summary += f"Columns: {list(df.columns)}\n\n"
            summary += f"First few rows:\n{df.head(10).to_string()}\n\n"
            summary += f"Data types:\n{df.dtypes.to_string()}\n\n"
            summary += f"Basic statistics:\n{df.describe().to_string()}\n"
            
            return summary
            
        except Exception as e:
            return f"Error processing file: {e}"
            
    def create_visualization(self, data: pd.DataFrame, chart_type: str = "bar") -> str:
        """
        Create a visualization and return as base64 encoded string
        
        Args:
            data: DataFrame to visualize
            chart_type: Type of chart (bar, line, scatter, etc.)
            
        Returns:
            Base64 encoded image string with data URI prefix
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "bar":
                data.plot(kind='bar', ax=ax)
            elif chart_type == "line":
                data.plot(kind='line', ax=ax)
            elif chart_type == "scatter" and len(data.columns) >= 2:
                ax.scatter(data.iloc[:, 0], data.iloc[:, 1])
            else:
                data.plot(ax=ax)
                
            plt.tight_layout()
            
            # Save to bytes
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            
            # Encode to base64
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close(fig)
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            print(f"Error creating visualization: {e}")
            return ""
            
    def parse_json_data(self, json_str: str) -> Any:
        """Parse JSON string into Python object"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
            
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        import re
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters if needed
        text = text.strip()
        return text
        
    def aggregate_data(self, df: pd.DataFrame, group_by: str, agg_column: str, 
                       agg_func: str = "sum") -> pd.DataFrame:
        """
        Aggregate data by grouping
        
        Args:
            df: DataFrame to aggregate
            group_by: Column to group by
            agg_column: Column to aggregate
            agg_func: Aggregation function (sum, mean, count, etc.)
            
        Returns:
            Aggregated DataFrame
        """
        try:
            if agg_func == "sum":
                return df.groupby(group_by)[agg_column].sum().reset_index()
            elif agg_func == "mean":
                return df.groupby(group_by)[agg_column].mean().reset_index()
            elif agg_func == "count":
                return df.groupby(group_by)[agg_column].count().reset_index()
            elif agg_func == "max":
                return df.groupby(group_by)[agg_column].max().reset_index()
            elif agg_func == "min":
                return df.groupby(group_by)[agg_column].min().reset_index()
            else:
                return df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
        except Exception as e:
            print(f"Aggregation error: {e}")
            return df
