#!/usr/bin/env perl

# Read the TSV result of the sortBySimilarity.rq query and create HTML
# out of it: list recipes and the 3 most similar recipes to each.

# Input lines look like this:

# 0.9777809	<https://en.wikibooks.org/wiki/Cookbook:B%C3%A1nh_M%C3%AC>	"Bánh mì: colorful Saigon sandwich[edit]"	<https://en.wikibooks.org/wiki/Cookbook:Coq_au_Vin>	"Cookbook:Coq au Vin"

use strict;
my @line = [];
my $score = 0;
my $doc1URL = ""; 
my $doc1title = ""; 
my $doc2URL = ""; 
my $doc2title = ""; 
my $score  = ""; 

print "<html><style type=\"text/css\">";
print " *   { font-family: arial,helvetica;  }";
print "body    {margin: .25in .5in .25in .5in}";
print "p      { font-family: arial,helvetica; }";
print "a      {text-decoration: none }";
print "</style></body>";

my $prevDoc1URL = "dummy";
my $relatedRecipesListed = 0;

while(<>) {
    chop($_);
    s/\[edit\]//;
    s/<//g;   # in URLs
    s/>//g; 
    @line = split(/\t/,$_);
    $score = $line[0];
    $doc1URL = $line[1];
    $doc1title = $line[2];
    $doc2URL = $line[3];
    $doc2title = $line[4];
    $score =~ s/\"\^.*//;
    $score =~ s/\"//;
    $doc1title =~ s/Cookbook://;
    $doc1title =~ s/^\"//;
    $doc1title =~ s/"$//;
    $doc2title =~ s/"Cookbook://;
    $doc2title =~ s/"$//;
    if ($doc1title ne "\?doc1title") {
        if (($prevDoc1URL ne $doc1URL) || ($prevDoc1URL eq "dummy")) {
            $relatedRecipesListed = 0;
            print '<h2><a href="' . $doc1URL . '">' . $doc1title . "</h2>\n";
        }
        if ($relatedRecipesListed < 3) {
            print '<p><a href="' . $doc2URL . '">' . $doc2title . "</a></p>\n";
            $relatedRecipesListed++;
        }
        $prevDoc1URL = $doc1URL;
    }
}

print "</body></html>"
