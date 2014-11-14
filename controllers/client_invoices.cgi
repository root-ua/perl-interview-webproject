#!/usr/bin/perl 

# Modules
use strict;
use warnings;

# Debug
use diagnostics;
use Data::Dumper;

# Global vars
our %client_status;
our %status_color;

# Main render method
sub RUN {
# $_[0] - CGI object reference
    my $cgi = shift;
    my %params = @_;
    
    my $title = 'Client invoices :: System';
    
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
[HTML]

    my $c_id = $params{'id'} || 1;
    &GetClientInfo($c_id);
    
    # HTML page footer
    print $$cgi->end_html();
}

sub GetClientInfo {
    
    my $c_id = shift;
    my $client   = &DBQuery("SELECT `client_id`, `first_name`, `last_name`, `is_active` FROM `client` WHERE `client_id` = '$c_id'", 'client_id');
    my $invoices = &DBQuery("SELECT `invoice_id`, `client_id`, `invoice_amount`, `invoice_date`, `payment_date` FROM `invoice` WHERE `client_id` = '$c_id'", 'invoice_id');

print <<"[HTML]";
<div align="center">
<table cellspacing="2" cellpadding="2" align="center">
<tr bgcolor="#C7C7C7">
    <th>Full name</th>
    <th>Status</th>
</tr>
[HTML]

foreach my $id (sort keys %{$$client}){
    my $full_name = $$client->{$id}{'first_name'}.' '.$$client->{$id}{'last_name'};
    my $status_text = $client_status{$$client->{$id}{'is_active'}};
    my $status_color = $status_color{$$client->{$id}{'is_active'}};
print <<"[HTML]";
    <tr bgcolor="$status_color">
        <td><a href="./index.cgi?cmd=client_invoices&id=$id">$full_name</a></td>
        <td>$status_text</td>
    </tr>
[HTML]
}

print <<"[HTML]";
</table>
</div>
<br/><br/>
[HTML]


print <<"[HTML]";
<div align="center">
<table cellspacing="2" cellpadding="2" align="center">
<tr bgcolor="#C7C7C7">
    <th>#</th>
    <th align="center">Invoice amount</th>
    <th align="center">Invoice date</th>
    <th align="center">Payment date</th>
</tr>
[HTML]
my $i = 1;
my ($paid, $unpaid) = (0, 0);
foreach my $id (sort keys %{$$invoices}){
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
