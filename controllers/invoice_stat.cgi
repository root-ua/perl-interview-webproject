#!/usr/bin/perl 

# Modules
use strict;
use warnings;

# Debug
use diagnostics;
use Data::Dumper;

# Main render method
sub RUN {
# $_[0] - CGI object reference
    my $cgi = shift;
    my %params = @_;
    my $days = $params{'days'} || 30;
    my $title = "Invoice statistics for last <font color=\"red\">$days</font> days :: System";
    
    # HTML page header
    print $$cgi->start_html(
        -title    => $title,
    );
    
print <<"[HTML]";
<style>
body {
    font-family:  Verdana;
    font-size: 14pt;
}
</style>
<div align="center">
<table cellspacing="2" cellpadding="2" align="center">
    <tr style="background-color: #E8E8E8;">
        <td align="center" width="200"><a href="./index.cgi?cmd=clients_list">Clients</a></td>
        <td align="center" width="200"><a href="./index.cgi?cmd=invoices_list">Invoices</a></td>
    </tr>
</table>
</div>
<br/><br/>
<div align="center"><b>$title</b></div>
<br/>
<div align="center">Statistics: <a href="./index.cgi?cmd=invoice_stat&days=30">last 30 days</a> |
<a href="./index.cgi?cmd=invoice_stat&days=60">last 60 days</a> |
<a href="./index.cgi?cmd=invoice_stat&days=90">last 90 days</a> |
<a href="./index.cgi?cmd=invoice_stat&days=180">more than 90 days</a></div><br/>
[HTML]

    &GetInvoices($days);
    
    # HTML page footer
    print $$cgi->end_html();
}

sub GetInvoices {
    
    my $days = shift;
    my $invoices = &DBQuery("SELECT `i`.`invoice_id`, `c`.`first_name`, `c`.`last_name`, `i`.`client_id`, `i`.`invoice_amount`, `i`.`invoice_date`,
                           `i`.`payment_date` FROM `invoice` AS `i` INNER JOIN `client` AS `c` ON `i`.`client_id` = `c`.`client_id`
                           WHERE `i`.`invoice_date` > SUBDATE(NOW(), INTERVAL $days DAY)", 'invoice_id');

print <<"[HTML]";
<div align="center">
<table cellspacing="2" cellpadding="2" align="center">
<tr bgcolor="#C7C7C7">
    <th align="center">#</th>
    <th align="center">Full name</th>
    <th align="center">Invoice amount</th>
    <th align="center">Invoice date</th>
    <th align="center">Payment date</th>
</tr>
[HTML]

my $i = 1;
my ($paid, $unpaid) = (0, 0);
foreach my $id (sort keys %{$$invoices}){
    my $full_name = $$invoices->{$id}{'first_name'}.' '.$$invoices->{$id}{'last_name'};
    my $invoice_amount = $$invoices->{$id}{'invoice_amount'};
    my $payment_date = $$invoices->{$id}{'payment_date'};
    my $invoice_date = $$invoices->{$id}{'invoice_date'};

    # 1: paid invoice; 0: unpaid invoice
    my $invoice_status = (!$payment_date || $payment_date =~ /^\s*$/ )?(0):(1);
    my $color = (!$payment_date || $payment_date =~ /^\s*$/ )?('#FA6450'):('#40A147');

    if($invoice_status == 1){
        $paid += $invoice_amount;
    }
    else{
        $unpaid += $invoice_amount;
    }
    
print <<"[HTML]";
    <tr bgcolor="$color">
        <td align="center">$i</td>
        <td align="center"><a href="./index.cgi?cmd=client_invoices&id=$id">$full_name</a></td>
        <td align="center">$invoice_amount</td>
        <td align="center">$invoice_date</td>
        <td align="center">$payment_date</td>
    </tr>
[HTML]
$i++;
}

$i--;
print <<"[HTML]";
<tr><td colspan="5">&nbsp;</td></tr>
<tr><td colspan="5">Total invoices: $i</td></tr>
<tr bgcolor="#40A147"><td colspan="3">Total amount of paid invoices:</td><td colspan="2" align="center">$paid</td></tr>
<tr bgcolor="#FA6450"><td colspan="3">Total amount of unpaid invoices:</td><td colspan="2" align="center">$unpaid</td></tr>
</table>
</div>
[HTML]

}

1;
