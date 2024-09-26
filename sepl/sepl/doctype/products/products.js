// Copyright (c) 2024, Thunder and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Products", {
// 	refresh(frm) {

// 	},
// });



// frappe.ui.form.on('YourParentDoctype', {
//     after_save: function(frm) {
//         let total_amount = 0;

//         // Iterate over each row in the child table and sum up the amount
//         $.each(frm.doc.item_details || [], function(i, row) {
//             total_amount += row.amount;
//         });

//         // Set the total amount in the material_cost field
//         frm.set_value('material_cost', total_amount);

//         // Refresh the field to show the updated value
//         frm.refresh_field('material_cost');
//     }
// });