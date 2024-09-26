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
        self.overhead_cost = sum([
            self.material_operating_margins or 0,
            self.material_tool_charges or 0,
            self.insurance or 0,
            self.transportation or 0,
            self.material_wastage or 0,
            self.miscellaneous or 0
        ])
        self.total_material_and_over_head_cost = (self.overhead_cost or 0) + (self.material_cost or 0)

    def calculate_labour_costs(self):
        self.total_labour_overhead = sum([
            self.labour_operating_margins or 0,
            self.labour_tool_charges or 0,
            self.engineering_charges or 0,
            self.supervision_charges or 0,
            self.admin_charges or 0,
            self.labour_miscellaneous or 0
        ])
        self.total_overhead_and_labour_cost = (self.total_labour_overhead or 0) + (self.labour_cost or 0)

    def calculate_final_costs(self):
        # Calculate final material cost after discount
        material_discount_factor = 1 - (self.material_discount or 0) / 100
        self.final_material_cost = self.total_material_and_over_head_cost * material_discount_factor

        # Calculate final labour cost after discount
        labour_discount_factor = 1 - (self.labour_discount or 0) / 100
        self.final_labour_cost = self.total_overhead_and_labour_cost * labour_discount_factor

        # Calculate final cost
        self.final_cost = self.final_material_cost + self.final_labour_cost

    @staticmethod
    def safe_multiply(a, b):
        if a is None or b is None:
            return 0
        return float(a) * float(b)

def calculate_child_table_totals(doc, method):
    for item in doc.item_details:
        item.amount = Products.safe_multiply(item.rate, item.qty)

    for labour in doc.labour_details:
        labour.amount = Products.safe_multiply(labour.rate, labour.qty)
