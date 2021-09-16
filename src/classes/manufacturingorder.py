from .baseclass import DataList, DataObject
from datetime import date


class ManufacturingOrder(DataObject):
    number: str
    material: str
    material_description: str
    description: str
    order_type: str
    plant: int
    target_qty: float
    unit: str
    date_start: date
    date_finish: date
    date_change: date
    date_created: date
    release: int
    bom_number: int
    bom_status: int


class ManufacturingOrderList(DataList):
    # TODO: Convert strings to date objects
    table: str
    table_dict: dict

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.table = "cockpitdata.cooisproductionarchive"
        self.table = "cockpitdata.cooisplannedarchive_prev30"
        self.table_dict = {
            "Order": "number",
            "Material": "material",
            "Order Type": "order_type",
            "Plant": "plant",
            "Target qty": "target_qty",
            "Unit": "unit",
            "Mat.Descr.": "material_description",
            "BOM": "bom_number",
            "BOM status": "bom_status",
            "Desc": "description",
        }
