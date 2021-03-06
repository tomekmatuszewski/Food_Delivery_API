#### Simple API for food delivery company:

1. Delivery registration
2. Add employee and client to database
3. Register order -> automatically calculate the travel distance
4. Track all orders / filter by dates - prices etc.

:snake: FAST_API :snake:, SQLAlchemy

    - FrontEnd      -> Semantic UI
    - Unit tests    -> Pytest 
    - Testing API   -> Postman / Insomnia
    - DB            -> SQLite

to run app:
    
    clone repo, create virtual env and activate
    $ pip install -r requirements.txt
    $ python run.py
    
App use external API (https://developer.mapquest.com/) to calculate distance between Client address and customer:
Set your API_KEY for proper data loading:

    $ export API_KEY=<your API KEY>
    
After this load data:

    $ python load_db.py
    
- http://127.0.0.1:8000/fast_delivery
    
Some screens:

![alt text](screens/screen1.png)

![alt text](screens/screen2.png)

![alt text](screens/screen3.png)

   
    
    
    
    
    





