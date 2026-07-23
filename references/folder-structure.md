# Managed folder structure

```text
ArtLibrary/
  00_Inbox/
  01_Archive_Originals/{year}/{run_id}/
  02_Catalog/
    catalog.jsonl
    catalog.csv
    duplicate-groups.json
    approval-log.jsonl
  03_Works/{year}/{work_id}/
    01_Master/
    02_Alternates/
    03_Details/
    04_Previews/
    05_Print_Files/
    06_Listing_Assets/
    metadata.json
    README.md
  04_Review_Required/
    Possible_Duplicates/
    Missing_Metadata/
    Low_Resolution/
    Rights_or_Privacy_Check/
    Uncertain_Grouping/
  05_Publish_Queue/{platform}/Draft/
  05_Publish_Queue/{platform}/Approved/
  05_Publish_Queue/{platform}/Published/
  99_Reports/
```

Source folders remain read-only unless the user explicitly authorizes a source mutation.
