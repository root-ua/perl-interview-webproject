#!/usr/bin/perl 

# Modules
use strict;
use warnings;

# Debug
use diagnostics;
use Data::Dumper;

# Include functions file
require "./functions.cgi";

# Init CGI
my $cgi = CGI->new();
my $method = $cgi->request_method() || 'GET';
my %params = &GetParams(\$cgi);

# HTTP headers
print $cgi->header(
   -type     => 'text/html',
   -charset  => 'UTF-8',
);

# Run controllers
&RunController(\$cgi, $method, %params);
