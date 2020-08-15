# RDF to MODS XML

The blog entry [Generating MODS XML from RDF with Go templates](http://www.bobdc.com/blog/rdf2modsxml/) describes more about the files in this directory. 

**rdf2modsxml.go** The Go source for the program that reads the RDF and the template and then outputs the MODS XML. 

**modsTemplate.xml** the template. 

**modsjournals2.ttl** RDF of metadata about two journal articles, based on [this sample journal metadata](https://www.loc.gov/standards/mods/userguide/examples.html#journal_article) from the MODS website.

**modsjournals2.xml*** XML created by the Go program with the template and RDF files above using the command line described in the blog entry (the command line that uses awk to remove the blank lines).

To check that the result is valid MODS XML, you'll want the  [MODS XML Schema](http://www.loc.gov/standards/mods/v3/mods-3-3.xsd), if anyone can truly want an XSD schema. The blog entry describes how to use xmllint to check the generated XML against the schema. 
