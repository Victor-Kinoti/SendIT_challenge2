[![Build Status](https://travis-ci.com/Victor-Kinoti/SendIT.svg?branch=ch-tests-161805245)](https://travis-ci.com/Victor-Kinoti/SendIT)
<<<<<<< HEAD
[![Coverage Status](https://coveralls.io/repos/github/Victor-Kinoti/SendIT_ch2/badge.svg?branch=reviews)](https://coveralls.io/github/Victor-Kinoti/SendIT_ch2?branch=reviews)
[![Maintainability](https://api.codeclimate.com/v1/badges/cc4addaa0ed3bff16ae3/maintainability)](https://codeclimate.com/github/Victor-Kinoti/SendIT_ch2/maintainability)
=======

[![Coverage Status](https://coveralls.io/repos/github/Victor-Kinoti/SendIT/badge.svg?branch=ch-tests-161805245)](https://coveralls.io/github/Victor-Kinoti/SendIT?branch=ch-tests-161805245)

>>>>>>> 47528c9a4996547ce8e28ff638f96332ff9a9d76

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
| POST| api/v1/register| registers new user |
| POST| api/v1/login|   logs in a registered user|
| GET | api/v1/parcels|gets all user parcels|
| GET | api/v1/parcels/order_id|gets specific order|
| PUT | api/v1/parcels/order_id/cancel|cancels specific order|
| GET | api/v1/users/parcels|admin gets all orders|
| GET | api/v1/users/<name>/parcels|admin gets specific user's orders|
| PUT | api/v1/users/<user_id>/delivered|admin sets order to status delivered|
| PUT | api/v1/users/<user_id>/paid|admin sets order to status Paid|

***manually test using postman***

Here's the [documentation](https://documenter.getpostman.com/view/4146964/RzZAme6q) on how to consume the API on a local machine. New users need to Register then Login

**Heroku site** [Here](https://sendit-keynote.herokuapp.com)

