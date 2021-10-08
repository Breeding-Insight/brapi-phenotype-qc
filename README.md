# BrAPI Phenotype QC Tool

The objective of this tool is to streamline routine phenotype QC processes. Interactive data filtering and viewing can allow faster cleaning of raw data compared to Excel.

## Planned Features

### High priority
- [X] Load studies from specified BrAPI server
- [X] Choose study to load observations from
- [X] Plot type selection
    - [X] histogram
    - [X] scatter plot
- [X] View plot
    - [X] by variable type
    - [ ] configurable axes variables
- [X] Select/filter points
    - [ ] by collector
    - [ ] by value range
    - [X] by interactive selection on plot
    - [ ] by interactive number of std dev from mean
    - [ ] by interquartile range
- [X] Remove observations
- [ ] Change observation properties
    - [ ] variable (dropdown of variables in study)
    - [ ] value
- [ ] Create new QCed study and upload (Do not modify raw data study)
    - [X] study
    - [ ] observation variables
    - [ ] observations

### Low priority
- Export to spreadsheet for additional QC not available in tool
- Import from spreadsheet
- View observation units plot
    - Indicate whether observation unit has any observations
    - Select observation unit to show observation details
- Algorithmic flagging of outliers
- Auth
- Error handling
- Layout & styling
