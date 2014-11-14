#!/usr/bin/perl 

# Modules
use strict;
use warnings;
use CGI-Simple;
use DBI;

# Debug
use diagnostics;
use Data::Dumper;

# Database connection properties
my %database = ( 'host'         => '127.0.0.1',
                 'port'         => '3306',
                 'type'         => 'mysql',
                 'name'         => 'test',
                 'user'         => 'root',
                 'password'     => ''
);

# Error log path
our $error_log = './error/system.log';

our %client_status = ( '1' => 'Active',
                      '0' => 'Deactivated',
);

our %status_color = (  '1' => '#40A147',
                      '0' => '#FA6450',
);

my ($second,$minute,$hour,$day,$month,$year) = localtime(time);
$year += 1900; $month += 1;
($month < 10)?($month = '0'.$month):();
($day < 10)?($day = '0'.$day):();
($hour < 10)?($hour = '0'.$hour):();
($minute < 10)?($minute = '0'.$minute):();
($second < 10)?($second = '0'.$second):();

sub DBconnect {
    my $dsn = "DBI:$database{'type'}:database=$database{'name'};host=$database{'host'};port=$database{'port'}";
    my %attr = ('ShowErrorStatement' => 1,
                'RaiseError'         => 1,
                'PrintError'         => 0,
                'AutoCommit'         => 1,
                'HandleError'        => \&LogError
    );
    my $dbh = DBI->connect($dsn, $database{'user'}, $database{'password'}, \%attr) || (&Log2File(DBI->errstr));
    return (\$dbh);
}

# Database query method
sub DBQuery {
    my $Data = &DBconnect();
    my $sth = $$Data->prepare($_[0]);
    $sth->execute();
    my $result = $sth->fetchall_hashref($_[1]);
    $sth->finish();
    $$Data->disconnect();
    return \$result;
}

sub LogError {
# Database error wrapper
# $_[0] - error message
    my ($message, undef, undef) = @_;
    &Log2File($message);
}

sub Log2File {
# Writing program logfile
# $_[0] - logfile message

    my ($message, $file);    
    my $ip = $ENV{'REMOTE_ADDR'} || 'NULL';
    my $url = $ENV{'REQUEST_URI'} || 'NULL';
    my $method = $ENV{'REQUEST_METHOD'} || 'NULL';

    ($_[1])?($file = $_[1]):($file = $error_log);
    ($_[0])?($message = $_[0]):($message = 'NULL');

    open (LOGFILE, '>>', $file);
    print LOGFILE ('['.$day.'.'.$month.'.'.$year.' '.$hour.':'.$minute.':'.$second."]\t[IP: ".$ip."]\t[method: ".$method."]\t< ".$message." >\t\n\tURL: $url\n\n");
    close(LOGFILE);
}

sub GetParams {
# $_[0] - CGI object reference
   my $cgi = $_[0];
   my @names = $$cgi->param;
   my %params = ();
   foreach (@names) {
       $params{$_} = $$cgi->param($_);
   }
   return %params;
}

sub RunController{
# $_[0] - CGI object reference
# $_[1] - HTTP method
# $_[2] - parametrs array

   my $cgi = shift;
   my $method = shift;
   my %params = @_;

   my $cmd = $params{'cmd'};
   
    my $controller = './controllers/'.$cmd.'.cgi';
    if(!$cmd || $cmd =~ /^\s*$/) {
        require './controllers/clients_list.cgi';;
    }
    elsif (-e $controller) {
        require $controller;
    }
    else {
        require "./controllers/404.cgi";
    }
    
    &RUN(\$$cgi, %params);

}


1;