---
schema: data_rescue_project 
title: HIFLD OPEN Mines and Mineral Resources
organization: Homeland Infrastructure Foundation-Level Data (HIFLD)
agency: Department of Homeland Security
websites: hifld-geoplatform.hub.arcgis.com/
data_source: https://hifld-geoplatform.hub.arcgis.com/
description: 
last_modified: 2025-11-09
metadata_available: No
metadata_url: 
category:
  - Infrastructure 
resources:
  - id: 1588
    url: https://www.datalumos.org/datalumos/project/239598
    format: 
    status: Finished
    size: 
    download_date: 2025-08-26
    maintainer: DRP, DL
    notes: The mine and the manufacturing plant need not be located in close proximity to each other to be "closely associated". Also, it is possible for more than one mine to be associated with a particular manufacturing plant, and for more than one manufacturing plant to be associated with a particular mine. A mine associated with a manufacturing plant represents an potential additional point of vulnerability to the manufacturing plant, likewise, the manufacturing plant represents a potential additional point of vulnerability to the mine. Any relevant transportation links between the two represents a third potential vulnerability. The links between the mines and the manufacturing plants are contained in the Mines_linked_to_ManufacturingID_table.dbf table. The [MINEID] field corresponds to the [SRCLNKID] attribute in this dataset. The [MNFID] corresponds to the [SRCLNKID] in the manufacturing dataset. Mines are typically large facilities. To enable a first responder or law enforcement team to easily drive to the mine the point representing the mine has been placed at the place where the main "haul road" meets the nearest public road. This location may be a considerable distance from the mine pit or shaft, but from this point on the ground it should be obvious how to drive to the mine itself. Text fields in this dataset have been set to all upper case to facilitate consistent database engine search results. All diacritics (e.g. the German umlaut or the Spanish tilde) have been replaced with their closest equivalent English character to facilitate use with database systems that may not support diacritics. The currentness of this dataset is indicated by the [CONTDATE] attribute. Based upon this attribute the oldest record dates from 06/06/2006 and the newest record dates from 10/12/2006.The data is legacy and not expected to be updated. It is being provided as the best available until Mineral Resources identifies an alternative data source.
---
