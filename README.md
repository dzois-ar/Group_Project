# Ecommerce
<p align="center">
   <img  src="static/images/logo.png" width="200" >
</p>   

To run this project in your computer, follow the steps below
-------------------------------------------------------------

Create virtual environment: virtualenv venv

Step 1. Make and activate virtual Environment in your computer
-------------------------------------------------------------

            In windows
            > virtualenv venv
           > Scripts\activate
           
           In mac and linux
           $ virtualenv venv 
           $ source bin/activate
           
Step 2. Clone the project
-------------------------------------------------------------           

     git clone https://github.com/dzois-ar/Group_Project-Eshop.git
     
     
      if you donot have git in your computer, install it before and clone it again.
      
      
Step 3: Install requirements  
-------------------------------------------------------------
     pip install -r requirements.txt
                or 
     pip install django pillow requests six
     
     
Step 4: Apply the migration if any
-------------------------------------------------------------
     python manage.py migrate
     
     `
 Step 5: You can now open project folder in your editor
-------------------------------------------------------------    

Step 6: Run Development server
-------------------------------------------------------------
     python manage.py runserver
     
     
     -->Then, the development server will be started at: http://localhost:8000/eshop/
     
    
 Instructions:   
-------------------------------------------------------------
1. You have to activate the virtual environment.
2. Then you have to run the server, to start locally hosting the project
3. After you go to the browser and you visit the following link: http://localhost:8000/eshop/
4. Now as a superuser, you could manage the Django administration controls (database, users etc.) via: http://localhost:8000/admin/ 
Website Keys and Passwords:

  - Superuser: Username: vkara Password: 123456789
  - Random User: Username: vasiliskar95 Password: 123456789
  
######  Webpage Description: As you log in as a user, the page offers:

  1. The chance to choose men and women products. At the same time, you could try to search for a specific item.
  2. You could place products to the cart and pay via Paypal or credit or debit card
  3. In the end of the page there is a chat icon, where you could contact as a customer with the eshop.
  
  App Preview :
-------------------------------------------------------------

![Screenshot from 2022-11-23 00-32-52](https://user-images.githubusercontent.com/80916754/203435008-f4e3761e-d502-49c1-87a1-40b53f0a67f7.png)

![Screenshot from 2022-11-23 00-30-33](https://user-images.githubusercontent.com/80916754/203434616-4e912c48-cc5f-405b-84c0-6a14f35ddc5f.png)



## User page:
![Screenshot from 2022-10-10 16-36-39](https://user-images.githubusercontent.com/80916754/203432264-26e20cd1-f410-46c1-8faf-6f33b4cddbdc.png)

## View page:
![Screenshot from 2022-10-10 16-37-15](https://user-images.githubusercontent.com/80916754/203432494-46b2c004-fb1a-43e9-97fa-bb3ac3c914a7.png)


## Shop page:
![Screenshot from 2022-10-10 16-38-42](https://user-images.githubusercontent.com/80916754/203436782-58f16e35-d829-4310-ac08-afa272455498.png)



## Checkout page:
![Screenshot from 2022-10-10 16-39-21](https://user-images.githubusercontent.com/80916754/203436883-fc2bbd3b-c320-4ef0-bd40-91473f785cf2.png)


## Chat page:

![Screenshot from 2022-10-10 16-55-06](https://user-images.githubusercontent.com/80916754/203436991-d6a6bcd8-c554-4ff3-a05f-d45bbd09d9ab.png)

