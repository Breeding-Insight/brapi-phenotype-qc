# BrAPI Phenotype QC Tool

The objective of this tool is to streamline routine phenotype QC processes. Interactive data filtering and viewing can allow faster cleaning of raw data compared to Excel.

## Planned Features

### High priority
- [X] Load studies from specified BrAPI server
- [X] Choose study to load observations from
- [X] View observations vs date plot
    - [X] by study 
    - [ ] by variable type
- [X] Select/filter points
    - [ ] by collector
    - [ ] by value range
    - [X] by interactive selection on plot
- [ ] Remove observations
- [ ] Change observation properties
    - variable
- [ ] Create new QCed study and upload
    - Do not modify raw data study

### Low priority
- Export to spreadsheet for additional QC not available in tool
- Import from spreadsheet
- View observation units plot
    - Indicate whether observation unit has any observations
    - Select observation unit to show observation details
- Algorithmic flagging of outliers
- Auth
- Error handling

