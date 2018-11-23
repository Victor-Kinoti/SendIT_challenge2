[![Build Status](https://travis-ci.com/Victor-Kinoti/SendIT.svg?branch=ch-tests-161805245)](https://travis-ci.com/Victor-Kinoti/SendIT)
[![Coverage Status](https://coveralls.io/repos/github/Victor-Kinoti/SendIT_ch2/badge.svg?branch=reviews)](https://coveralls.io/github/Victor-Kinoti/SendIT_ch2?branch=reviews)
[![Maintainability](https://api.codeclimate.com/v1/badges/cc4addaa0ed3bff16ae3/maintainability)](https://codeclimate.com/github/Victor-Kinoti/SendIT_ch2/maintainability)

SendIT is a courier service that helps users deliver parcels to different destinations. 
### Features:

1. New user can create an account for sendit app

2. User signed up can login/logout

3. User can create a parcel delivery order

4. User can get history of parcel orders

5. User can get specific parcel order by ID

6. User can cancel an order not yet delivered

7. User can update destination of an order

8. Admin can get orders of a specific user


## Installing
* Create and activate a virtual enviroment:

`pip install virtualenv`

**activate:**

`virtualenv env`

`source env/bin/activate` on your terminal

## Clone Sendit repo
`git clone https://github.com/Victor-Kinoti/SendIT.git` on your terminal

install dependencies:

`pip install -r requirements.txt` in the root folder 


| Method        | URL/Endpoint          | output  |
| ------------- |:-------------:| -----:|
| POST| api/v2/parcels| create order |
| POST| api/v2/signup| registers new user |
| POST| api/v2/login|   logs in a registered user|
| GET | api/v2/parcels|gets all user parcels|
| GET | api/v2/parcels/order_id|gets specific order|
| PUT | api/v2/parcels/order_id/presentlocation|present Location|
| GET | api/v2/users/parcels|admin gets all orders|
| GET | api/v2/users/<name>/parcels|admin gets specific user's orders|
| PUT | api/v2/users/<user_id>/delivered|admin sets order to status delivered|
| PUT | api/v2/users/<user_id>/paid|admin sets order to status Paid|

***manually test using postman***

Here's the [documentation](https://documenter.getpostman.com/view/4146964/RzZAme6q) on how to consume the API on a local machine. New users need to Register then Login

**Heroku site Version !** [Here](https://sendit-keynote2.herokuapp.com/api/v1/parcels)

**Heroku site Version !** [Here](https://sendit-keynote2.herokuapp.com/api/v2/parcels)

Run `export DATABASE_URL="dbname='sendit' user='postgres' host='localhost' password='keynote269' port='5432'"` to setup db environment

Run **PWD** on terminal to get location of repo then type: `export PYTHONPATH=$PYTHONPATH:+ pwd output` helps in importations

