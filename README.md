##Shopping Cart

- **Setup**

- In terminal, git clone https://github.com/BasileKoko/shopping_cart
- cd shopping/
- Create a virtual environment run 'virtualenv -p python3 your_env_name'
- Install project dependencies pip install -r requirements.txt
- Create a local database and set environment variable (DB_NAME, DB_USER, DB_PASSWORD, DB_LOCAL_HOST, DB_PORT)
- Run python manage.py migrate
- Items and Voucher data will be preload after migration
- visit 127.0.0.1:8000 (Django Rest Framework page)
- For data entry use the option 'raw data', 'application/json'
- Enter data in the content field
- Use comma to add items and always remove the last comma when removing item (i.e: 1,2 or 3) 

### URLS to test:
- Unauthenticate user won't be able to access resource
```
 1. To register a new user
/api/v1/rest-auth/registration

2. To login
/api/v1/rest-auth/login

3. To logout
/api/v1/rest-auth/logout

4. To see list of items
/api/v1/items

5. To see a single item (i.e: item ID 1)
/api/v1/items/1

6. Create a basket with or without items
/api/v1/basket/add
relaod page to see the item created

7.Change Basket content(i.e basket ID 1)
/api/v1/basket/change/1
make sure to add or remove accordingly as explained above

8. Move item from basket to trolley
/api/v1/basket/change/add_to_trolley

9.Add a trolley
/api/v1/trolley/add
reload the page to see the item created

10. Change trolley content (i.e for trolley ID 1)
/api/v1/trolley/change/1
make sure to add or remove accordingly as explained above

11. Add order
/api/v1/order/add

User can only enter payment method and voucher code
The order total cost, status and list of items ordered will be populated automatically
if order status is completed items will be removed from user trolley
Order history will show as the orders with status completed. 

```

- **Notes**
- The folder 'file' shows the initial database schema and workflow
- At the moment this functionality does not work as expected.
It can fixed with a bit more debugging time.
But the logic is implemented
- More tests could be added 