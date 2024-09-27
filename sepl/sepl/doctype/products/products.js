frappe.ui.form.on('Products', {
    refresh: function(frm) {
        frm.fields_dict['item_details'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                    'is_stock_item': 1
                }
            };
        };
    }
});

frappe.ui.form.on('Item Details', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            frappe.call({
                method: 'get_item_details',
                doc: frm.doc,
                args: {
                    item_code: row.item_code
                },
                callback: function(r) {
                    if (r.message) {
                        // Store the current qty
                        let currentQty = row.qty;
                        
                        frappe.model.set_value(cdt, cdn, {
                            'item_name': r.message.item_name,
                            'uom': r.message.uom,
                            'category': r.message.category,
                            'thicknesssq_mm': r.message.thicknesssq_mm,
                            'length_ft': r.message.length_ft,
                            'color': r.message.color,
                            'brand': r.message.brand,
                            'rate': r.message.rate,
                            'size': r.message.size,
                            'qty': currentQty || r.message.qty // Use current qty if it exists, otherwise use from item master
                        });
                    }
                }
            });
        }
    },
    
    qty: function(frm, cdt, cdn) {
        // This function will be triggered when qty is changed manually
        let row = locals[cdt][cdn];
        if (row.rate && row.qty) {
            frappe.model.set_value(cdt, cdn, 'amount', row.rate * row.qty);
        }
    }
});

