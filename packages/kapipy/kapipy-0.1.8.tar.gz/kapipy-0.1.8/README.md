# kapipy
A python client for accessing and querying datasets from geospatial open data portals such as LINZ, Stats NZ and LRIS.

## Overview  
kapipy is a Python package that provides a python interface to the Koordinates geospatial content management system. It allows users to connect a data portal, retrieve metadata, and query vector layers and tables. 

Documentation available at [Github Pages documentation website](https://phaakma.github.io/kapipy/)  

## Disclaimer  
This is a hobby project and the modules are provided as-is on a best-effort basis and you assume all risk for using it.  
The author has no affiliation with either Koordinates nor LINZ, Stats NZ or LRIS. As such, the underlying API's and services may change at any time without warning and break these modules. The author is not privvy to any inside knowledge or documentation beyond what is available online or by inspecting the payloads returned by the services.  

This project does not cover the full spectrum of the Koordinates API and probably never will. It focuses currently on basic workflows such as connecting using an api key, getting references to datasets and downloading them.  

The author is happy to take feedback and consider suggestions and code contributions as time allows. Preferred method for feedback is via the Github repository issues page.    

## Installation  

```bash
pip install kapipy
```

## Usage  

* Import kapipy.  
* Create a GIS object, passing in an api key.  
* Get a reference to an item using {gis}.content.get({layer_id})
* Perform actions on the item.  

Basic example:  
```python
from kapipy.gis import GIS
linz = GIS(name="linz", api_key="my-api-key")
rail_station_layer_id = "50318"
itm = linz.content.get(rail_station_layer_id)
data = itm.query()
data.head()
```
