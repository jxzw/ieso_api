from typing import Generator
import requests
import json
from bs4 import BeautifulSoup as bs

supply_request = requests.get('http://reports.ieso.ca/public/GenOutputCapability/PUB_GenOutputCapability_20210824.xml')

file = open("output_raw.xml", 'w')
file.write(supply_request.text)
file.close()

# finds the second '>' character to remove excess header information
xml_text = supply_request.text
c = 0
i, j = '', ''
while j != '>':
        while i != '>':
                i = xml_text[c]
                c += 1
        j = xml_text[c]
        c += 1
xml_text = xml_text[c:]
file = open("output.xml", 'w')
file.write(xml_text)
file.close()

with open("output.xml", "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
file.close()

class Generator:
        def __init__(self, name, fueltype, outputs, capabilities, capacity):
                self.name = name
                self.fueltype = fueltype
                self.outputs = outputs
                self.capabilities = capabilities
                self.capacity = capacity

list_generators = []
outputs_dict = {}
capabilities_dict = {}
capacities_dict = {}

generators = bs_content.find_all("generator")
for generator in generators:
        fueltype = generator.find('fueltype').contents[0]
        name = generator.find('generatorname').contents[0]
        fueltype = generator.find('fueltype').contents[0]
        outputs = generator.find("outputs")
        output = outputs.find_all("output")
        for h in output:

                hour = h.find('hour').contents[0]
                timehour = int(hour)
                if h.find('energymw') != None:
                        output_energymw = h.find('energymw').contents[0]
                        outputs_dict[hour] = output_energymw
                else:
                        outputs_dict[hour] = 0

        capabilities = generator.find("capabilities")
        capability = capabilities.find_all("capability")
        for x in capability:
                hour = x.find('hour').contents[0]
                if x.find('energymw') != None: 
                        capability_energymw = x.find('energymw').contents[0]
                        capabilities_dict[hour] = capability_energymw 
                

        capacities = generator.find("capacities")
        availcapacity = capacities.find_all("availcapacity")
        for c in availcapacity:
                hour = c.find('hour').contents[0]
                if c.find('energymw') != None: 
                        capacity_energymw = c.find('energymw').contents[0]
                        capacities_dict[hour] = capacity_energymw
                
        generatorEntry = Generator(name, fueltype, outputs_dict, capabilities_dict, capacities_dict)
        list_generators.append(generatorEntry)

        outputs_dict = {}
        capabilities_dict = {}
        capacities = {}


keydict = {}
c = 0
i = 0
for i in list_generators:
        keydict[c] = { 'name' : i.name, 'fueltype': i.fueltype, 'outputs': i.outputs, 'capabilities': i.capabilities, 'capacities': i.capacity}
        c += 1
x = 0
newdict = {}

json_object = json.dumps(keydict, indent = 4) 
file = open("output.json", 'w')
file.write(json_object)
file.close()


for i in keydict:
        if keydict[i]['fueltype'] == "SOLAR":
                newdict[x] = keydict[i]
                x += 1

json_object = json.dumps(newdict, indent = 4) 
file = open("solar.json", 'w')
file.write(json_object)
file.close()

