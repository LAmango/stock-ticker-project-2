# stock-ticker-project-2
The second version of the ticker project. This time the files will be class and will have driver file to run them. We will also be using a database pull data from. Testing and documentation will also be an important part of this project using pytest, sphinx and autodoc. 


### Sphinx
```
	make html
```
To spin up a web server to check the docs
```
	python3 -m http.server
```
Copy '0.0.0.0' address to browser

### Py.test
1. Create a python file in the **stock** directory
2. Call them **test_tickers.py** and **test_query.py** respectively
3. Use **test_fetcher.py** as a reference on how to import and make tests.

To run pytests:
```
	pytest -v
``` 
To check the coverage:
```
	pytest --cov=stock
```
To report to check coverage of files:
```
	pytest --cov=stock --cov-report html:coverage
```
A coverage file will be added to the current directory.
Open './coverage/index.html' in the browser and click on the file to see what is missing coverage.