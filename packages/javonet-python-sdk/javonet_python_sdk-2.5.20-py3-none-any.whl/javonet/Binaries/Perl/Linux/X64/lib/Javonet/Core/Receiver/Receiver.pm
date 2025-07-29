package Javonet::Core::Receiver::Receiver;
use strict;
use warnings;
use Config;
use File::Basename;

use Exporter qw(import);
our @EXPORT = qw(heart_beat send_command get_runtime_info);

my $perlLibDirJavonet;
my $perlLibDirDeps;

BEGIN {
    my $thisFileDir = dirname(__FILE__);
    $perlLibDirJavonet = "$thisFileDir/../../../";
    $perlLibDirDeps = "$thisFileDir/../../../../deps/lib/perl5"
}

use lib "$perlLibDirJavonet";
use lib "$perlLibDirDeps";
use aliased 'Javonet::Core::Interpreter::Interpreter' => 'Interpreter';
use aliased 'Javonet::Sdk::Core::RuntimeLogger' => 'RuntimeLogger';
#
sub heart_beat {
    my ($self, $message_byte_array_ref) = @_;
    my @response_byte_array = (49, 48);
    return \@response_byte_array;
}

sub send_command {
    my ($self, $message_byte_array_ref) = @_;
    my @message_byte_array = @$message_byte_array_ref;
    my @response_byte_array = Javonet::Core::Interpreter::Interpreter->process(\@message_byte_array);
    return \@response_byte_array;
}

sub get_runtime_info {
    return RuntimeLogger->rl_get_runtime_info();
}

1;
