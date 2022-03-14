# Backend interview API
## Run project
1) Clone repository
2) `pip install -r requirements.txt`
3) `python manage.py db init`
4) `python manage.py db migrate`
5) `python manage.py db upgrade`
6) Start server with `manage.py runserver`
## Endpoints
### 

## Customer order line [/customer-order-line]

### List all customer order line [GET]
`GET api/customer-order-lines`
### Create new customer order line [POST]
`POST api/customer-order-lines`
```json
{
    "order_number": "ORD_1567",
    "item_name": "LAPTOP",
    "status": "SHIPPED"
}
```
### Edit one customer order line [PUT]
`PUT api/customer-order-line/{id}`
```json
{
    "status": "PENDING"
}
```
### Delete one customer order line [DELETE]
`DELETE api/customer-order-line/{id}`
### Get the status of every order [GET]
`GET api/get-customer-order-status/`

## Customer order [/customer-order]

### List all customer order [GET]
`GET api/customer-orders`
### Create new customer order [POST]
`POST api/customer-orders`
```json
{
    "ord_id": "113-8909896-6940269",
    "ord_dt": "10/23/19",
    "qt_ordd": 1
}
```
### Edit one customer order [PUT]
`PUT api/customer-order/{id}`
```json
{
    "ord_dt": "11/23/19"
}
```
### Delete one customer order [DELETE]
`DELETE api/customer-order/{id}`
### Get the seasons of every order [GET]
`GET api/get-seasons/`

## Customer order [/weather]

### List all weathers [GET]
`GET api/weathers`
### Create new weather [POST]
`POST api/weathers`
```json
{
    "date": "1/2/20",
    "was_rainy": true
}
```
### Edit one weather [PUT]
`PUT api/weather/{id}`
```json
{
    "ord_dt": "11/23/19"
}
```
### Delete one weather [DELETE]
`DELETE api/weather/{id}`
### Get changes of state on was rainy [GET]
`GET api/detect-change/`
