#!/usr/bin/perl

$dataModelBaseURI="http://learningsparql/sqlite/model#" ;
$dataBaseURI="http://learningsparql/sqlite/data#" ;

print "\@prefix m: <$dataModelBaseURI> . \n";
print "\@prefix d: <$dataBaseURI> . \n\n";

while(<>) {
    chop($_);
    s/\\/\\\\/g;   # escape slashes in data
    s/\"/\\\"/g;  # escape " in data
    @fields = split(/\t/,$_);
    if ($. == 1) {   # if it's the first line, save values as property names
        @properties = @fields;
        foreach $i (@properties) {
            $i = "m:" . $i;
        }
    }
    else {
        print "[\n";
        $i = 0;
        while ($i < @properties) {
            # " chars get escaped above; if the value is a JSON string
            # where they're already escaped, ignore the value for now.
            if ($fields[$i] =~ /\\\"\{/) {
                $fields[$i] = "***** some JSON string *********";
            }
            # To get rid of binary data, I tried throwing out just
            # control characters, but some chars still messed things
            # up. For now, throw out all non-ASCII chars.
            if ($fields[$i] =~ /([\x{0000}-\x{0013}]|[\x{007F}-\x{FFFF}])/) {    
                $fields[$i] = "***** some binary value *********";
            }
            print "   " . @properties[$i] . " \"" . $fields[$i++] . "\"" ;
            if ($i < @properties) {
                print " ;\n";
            }
        }
        print " ] .\n";
    }
}
