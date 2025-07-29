from gradio.components.base import Component


class TabulaLite(Component):
    def __init__(self, value=None, rows_per_page=10, label=None, **kwargs):
        super().__init__(label=label, **kwargs)
        
        # print(f"__init__ 1:\n {value}")
        self.value = value if value is not None else pd.DataFrame()
        self.rows_per_page = rows_per_page
        # print(f"__init__ self.value:\n {self.value}")
        # print(f"__init__ self.rows_per_page:\n {self.rows_per_page}")

 
    def get_config(self):
        # print(f"get_config:\n {self.value}")
        return {
            "rows_per_page": self.rows_per_page,
            "value": self.value  # 👈 Add this to pass to frontend
        }

    def preprocess(self, x):
       #print(f"preprocess x:\n {x}")
       return x
   
    def on_select(self, payload):
        #print("Received payload:", payload)
        return f"Hello {payload['name']}, age {payload['age']}"

    def postprocess(self, y):
        # y: receives selected row from frontend
        
        # Ensure the component value is returned as JSON-compatible list of dicts
        #print(f"postprocess 1 y:\n {y}")
        #print(f"postprocess 1 self:\n {self}")

        if isinstance(y, pd.DataFrame):
            return y.to_dict(orient="records")
        
        #print(f"postprocess 2 y:\n {y}")
        return y

    def create_large_dataframe(size=1000):
        return pd.DataFrame({
            "ID": np.arange(1, size + 1),
            "Name": [f"Name_{i}" for i in range(1, size + 1)],
            "Value": np.random.randint(100, 1000, size=size),
            "Category": np.random.choice(['A', 'B', 'C', 'D'], size=size),
            "Timestamp": pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, size=size), unit='D')
        })

    def get_paginated_data(df, page, rows_per_page):
        print(f"get_paginated_data 2:\n {df}")
        total_rows = len(df)
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page
        page = max(1, min(page, total_pages))
        start = (page - 1) * rows_per_page
        end = start + rows_per_page
        return df.iloc[start:end], page, total_pages

    def api_info(self):
        return {
            "type": "component",
            "input_type": "json",
            "output_type": "json"
        }
        
    def example_payload(self):
        # Provide a small dummy DataFrame as a JSON-compatible example
        return [
            {"ID": 1, "Name": "Example", "Value": 123, "Category": "A", "Timestamp": "2023-01-01"}
        ]

    class JS:
        import_path = "frontend"
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component
