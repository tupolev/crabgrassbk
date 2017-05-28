# Crabgrassbk
## Crabgrass page backup crawler
### Description
This a crawler to save all created pages within a [crabgrass](https://riseup.net) group, intially on riseup.net.
It uses selenium webdriver (python dependency) and phantomJS (included).

### Features
- Can download page images
- Can download page attachments
- Can generate Zip file package with the backup directory
- File extensions for downloadable attachments is configurable

### Requirements
- Python 3.5
- Pip
- Check requirements.txt for complete list of requirements

### Setup
- `git clone git@github.com:tupolev/crabgrassbk.git`
- (We recomment using a virtualenv here)
- `pip install -r requirements.txt`

### Execution
Just configure properly the `conf/config.yml` file and run `python crabgrassbk.py`

### Credits
Written by _tupolev_ for [_Oficina Precaria Berlín_](http://oficinaprecariaberlin.org) organization.

**RiseUpLabs Crabgrass repository**: https://0xacab.org/riseuplabs/crabgrass

**Rise Up Crabgrass**: https://we.riseup.net

