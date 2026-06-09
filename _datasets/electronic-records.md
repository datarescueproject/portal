---
schema: data_rescue_project 
title: Electronic Records
organization: National Archives and Records Administration
agency: National Archives and Records Administration
websites: archives.gov
data_source: https://s3.amazonaws.com/NARAprodstorage/lz/electronic-records
description: 
last_modified: 2026-04-22
dataset_source_status: 
metadata_available: No
metadata_url: 
category:
  - Arts & Culture 
  - Science & Research 
resources:
  - id: 3019
    url: https://sciop.net/datasets/nara-electronic-records-s3-mirror
    format: PDF, TXT, HTML, dat
    status: Finished
    size: 8800.0
    download_date: 2026-03-15
    maintainer: SRC
    notes: Contains all records within the specified AWS bucket folder, including the UAPS records found at https://s3.amazonaws.com/NARAprodstorage/lz/bulk-downloads/uaps/zips, for funsies.All records have been packed with the sciop-cli pack tool, into tar.zst files. These can be extracted manually with the usual Windows/Mac file exploration programs, or can be unpacked en-masse with the sciop-cli unpack tool (https://codeberg.org/Safeguarding/sciop-cli)
---
