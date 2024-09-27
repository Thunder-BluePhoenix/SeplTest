import frappe
from frappe.model.document import Document

class Products(Document):
    def validate(self):
        self.calculate_item_details()
        self.calculate_labour_details()
        self.calculate_material_costs()
        self.calculate_labour_costs()
        self.calculate_final_costs()

    def calculate_item_details(self):
        total_amount = 0
        for item in self.item_details:
            item.amount = self.safe_multiply(item.rate, item.qty)
            total_amount += item.amount or 0
        self.material_cost = total_amount

    def calculate_labour_details(self):
        total_amount = 0
        for labour in self.labour_details:
            labour.amount = self.safe_multiply(labour.rate, labour.qty)
            total_amount += labour.amount or 0
        self.labour_cost = total_amount

    def calculate_material_costs(self):
        material_cost = self.material_cost or 0
        self.value_after_material_discount = self.safe_multiply(material_cost, (self.material_discount or 0) / 100)
        self.value_after_material_operating_margins = self.safe_multiply(material_cost, (self.material_operating_margins or 0) / 100)
        self.value_after_material_tool_charges = self.safe_multiply(material_cost, (self.material_tool_charges or 0) / 100)
        self.value_after_insurance = self.safe_multiply(material_cost, (self.insurance or 0) / 100)
        self.value_after_transportation = self.safe_multiply(material_cost, (self.transportation or 0) / 100)
        self.value_after_material_wastage = self.safe_multiply(material_cost, (self.material_wastage or 0) / 100)
        self.value_after_miscellaneous = self.safe_multiply(material_cost, (self.miscellaneous or 0) / 100)

        self.overhead_cost = sum([
            self.value_after_material_discount,
            self.value_after_material_operating_margins,
            self.value_after_material_tool_charges,
            self.value_after_insurance,
            self.value_after_transportation,
            self.value_after_material_wastage,
            self.value_after_miscellaneous
        ])
        self.total_material_and_over_head_cost = material_cost + self.overhead_cost

    def calculate_labour_costs(self):
        labour_cost = self.labour_cost or 0
        self.value_after_labour_discount = self.safe_multiply(labour_cost, (self.labour_discount or 0) / 100)
        self.value_after_labour_operating_margins = self.safe_multiply(labour_cost, (self.labour_operating_margins or 0) / 100)
        self.value_after_labour_tool_charges = self.safe_multiply(labour_cost, (self.labour_tool_charges or 0) / 100)
        self.value_after_engineering_charges = self.safe_multiply(labour_cost, (self.engineering_charges or 0) / 100)
        self.value_after_supervision_charges = self.safe_multiply(labour_cost, (self.supervision_charges or 0) / 100)
        self.value_after_admin_charges = self.safe_multiply(labour_cost, (self.admin_charges or 0) / 100)
        self.value_after_labour_miscellaneous = self.safe_multiply(labour_cost, (self.labour_miscellaneous or 0) / 100)

        self.total_labour_overhead = sum([
            self.value_after_labour_discount,
            self.value_after_labour_operating_margins,
            self.value_after_labour_tool_charges,
            self.value_after_engineering_charges,
            self.value_after_supervision_charges,
            self.value_after_admin_charges,
            self.value_after_labour_miscellaneous
        ])
        self.total_overhead_and_labour_cost = labour_cost + self.total_labour_overhead


    def calculate_final_costs(self):
        self.final_cost = self.total_overhead_and_labour_cost + self.total_material_and_over_head_cost

    @staticmethod
    def safe_multiply(a, b):
        if a is None or b is None:
            return 0
        return float(a) * float(b)

    @frappe.whitelist()
    def get_item_details(self, item_code):
        item = frappe.get_doc("Item", item_code)
        return {
            "item_name": item.item_name,
            "uom": item.stock_uom,
            "category": item.custom_category,
            "thicknesssq_mm": item.custom_thicknesssqmm,
            "length_ft": item.custom_lengthft,
            "color": item.custom_color,
            "brand": item.brand,
            "rate": item.custom_rate,
            "size": item.custom_size,
            "qty": item.custom_qty
        }

def calculate_child_table_totals(doc, method):
    for item in doc.item_details:
        item.amount = Products.safe_multiply(item.rate, item.qty)

    for labour in doc.labour_details:
        labour.amount = Products.safe_multiply(labour.rate, labour.qty)
