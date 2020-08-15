package main

import (
	"flag"
	"fmt"
	"github.com/knakk/rdf"
	"html/template" // text/template seems to work the same but keeps XML comments
	"io"
	"log"
	"os"
	"unicode/utf8"
)

var usage = `rdf2modsxml
-------
Read RDF in any serialization and convert to MODS XML according to 
mappings specified at https://t.co/L20MBi0BBs. 

Based on https://github.com/knakk/rdf2rdf/blob/master/rdf2rdf.go. 
(This is my first non-trivial go program.)

Usage: 
	rdf2modsxml -in=input.ttl

Options:
	-h --help      Show this message.
	-in            Input file.


  Format    | File extension
  ----------|-------------------
  N-Triples | .nt
  RDF/XML   | .rdf .rdfxml .xml
  Turtle    | .ttl

`

// docsMetadata holds metadata for multiple documents. Document ID
// (subject of triples about the document) is the key. The value
// associated with the key is another map that has predicate values as
// keys and an arrays as values so that a single subject-predicate
// pair can have multiple values (.e.g. multiple topic values for a
// given document).
var docsMetadata = map[string]map[string][]string{}

// knakk/rdf2rdf can identify whether an Object is a literal or a URI
// or a bnode so future steps could build on that. 

func main() {

	log.SetFlags(0)
	log.SetPrefix("ERROR: ")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, usage)
	}
	input := flag.String("in", "", "Input file")
	flag.Parse()

	if *input == "" {
		fmt.Println("Usage:")
		flag.PrintDefaults()
		os.Exit(1)
	}

	inFile, err := os.Open(*input)
	if err != nil {
		log.Fatal(err)
	}
	defer inFile.Close()

	var inFileRdr io.Reader
	inFileRdr = inFile

	inExt := fileExtension(*input)
	var inFormat, outFormat rdf.Format

	switch inExt {   // Can read multiple serializations!
	case "nt":
		inFormat = rdf.NTriples
	case "ttl":
		inFormat = rdf.Turtle
	case "xml", "rdf", "rdfxml":
		inFormat = rdf.RDFXML
	case "":
		log.Fatal("Unknown file format. No file extension on input file.")
	default:
		log.Fatalf("Unsupported file exension on input file: %s", inFile.Name())
	}
	tr := readTriples(inFileRdr, inFormat, outFormat)
	for i := 0; i < len(tr); i++ {
		subject := tr[i].Subj.String()
		predicate := tr[i].Pred.String()
		object := tr[i].Obj.String()

		// If that subject has no entry, make one.
		if _, found := docsMetadata[subject]; !(found) {
			docsMetadata[subject] = map[string][]string{}
		}

		// If the subject already has any values for that predicate
		if _, found := docsMetadata[subject][predicate]; found {
			// Append the new value to the array stored with the predicate
			docsMetadata[subject][predicate] = append(docsMetadata[subject][predicate], object)
		} else {
			// Create new array to store object values for that subject-predicate pair
			docsMetadata[subject][predicate] = []string{object}
		}

	}

	// Read the template and output the data with it.
	modsTemplate, err := template.ParseFiles("modsTemplate.xml")
	err = modsTemplate.Execute(os.Stdout, docsMetadata)
	if err != nil {
		// whatever; I got an error if I didn't do something with err
	}
}

func readTriples(inFile io.Reader, inFormat, outFormat rdf.Format) []rdf.Triple {

	dec := rdf.NewTripleDecoder(inFile, inFormat)

	tr, err := dec.DecodeAll()
	if err != nil {
		log.Fatal(err)
	}
	return tr
}

func fileExtension(s string) string {
	i := len(s)
	for i > 0 {
		r, w := utf8.DecodeLastRuneInString(s[0:i])
		if r == '.' {
			return s[i:len(s)]
		}
		i -= w
	}
	return "not found"
}
