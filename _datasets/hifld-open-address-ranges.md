---
schema: data_rescue_project 
title: HIFLD Open Address Ranges
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
  - id: 1785
    url: https://www.datalumos.org/datalumos/project/240886/version/V1/view
    format: 
    status: Finished
    size: 1.1787
    download_date: 2025-08-26
    maintainer: DRP, DL
    notes: Address ranges describe a label given to a unique collection of addresses that fall along a road or path. Address ranges provide a way of locating homes and businesses based on their street addresses when no other location information is available.Using a house number, street name, street side and ZIP code, address ranges can locate the address to the geographic area associated to that side of the street. Once geocoded, the U.S. Census Bureau can assign the address to a field assignment area or tabulate the data for that address. In addition, academics, researchers, professionals and government agencies outside of the Census Bureau use MAF/TIGER address ranges to transform tabular addresses into geographical datasets for decision-making and analytical purposes.Address ranges must be unique to geocode addresses to the correct location and avoid geocoding conflicts. Multiple elements in MAF/TIGER are required to make an address range unique including street names, address house numbers and street feature geometries, such as street centerlines. The address range data model is designed to maximize geocoding matches with their correct geographic areas in MAF/TIGER by allowing an unlimited number of address range-to-street feature relationships.The Census Bureau’s Geography Division devises numerous operations and processes to build and maintain high quality address ranges so thatAddress ranges accurately describe the location of addresses on the ground.Address All possible city-style addresses are geocoded.Address ranges can handle all known address and street name variations.Address ranges conform with current U.S. Postal Service ZIP codes.Address ranges are reliable and free from conflicts.Automated software continually updates existing address ranges, builds new address ranges and corrects errors. An automated operation links address location points and tabular address information to street feature edges with matching street names in the same block to build and modify address ranges.Many business rules and legal value checks ensure quality address range data in MAF/TIGER. For example, business rules prevent adding or modifying address ranges that overlap another house number range with the same street name and ZIP code. Legal value checks verify that address ranges include mandatory attribute information, valid data types and valid character values.Some of the TIGER/Line products for the public include address ranges and give the public the ability to geocode addresses to MAF/TIGER address ranges for the user’s own purpose. The address range files are available for the nation, Puerto Rico and the U.S. Island Areas at the county level. TIGER/Line files require geographic information system (GIS) software to use.The Census Bureau Geocoder Service is a web service provided to the public. The service accepts up to 1,000 input addresses and, based on Census address ranges, returns the interpolated geocoded location and census geographies. Users can access the service a web interface or a representational state transfer (REST) application program interface (API) web service. See the Census Geocoder for more information on this process. Directions on how to use the Census Geocoder available Geocoding Services Web Application Programming Interface (API)Download https://www2.census.gov/geo/tiger/TGRGDB24/tlgdb_2024_a_us_addr.gdb.zip
---
