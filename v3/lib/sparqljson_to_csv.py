import json
import csv
import os
import logging
from datapackage_pipelines.wrapper import ingest, spew
from os import listdir
from os.path import isfile, join
from datapackage_pipelines.utilities.resources import streaming, PROP_STREAMING

def getLogger():
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  consoleHandler = logging.StreamHandler()
  logger.addHandler(consoleHandler)
  return logger

def convert_sparqljson_to_csv(filepath, outputpath):
    infile = open(filepath, "r")
    outfile = open (outputpath, "w")

    sparqljson = json.load(infile)
    writer = csv.writer(outfile)

    header = []
    for variable in sparqljson['head']['vars']:
      header.append(variable)
      header.append('type::' + variable)
      header.append('datatype::' + variable)
      header.append('xml:lang::' + variable)
    writer.writerow(header)

    for result in sparqljson['results']['bindings']:
      row = []
      for variable in sparqljson['head']['vars']:
        row.append(result[variable]['value'])
        row.append(result[variable]['type'])
        datatype = ''
        lang = ''
        if 'datatype' in result[variable]:
          datatype = result[variable]['datatype']
        row.append(datatype)
        if 'xml:lang' in result[variable]:
          lang = result[variable]['xml:lang']
        row.append(lang)
      writer.writerow(row)

    infile.close()
    outfile.close()

    json_file = filepath.replace(os.path.basename(filepath), os.path.basename(outputpath).replace('.csv', '.json'))
    os.rename(filepath, json_file)
    return json_file



logger = getLogger()
parameters, datapackage, res_iter = ingest()

if datapackage is None:
    datapackage = {}

datapackage.setdefault('resources', [])

for param in ['name', 'sparqljson-path', 'csv-output']:
    assert param in parameters, \
        "You must define {0} in your parameters".format(param)

sparqljson_resource_index = -1
sparqljson_resource = {}
for idx, resource in enumerate(datapackage['resources']):
    if 'name' in resource:
        if parameters['name'] == resource['name']:
            sparqljson_resource = resource
            sparqljson_resource_index = idx
            break
assert any(sparqljson_resource), "Could not find the sparqljson resource"

# find the first 'tmpfile in path directory'
sparqljson_file = ''
files = [f for f in listdir(parameters['sparqljson-path']) if isfile(join(parameters['sparqljson-path'], f))]
for file in files:
    if file.startswith('tmp'):
      sparqljson_file = parameters['sparqljson-path'] + file
      convert_sparqljson_to_csv(sparqljson_file, parameters['csv-output'])
      break

spew(datapackage, res_iter)
