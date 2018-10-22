# Edyst Challenge
### A simple flask app that counts words in given URL.

## Dependencies
 * Flask==1.0.2
 * Flask-SQLAlchemy==2.3.2
 * Flask-WTF==0.14.2
 * redis==2.10.6
 * requests==2.19.1
 * rq==0.12.0
 * SQLAlchemy==1.2.12
 
 ## Setup
 Following steps assume that you have python3 installed and created a virtual enviroment on your computer.
 
 ### Install the dependencies
 ``` pip install -r requirements.txt ```
 
 ### Run redis worker
 Activate your virtual environment and go to project directory using the console and run the following command.
  
  ``` python worker.py ```
  
 > Note: You should keep this *worker* running in background.
 
 ### Create Database
pen a new teminal window and activate your virtual enviroment, then create database using
 
 ``` python create_db.py```
 
 
 ### Run application server
 Open a new teminal window and activate your virtual enviroment, then run the app using
 
 ``` python app.py ```
 
Now open your browser and visit ``` http://localhost:5000 ```


### Run Tests
Open a new terminal window and activate your virtual environment, then run tests using

``` python tests.py ```



