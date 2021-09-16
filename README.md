# mysqldataclass

mysqldataclass is a Python library for easily creating objects from a database

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install mysqldataclass .

```bash
pip install mysqldataclass 
```

## Usage

```python
import mysqldataclass

# Inherit DataObject
Inherit DataObject to create unique classes for your table objects

example:
class PurchaseReq(DataObject):
    number: str
    material: str
    short_text: str
    quantity: float
    unit: str
    date_release_str: str
    date_release: date
    date_delivery_str: str
    date_delivery: date
    date_change_str: str
    date_change: date
    date_request_str: str
    date_request: date
    purchase_order_number: int
    date_purchase_order_str: str
    date_purchase_order: date
    department: str
    vendor_number: int
    vendor_name: str

# Inherit DataList
Inherit DataList to easily fill data from a database table

example:
class PurchaseReqList(DataList):
    table: str
    table_dict: dict

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.table = "cockpitdata.purchasereqnc"
        self.table_dict = {
            "Purch.Req.": "number",
            "Material": "material",
            "Short Text": "short_text",
            "Quantity": "quantity",
            "Un": "EA",
            "Release Dt": "date_release_str",
            "Deliv.Date": "date_delivery_str",
            "Chngd On": "date_changed_str",
            "Req. Date": "date_request_str",
            "PO": "purchase_order_number",
            "PO Date": "date_purchase_order_str",
            "Requisnr.": "department",
            "Fixed vend": "vendor_number",
            "Name of Vendor": "vendor_name",
        }

table = table you want to access
table_dict = column : variable_name

your new object will be created with the provided variable name attributes.

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)