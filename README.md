# Weddify

A wedding planner website where Vendors such as Marriage Hall owners, Photographers, Caterers, and Bridal salons can register their services and Users can book them.

Features - 
* It is based on Microservices Architecture.
* The microservices are created using Django and Springboot.
* Django Templates and Bootstrap are used for the responsive front end.
* RabbitMQ and Celery are used for asynchronous communication.
* Static and media files are stored on S3.
* nginx server as Reverse Proxy.
* Payments are handled using Razorpay Payment Gateway.
* Dockerised for easy deployment.

How to start -
1. Git clone
2. Change directory to Weddify_Microservices
3. Register your AWS and Razorpay keys in the settings.py files.
4. Run 'docker compose up'
5. Sit back and relax!
