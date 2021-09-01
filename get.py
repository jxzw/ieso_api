from typing import Generator
import xml.etree.ElementTree as ET
import requests
import lxml
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
xml_text = xml_text[157:]
file = open("output.xml", 'w')
file.write(xml_text)
file.close()

with open("output.xml", "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
file.close()

generators = bs_content.find_all("generator")
name = generators[0].find("generatorname")
fueltype = generators[0].find("fueltype")
outputs = generators[0].find("outputs")
output = outputs.find_all("output")
hour = output[0].find('hour')
energymw = output[0].find('energymw')
output_list = []

class Generator:
        def __init__(self, name, fueltype, outputs):
                self.name = name
                self.fueltype = fueltype
                self.outputs = outputs
                self.info = {'name' : self.name, 'fueltype': self.fueltype, 'outputs': self.outputs}

list_generators = []
outputs_dict = {}
for generator in generators:
        if generator.find('fueltype').contents[0] == "NUCLEAR":
                name = generator.find('generatorname').contents[0]
                fueltype = generator.find('fueltype').contents[0]
                outputs = generator.find("outputs")
                output = outputs.find_all("output")
                key = 0
                for h in output:
                        hour = h.find('hour').contents[0]
                        energymw = h.find('energymw').contents[0]
                        outputs_dict[hour] = energymw 
                list_generators.append(Generator(name, fueltype, outputs_dict))
                outputs_dict = {}


print(list_generators[0].info)

            
