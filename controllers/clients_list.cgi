#!/usr/bin/perl 

# Modules
use strict;
use warnings;

# Debug
use diagnostics;
use Data::Dumper;

our %client_status;
our %status_color;

# Main render method
sub RUN {
# $_[0] - CGI object reference
    my $cgi = $_[0];
    my $title = 'Clients list :: System';
    
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

    &GetClients();
    
    # HTML page footer
    print $$cgi->end_html();
}

sub GetClients {
    
    my $clients = &DBQuery("SELECT `client_id`, `first_name`, `last_name`, `is_active` FROM `client`", 'client_id');

print <<"[HTML]";
<div align="center">
<table cellspacing="2" cellpadding="2" align="center">
<tr bgcolor="#C7C7C7">
    <th>#</th>
    <th>Full name</th>
    <th>Status</th>
</tr>
[HTML]

my $i = 1;
foreach my $id (sort keys %{$$clients}){
    my $full_name = $$clients->{$id}{'first_name'}.' '.$$clients->{$id}{'last_name'};
    my $status_text = $client_status{$$clients->{$id}{'is_active'}};
    my $status_color = $status_color{$$clients->{$id}{'is_active'}};
print <<"[HTML]";
    <tr bgcolor="$status_color">
        <td>$i</td>
        <td><a href="./index.cgi?cmd=client_invoices&id=$id">$full_name</a></td>
        <td>$status_text</td>
    </tr>
[HTML]
$i++;
}

$i--;
print <<"[HTML]";
<tr><td colspan="3">Total clients: $i</td></tr>
</table>
</div>
[HTML]

}

1;
