# ieso_api

This is a work in progress serializer for ieso's api

This script pulls data about the energy output of every electricity generator in the Province of Ontario and serializes to JSON. 

Though the IESO publishes generator data hourly, their API only returns 3 months worth of data. This script is for the purpose of continuously recording output data, that will eventually be turned into a web app. 

