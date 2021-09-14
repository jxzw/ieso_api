# ieso_xml_parser

This is a work in progress data pipeline for the IESO's XML structured API.

This script pulls data about the energy output of every electricity generator in the Province of Ontario, parses it, and saves it in a beautiful and storage efficient JSON. 

Though the IESO publishes generator data hourly, their API only returns 3 months worth of data. This script is for the purpose of continuously recording output data, that will eventually be turned into a web app. 

