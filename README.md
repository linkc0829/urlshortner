# A Url Shortner With Rate Limiter Using Django, Redis and Postgres


## How To Use
### Prerequisites
* Docker and Docker Compose 

### Usage
```
git clone https://github.com/linkc0829/urlshortner.git

cd urlshortner

docker compose up --build -d
```

## API Documentation
### Create Short Url
```
POST /url
```
#### Description: Create a shorten url given the origin one
* create a 10 digits hash to represent the origin url and store the expiration in postgres
* cache the hash in redis for 30 days so that once reach the expiration, the shorten url become invalid

#### Request Parameters:

| Name | Type | Required | Sample | Description |
| -------- | -------- | -------- | -------- | -------- |
| origin_url     | string     | True     | https://www.google.com | the url to shorten

#### Response Example:
| Name | Type | Sample | Description |
| -------- | --------  | -------- | -------- |
| short_url     | string       | http://127.0.0.1:8000/url/90e9420393 | the shorten url
| expiration_date | ISO Date | 2025-04-25T10:54:08.880 | the date the shorten url expire
| success | boolean | true | if operation success or not
| reason | string | | indicate the reason if failed

#### Request Example:
```
curl --location 'http://127.0.0.1:8000/url/' \
--header 'Content-Type: application/json' \
--data '{
    "origin_url": "https://google.com"
}'
```

#### Response Example:
```
{
    "short_url": "http://127.0.0.1:8000/url/90e9420393",
    "expiration_date": "2025-04-25T10:54:08.880",
    "success": true
}
```

#### Error Example:
```
{
    "success": false,
    "reason": "URL too long"
}
```


### Redirect To Origin Url
```
GET /url/<str:hash>
```

#### Rate Limit: 1000 times/minute for every shorten url

#### Description: Redirect the shorten url to origin url with a rate limiter
* rate limit the api using sliding window technique with redis sorted set
    * one minute window and limit 1000 times
* use the hash as key to get the cache origin_url then redirect to the target

#### Request Example
```
curl --location 'http://127.0.0.1:8000/url/99999ebcfd'
```

#### Error Example
```
{
    "success": false,
    "reason": "ratelimited"
}
```





