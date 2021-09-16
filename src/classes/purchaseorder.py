from .baseclass import DataList, DataObject
from datetime import date


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


class PurchaseReqList(DataList):
    # TODO: Convert strings to date objects
    table: str
    table_dict: dict

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # purchasereqs not converted
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


class PurchaseOrderList(DataList):
    pass
