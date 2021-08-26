# Create a custom processor and see if I can access data from SPARQL endpoint

1. Create a custom processor local to the pipeline in a directory `.lib/`
2. Custom processor reads JSON data in SPARQL JSON format.

Pipeline will:

1. Query a SPARQL endpoint 
2. Dump that resulting SPARQL query of JSON data as CSV to current directory (`out-path: .`) [not that useful, but wanted to see if it was possible]
3. Query a SPARQL endpoint 
4. Dump that resulting SPARQL query of JSON as JSON (`format: json`) to a directory called 'r2r-hot-cruise-dois' [wanted to see if I could save non-local, external data in JSON format]
5. Load the resulting datapackage.json from Step 4 at `./r2r-hot-cruise-dois` into the pipeline (so we can access the json file from Step 4
6. Run custom processor that converts the SPARQL JSON results into CSV using my own code.
