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
    my $cgi = $_[0];
    my $title = 'Page not found :: System';
    
    # HTML page header
    print $$cgi->start_html(
        -title => $title,
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
<div align="center" style="color: red;"><b>Error 404 :: Page not found!<b></div>
[HTML]

    # HTML page footer
    print $$cgi->end_html();
}

1;
