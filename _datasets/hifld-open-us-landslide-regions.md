---
schema: data_rescue_project 
title: HIFLD Open US Landslide Regions
organization: Homeland Infrastructure Foundation-Level Data (HIFLD)
agency: Department of Homeland Security
websites: hifld-geoplatform.hub.arcgis.com/
data_source: hifld-geoplatform.hub.arcgis.com
description: 
last_modified: 2026-01-21
metadata_available: No
metadata_url: 
category:
  - Infrastructure 
resources:
  - id: 1990
    url: https://www.datalumos.org/datalumos/project/240751/version/V1/view
    format: 
    status: Finished
    size: 1.3532
    download_date: 2025-08-26
    maintainer: DRP, DL
    notes: Landslides are damaging and deadly, and they occur in every U.S. state. However, our current ability to understand landslide hazards at the national scale is limited, in part because spatial data on landslide occurrence across the U.S. varies greatly in quality, accessibility, and extent. Landslide inventories are typically collected and maintained by different agencies and institutions, usually within specific jurisdictional boundaries, and often with varied objectives and information attributes or even in disparate formats. The purpose of this data release is to provide an openly accessible, centralized map of existing information about landslide occurrence across the entire U.S. This data release is an update of previous versions 1 (Jones and others, 2019) and 2 (Belair and others, 2022). Changes relative to version 2 are summarized in us_ls_v3_changes.txt. It provides an integrated database of the landslides from these inventories (refer to US_Landslide_v3_gpkg) with a selection of uniform attributes, including links to the original digital inventory files (whenever available) (“Inv_URL”). The data release includes digital inventories created by both USGS and non-USGS authors. The original inventory is denoted by an abbreviation in the “Inventory” attribute. The full citation for each abbreviation can be found in us_ls_v3_references.csv. The date of the landslide event is included as a minimum and maximum (“Date_Min” and “Date_Max”) to accommodate events that happen within a range of dates. The date value is inherently difficult to interpret or discern due to the nature of landsliding, where some landslides move for long periods of time or move intermittently, and some areas can exhibit multiple landslide events. To preserve the constituent inventories as much as possible, we include all entries even if they are not considered landslides, such as “gullies” or “avalanche chutes.” We include a landslide type attribute when that information is available (“LS_Type”). The landslide classification system used in the original inventories is not always known or stated in the metadata, but many mapping entities use the schema from Cruden and Varnes (1996) or the updated schema from Hungr and others (2014). Given the wide range of landslide information sources in this data compilation, we provide an attribute to assess the relative confidence in the characterization of the location and extent of each landslide (entry) (“Confidence”). The confidence level reflects the resolution and quality of input data, as well as the method used for identification and mapping. This confidence does not reflect a formal accuracy assessment of field attributes. Relative to the previous data releases (version 1 and 2), this update (v3) includes more inventories, updated confidence rules, a new landslide type attribute, a new unique identifier (“USGS_ID”), new machine-readable date fields, and an ancillary database containing all fields from the original inventories (refer to US_Landslide_v3_ancillary). Please contact gs-haz_landslides_inventory@usgs.gov for more information on how to contribute additional inventories to this community effort. When possible, please cite the constituent inventories as well as this data release.This data release includes (1) a landslide point file and polygon file in multiple forms (US_Landslide_v3_gpkg, US_Landslide_v3_shp, US_Landslide_v3_csv), (2) an ancillary database with original fields (US_Landslide_v3_ancillary), (3) a spreadsheet that summarizes the confidence rules, their justification, and any extra analyses (us_ls_v3_analyses.csv), (4) a summary file of the changes made between version 2 and version 3 (us_ls_v3_changes.txt), (5) a file containing the references of the constituent inventories (us_ls_v3_references.csv), (6) and a readme (README.txt).Disclaimer Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government.
---
