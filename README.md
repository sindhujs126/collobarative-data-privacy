Cap Data Privacy
# Data Cap Privacy using spark framework

An enhanced privacy preservation approach with enforcing policies for processing big data in spark framework

## Requirements
The following are required for running the project.
```bash
python 3.6 +
pip 20.0 +
java
Fastapi 0.60 +
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the packages in requirements.txt file.

```bash
pip install -U -r requirements.txt
```

## Usage

```python
python run.py 
```
Once the project runs open your browser and open `http://localhost:5000`


## Steps
* Once the project is running and you opened the browser you will have to upload two files: (example data is found in data-set folder of the project.)
1. CSV File which contains all the data fields which you wanted to compress with security.
2. YAML File which will contain all the key mappings for encrypting the data.

* Once the files are uploaded click on generate report button to get you results.

* In the results you can see two tables one with the data you uploaded and other with the encrypted data.

* OnClicking Download Button the report will be downloaded directly.

## Notes
* Make sure the fields in the tables are less and data is less. (since its displayed in UI).
* Also not that the yaml fields should match the field names in the csv data set.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
