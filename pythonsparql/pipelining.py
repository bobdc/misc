#!/usr/bin/env python

import urllib
import sys
from rdflib import Graph
import logging   # see https://docs.python.org/2/howto/logging.html 
from time import gmtime, strftime
import re

# global variables
wdRegEx = re.compile(r"\<http://www.wikidata.org/entity/(?P<localName>.+)\>")
g = Graph()       # graph where we'll store triples
endpoint = "https://query.wikidata.org/sparql"
maxValues = 40      # maximum number of VALUES entries per query 


def finishQuery(queryToSplit,newQuery,queryNumber,queryFooter):
    newQuery += queryFooter
    url = endpoint + "?" + urllib.urlencode({"query": newQuery})
    # Next line could use a try... except wrapper to report on timeouts, malformed queries, etc. 
    g.parse(url)
    logging.info('Triples in graph g after ' + queryToSplit + ' query number ' + str(queryNumber) + ': ' + str(len(g)))

    
def splitAndRunRemoteQuery(queryToSplit,valuesList,queryHeader,queryFooter):
    valuesInThisQuery = 0   # In the current query being built
    queryNumber = 1
    for row in valuesList:
        if valuesInThisQuery == 0:
            newQuery = queryHeader

        ID = '<%s>' % row
        result = wdRegEx.search(ID)    # Convert URI to qname if possible (shortens eventual URL)
        if result != None:
            ID = 'wd:' + result.group('localName')
        newQuery = newQuery + ID + '\n'

        valuesInThisQuery += 1
        if valuesInThisQuery > maxValues:
            # Finish up this query and execute it.
            finishQuery(queryToSplit,newQuery,queryNumber,queryFooter)
            valuesInThisQuery = 0
            queryNumber += 1
    # If there are some leftover entries
    if valuesInThisQuery > 0:    
        finishQuery(queryToSplit,newQuery,queryNumber,queryFooter)
    
def main(cityLocalID):
    cityQname = "wd:" + cityLocalID

####### Start of SPARQL query variables ######

    queryRetrieveGeoPoints = """
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
PREFIX p: <http://www.wikidata.org/prop/> 
PREFIX psv: <http://www.wikidata.org/prop/statement/value/> 
PREFIX schema: <http://schema.org/> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 

CONSTRUCT {
   ?s ?p ?o .
   ?s wgs84:lat ?lat . 
   ?s wgs84:long ?long . 
}

WHERE {

   BIND(CITY-QNAME AS ?geoEntityWikidataID) 

   ?s wdt:P131+ ?geoEntityWikidataID .  
   ?s p:P625 ?statement . # coordinate-location statement
   ?statement psv:P625 ?coordinate_node .
   ?coordinate_node wikibase:geoLatitude ?lat .
   ?coordinate_node wikibase:geoLongitude ?long .
}
"""

    queryListSubjects ="""
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT ?s WHERE {
  ?s wgs84:lat ?lat
}  
"""

    entityDataQueryHeader = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/> 
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 

CONSTRUCT
{ ?s ?p ?o. 
  ?s ?p1 ?o1 . 
  ?s wgs84:lat ?lat . 
  ?s wgs84:long ?long .
  ?p rdfs:label ?pname .
  ?s wdt:P31 ?class .   
}
WHERE {
  VALUES ?s {
"""

    # Notes pulled out of entityDataQueryFooter below: wdt:P131 means
    # 'located in the administrative territorial entity' .
    # p:P625 is the coordinate-location statement.
    # ?directClaimP part is to reduce the indirection used by Wikidata
    # triples. Based on Tommy Potter query at
    # http://www.snee.com/bobdc.blog/2017/04/the-wikidata-data-model-and-yo.html.
    # VALUES after ?p1 clause is actually faster than just
    # having specific triple patterns for those 2 p1 values.
    # 'en' part is if only English names desired. For  English + something else, follow this pattern: 
    # FILTER (isURI(?o1) || lang(?o1) = 'en' || lang(?o1) = 'de')
    # P31: Class membership. Pull this and higher level classes out in later query.
    
    entityDataQueryFooter = """
}
  ?s wdt:P131+ ?geoEntityWikidataID .  
      ?s p:P625 ?statement . 
  ?statement psv:P625 ?coordinate_node .
  ?coordinate_node wikibase:geoLatitude ?lat .
  ?coordinate_node wikibase:geoLongitude ?long .

  ?s ?directClaimP ?o .
  ?p wikibase:directClaim ?directClaimP .
  ?p rdfs:label ?pname .

  ?s ?p1 ?o1 .
  VALUES ?p1 {
    schema:description
    rdfs:label        
    skos:altLabel
  }

  ?s wdt:P31 ?class .
  
  FILTER (isURI(?o1) || lang(?o1) = 'en' )

  FILTER(lang(?pname) = 'en')
}
"""

    listClassesQuery = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/> 

SELECT DISTINCT ?class WHERE {
  ?instance wdt:P31 ?class .
}
"""
    queryGetClassesHeader = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
CONSTRUCT {
  ?class rdfs:subClassOf ?superclass ; 
         rdfs:label ?className .
  ?superclass rdfs:label ?superclassName . 
  }
WHERE {
?instance wdt:P31 ?class .
  VALUES ?instance {
"""

    queryGetClassesFooter = """
  }
?class rdfs:label ?className .
  ?class wdt:P279+ ?superclass . 
  ?superclass rdfs:label ?superclassName . 
  FILTER ( lang(?className) = 'en' )
  FILTER ( lang(?superclassName) = 'en' )
}
"""

    queryObjectsThatNeedLabel = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?o WHERE {
  ?s ?p ?o .
  MINUS { ?o rdfs:label ?label }
  FILTER(strstarts(str(?o),'http://www.wikidata.org/entity/'))
}
"""

    queryGetObjectLabelsHeader = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

CONSTRUCT { ?s rdfs:label ?o }
WHERE {
VALUES ?s {
"""

# FILTER below is for English only; for English + something else follow this pattern:
  # FILTER (lang(?o) = 'en' || lang(?o) = 'de')

    queryGetObjectLabelsFooter = """
}
  ?s rdfs:label ?o . 
  FILTER (lang(?o) = 'en' )
}
"""

########## End of SPARQL queries #############

    # 1. Get the qnames for the geotagged entities within the city & store in graph g. 

    queryRetrieveGeoPoints = queryRetrieveGeoPoints.replace("CITY-QNAME",cityQname)
    url = endpoint + "?" + urllib.urlencode({"query": queryRetrieveGeoPoints})
    g.parse(url)
    logging.info('Triples in graph g after queryRetrieveGeoPoints: ' + str(len(g)))

    # 2. Take the subjects in graph g and create queries with a VALUES clause 
    #    of up to maxValues of the subjects. 

    subjectQueryResults = g.query(queryListSubjects)
    splitAndRunRemoteQuery("querySubjectData",subjectQueryResults,
                           entityDataQueryHeader,entityDataQueryFooter)

    # 3. See what classes are used and get their names and those of their superclasses.
    classList = g.query(listClassesQuery)
    splitAndRunRemoteQuery("queryGetClassInfo",classList,
                           queryGetClassesHeader,queryGetClassesFooter)

    # 4. See what objects need labels and get them.
    objectsThatNeedLabel = g.query(queryObjectsThatNeedLabel)
    splitAndRunRemoteQuery("queryObjectsThatNeedLabel",objectsThatNeedLabel,
                           queryGetObjectLabelsHeader,queryGetObjectLabelsFooter)

    print(g.serialize(format = "n3"))   # (Actually Turtle, which is what we want, not n3.)
    
if __name__ == "__main__":
    if  len(sys.argv) != 2:
        print "Enter a city's Wikidata URI local name (e.g. Q123766)"
        print "as a command line argument to retrieve data about that city."
    else:
        logging.basicConfig(filename='pipelining.log',level=logging.DEBUG)
        cityLocalID = sys.argv[1]
        logging.info(strftime("Starting at %Y-%m-%dT%H:%M:%S with ID ", gmtime()) + cityLocalID)
        main(cityLocalID)
        logging.info(strftime("Finishing at %Y-%m-%dT%H:%M:%S", gmtime()))


