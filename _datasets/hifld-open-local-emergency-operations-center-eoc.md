---
schema: data_rescue_project 
title: HIFLD OPEN Local Emergency Operations Center (EOC)
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
  - id: 1598
    url: https://www.datalumos.org/datalumos/project/239489
    format: 
    status: Finished
    size: 
    download_date: 2025-08-26
    maintainer: DRP, DL
    notes: HSIP Local Emergency Operations Centers in the United States "The physical location at which the coordination of information and resources to support domestic incident management activities normally takes place. An Emergency Operations Center may be a temporary facility or may be located in a more central or permanently established facility, perhaps at a higher level of organization within a jurisdiction. Emergency Operations Centers may be organized by major functional disciplines (e.g., fire, law enforcement, and medical services), by jurisdiction (e.g., Federal, State, regional, county, city, tribal), or some combination thereof." (Excerpted from the National Incident Management System) The Government Provided Information (GPI) source for this layer contains State and Federal Emergency Operations Centers in addition to local Emergency Operations Centers. This dataset contains Federal and local Emergency Operation Centers and only those federal centers that are of a local nature such as military installations. In cases where an Emergency Operations Center has a mobile unit, TechniGraphics captured the location of the mobile unit as a separate record. This record represents where the mobile unit is stored and if the location could not be verified, a point was placed in the approximate center of the Emergency Operations Centers service area. TechniGraphics tried to verify whether or not each Emergency Operations Center has a generator on-site and whether or not the Emergency Operations Center is located in a basement. This information is indicated by the values in the [GENERATOR] and [BASEMENT] fields respectively. In cases where more than one record existed for a geographical area (e.g., county, city), TechniGraphics verified whether or not one of the records represented an alternate location. This was indicated by appending "-ALTERNATE" to the value in the [NAME] field. Some Emergency Operations Centers are located at private residences. The [TYPE] field was manually evaluated during the delivery process to compare the records in which the [NAME] field contained "-ALTERNATE". In cases where these values contradicted information that was verified by TechniGraphics (e.g. [NAME] contained "- ALTERNATE" and [TYPE] = "PRIMARY"), the value in the [TYPE] field was changed to match the type indicated by the [NAME] of the verified record. TechniGraphics did not change values in this field if the type was not verified. Records with "-Department of Defense (DOD)" appended to the end of the [NAME] value are located on a military base, as defined by the Defense Installation Spatial Data Infrastructure (DISDI) military installations and military range boundaries. "#" and "*" characters were automatically removed from standard HSIP fields that TechniGraphics populated. Double spaces were replaced by single spaces in these same fields. At the request of NGA, text fields in this dataset have been set to all upper case to facilitate consistent database engine search results. At the request of NGA, all diacritics (e.g., the German umlaut or the Spanish tilde) have been replaced with their closest equivalent English character to facilitate use with database systems that may not support diacritics. The currentness of this dataset is indicated by the [CONTDATE] field. Based upon this attribute, the oldest record dates from 08/28/2009 and the newest record dates from 11/18/2009.
---
