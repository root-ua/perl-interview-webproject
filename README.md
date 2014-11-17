perl-interview-webproject
=========================

Interview task for Perl vacancy

It is necessary to create small database (MySQL). There should be two tables: 
client (client_id, first_name, last_name, is_active)
invoice (invoice_id, client_id, invoice_amount, invoice_date, payment_date)

Fill DB with some test data using SQL script.

When DB is ready, prepare simple Perl web page. It should show in one grid information about active clients, total invoices for client, amount of paid invoices for client, amount of not paid invoices for client, amount of client invoices with non-paid amounts during 30 days, 60 days, 90 days, more then 90 days.

There is no need to edit data on UI. Just show there in the grid such report.

Page should be accurate. But there is no need in fancy design.

Time for implementation - 4-8 hours.
