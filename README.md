
# Team 4 Project 2
## About
We have created a database for NPMJS modules that allows users the ability to upload, download, update, rate, and delete packages using a rating application (referred to as the “trustworthiness module”). Our system allows users to interact with it via a RESTful API or a user-friendly, accessible, ADA-compliant front-end. At ingestion, packages are tested to ensure they are trustworthy enough to be stored in the system using the trustworthiness module. From there, users can browse packages using a paginated, searchable, package viewer. Packages can be requested from the system and rated by providing the package’s ID. When needed, the entire system may be reset.

## Getting started

There are four types of requests that can be made:

  

POST:
-   Upload package "/package"
-   View packages "/packages"

DELETE

-   Delete package
    
-   Reset system "/reset"
    
-   Delete all versions of package by name "/package/byName/{name}"
    

PUT

-   Update package "/package/{id}"
    

GET

-   Download package "/package/{id}"
    
- Rate package "/package/{id}/rate"

## Requirements:
Java 17
Python 3.8

## License

 
MIT
