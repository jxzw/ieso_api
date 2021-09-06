from typing import Generator
import requests
import json
from bs4 import BeautifulSoup as bs



class Generator:
        def __init__(self, name, fueltype, date, outputs, capabilities, capacity):
                self.name = name
                self.fueltype = fueltype
                self.outputs = outputs
                self.date = date
                self.capabilities = capabilities
                self.capacity = capacity
                self.info = { 'name' : self.name, 'fueltype': self.fueltype, "date": self.date, 'outputs': self.outputs, 'capabilities': self.capabilities, 'capacities': self.capacity}

class XML:
        def __init__(self, date=None):
                if date != None: self.date = date
                else:
                        self.date = None

            
        # date  format as string 'YYYYMMDD'
        def GetIesoXML(self):
                url_date = ""
                if self.date != None:
                        url_date = "_" + self.date

                supply_request = requests.get(f'http://reports.ieso.ca/public/GenOutputCapability/PUB_GenOutputCapability{url_date}.xml')

                if self.date == None:
                        self.date = bs(supply_request.text, "lxml").find('date').contents[0].replace('-','')

                url_date = "_" + self.date

                file = open(f"output_raw{url_date}.xml", 'w')
                file2 = open(f"output_raw.xml", 'w')
                file.write(supply_request.text)
                file2.write(supply_request.text)
                file.close()
                file2.close()

                # finds the second '>' character to remove excess header information
                # the ieso includes header information, which is then omitted
                c = 0
                i, j = '', ''
                while j != '>':
                        while i != '>':
                                i = supply_request.text[c]
                                c += 1
                        j = supply_request.text[c]
                        c += 1
                output = supply_request.text[c:]

                #saves headerless xml 
                file = open(f"output{url_date}.xml", 'w')
                file2 = open(f"output.xml", 'w')
                file.write(output)
                file2.write(output)
                file.close()
                file2.close()

                self.response = output

                return self.response


        def parse(self):
                #reads the headerless xml
                url_date = "_" + self.date
                with open(f"output{url_date}.xml", "r") as file:
                        content = file.readlines()
                        content = "".join(content)
                        bs_content = bs(content, "lxml")
                        file.close()

                list_generators = []
                outputs_dict, capabilities_dict, capacities_dict = {}, {}, {}

                date = str(bs_content.find('date').contents[0]).replace('-','')

                generators = bs_content.find_all("generator")

                for generator in generators:
                        fueltype = generator.find('fueltype').contents[0]
                        name = generator.find('generatorname').contents[0]
                        fueltype = generator.find('fueltype').contents[0]
                        outputs = generator.find("outputs")
                        output = outputs.find_all("output")

                        for h in output:
                                hour = h.find('hour').contents[0]
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
                                else:
                                        capabilities_dict[hour] = 0        

                        capacities = generator.find("capacities")
                        availcapacity = capacities.find_all("availcapacity")
                        for c in availcapacity:
                                hour = c.find('hour').contents[0]
                                if c.find('energymw') != None: 
                                        capacity_energymw = c.find('energymw').contents[0]
                                        capacities_dict[hour] = capacity_energymw
                                else:
                                        capacities_dict[hour] = 0
                                
                        generatorEntry = Generator(name, fueltype, date, outputs_dict, capabilities_dict, capacities_dict)
                        list_generators.append(generatorEntry)
                        self.list_generators = list_generators

                return list_generators


        def DumpToJson(self):
                url_date = "_" + self.date
                keydict = {}
                c = 0
                i = 0
                for i in self.list_generators:
                        keydict[c] = i.info
                        c += 1

                json_object = json.dumps(keydict, indent = 4) 
                file = open(f"output{url_date}.json", 'w')
                file2 = open(f"output.json", 'w')
                file.write(json_object)
                file2.write(json_object)
                file.close()
                file2.close()
                fueltypes = ['NUCLEAR', 'GAS', 'BIOFUEL', 'HYDRO', 'SOLAR', 'WIND']
                for fuel in fueltypes:
                        x = 0
                        dumpdict = {}
                        for i in keydict:
                                if keydict[i]['fueltype'] == fuel:
                                        dumpdict[x] = keydict[i]
                                        x += 1
                        json_object = json.dumps(dumpdict, indent = 4)                         
                        file = open(f"fuel\\/{fuel}{url_date}.json", 'w')
                        file.write(json_object)
                        file.close()


# main

now = XML()
now.GetIesoXML()
now.parse()
now.DumpToJson()