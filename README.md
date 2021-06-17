# Item management

*This API implements item management (create, delete, read) and transfer of items between users.*

## Using with Docker

To run your application in a docker container, use the bash script.

*example: `./startup.sh`*

You can access the API at http://localhost:8000 and access the documentation at http://localhost:8000/swagger-ui/  

## Methods 

***/registration - user registration:***
- POST request
- request parameters: 
  - login
  - password
- response parameters: 
  - successful registration message 


***/login - user authorization:***
- POST request
- request parameter:
  - login
  - password
- response parameters: 
  - temporary token 


***/items/new - item creation:***
- POST request
- request parameters:
  - temporary token
  - name
- response parameter:
   - message about the successful creation of the item
   - item id 
   - item name 


***/items/id - removing an item:***
- DELETE request
- request parameters:
  - temporary token
  - item id
- response parameter:
  - successful item deletion message 

  
***/items - getting a list of items:***
- GET request
- request parameters:
  - temporary token
- response parameter:
  - list of custom items 
  
  
***/send - generating a link to transfer the item:***
- POST request
- request parameters:
  - item id 
  - login of the receiving user 
  - temporary token
- response parameters:
  - the link the receiving user should follow 
  
  
 ***/get - follow the link to get an item:***
- GET request
- request parameters: 
  - the link generated in the response of the dispatch method
  - the receiving user's temporary token to prove ownership
- response parameters: 
  - message about the successful receipt of the item 
  
  
