#!/usr/bin/perl
# Convert http://unicode.org/emoji/charts/emoji-list.html to RDF Turtle.
# I was going to do this in Python but it would have been much more verbose.

use strict;

my $number = "";
my $code = "";
my $nameContent = "";

print "\@prefix e:    <http://unicode.org/emoji/charts/emoji-list.html#> .\n";
print "\@prefix lse:  <http://learningsparq.com/emoji/> .\n";
print "\@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n";

while(<>) {
    if (/<tr>/) {
        $code = "";
        $nameContent = "";
    }
    $number = $1 if (/'rchars'>(.+)<\/td>/);

    if (/'code'.*U\+(.+)<\/a>/) {
        $code = $1;
        print "e:$code\n";
        print  "   lse:code '$code' ;\n";
        print  "   lse:number $number ;\n";
    }

    if (/'chars'>(.+)<\/td>/) {
        print "   lse:char '$1' ;\n"
    }

    if (/'name'>(.+)<\/td>/) {
        $nameContent = $1;
        # The actual name (e.g. "GRINNING FACE") and list of annotations
        # both have class='name', so deal with each appropriately.
        if ($nameContent =~ /<a /) {
            # It's tempting to make these resource values, but many have chars
            # that don't work in URIs,
            # e.g. http://unicode.org/emoji/charts/emoji-annotations.html#+1
            while($nameContent =~ /<a href='emoji-annotations.html#(.+?)'/g ) {
                print "   lse:annotation  '$1' ;\n"
            } 
        }
        else {
            $nameContent =~ s/<br>/ /;
            print "   rdfs:label '$nameContent' ;\n";
        }
    }
    if  (/<\/tr>/ && $code ne "") {
        print ".\n\n";
    }
}
