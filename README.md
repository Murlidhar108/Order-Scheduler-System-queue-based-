# Order-Scheduler-System-queue-based- 

## The project is about queue based order scheduling system in which user will be authenticated and they schedule their orders. Orders may be one time order or can have recurring nature,  it is totally based on the user requirement. Along with this user can manage their orders like they can view, update or even delete them. They can also convert the one time order to recurring nature or vice versa. For the History purpose, status of the order are logged into the log file along with their ids, and timestamps and status. The project was to demonstrate how scheduled and recurring tasks can be handled reliably in a backend system using a queue-based architecture.

## Features 
- Authentication (JWT)
- One-time & recurring orders
- Queue-based execution
- Logging / notifications
- CRUD operations

Tech Stack

Backend - Node.js
Database - MySql
Queue - Bull
Auth - Jwt
Logging - File Handling

System Flow:

The system follows a layered backend architecture where user interactions are handled through REST APIs, while order execution is processed asynchronously using 
a background job queue.

Users interact with the API layer to authenticate and manage their orders. When an order is created, the backend stores the order details in the database and schedules a corresponding job in the queue for execution at the specified time or interval.

A worker processes the job by simulating order placement, updating execution status, and writing logs. This separation of request handling and execution ensures reliable, non-blocking, and fault-tolerant order processing.

Client → API Layer → Database → Job Queue → Worker → Execution → Logs



Database Schema

The system uses MySQL to store user and order information. There are two main tables: User and Order.

User Table
Column Name	                           Type	                                       Description
user_id	INT, PK, AUTO_INCREMENT     	Unique                                       ID for each user
email	                                VARCHAR	                                     User’s email for login
password	                            VARCHAR	                                     Hashed password for security
token	                                VARCHAR	                                     JWT token for authentication




Order Table
Column Name	                                         Type	                                 Description
order_id	                                     INT, PK, AUTO_INCREMENT	                   Unique ID for each order
user_id	                                       INT, FK	References user.user_id            links order to user
order_name	                                         VARCHAR	                          Name or description of the order
schedule_time                                       	DATETIME	                          Scheduled execution time for the order
status	                                       'Scheduled','completed'                    	Current status of the order
job_id	                                              VARCHAR	                           ID of the corresponding job in the Bull queue
is_recurring	                                        BOOLEAN	                              Whether the order is recurring or one-time
repeat_interval	                                        INT	                                       Interval value for recurring orders
repeat_unit                                    	'minutes','hours','days'               	Time unit for recurring orders
max_executions	                                         INT	                             Maximum number of times the order should execute
executions_count	                                      INT	                              Number of times the order has already executed







Order Scheduling Logic

One-Time Orders

These orders are executed only once at the scheduled time specified by the user. When a one-time order is created:
The order details are stored in the Order table. A job is added to the Bull queue with a delay corresponding to the scheduled execution time.
The job executes at the scheduled time and updates the order status in the database once completed.

2️⃣ Recurring Orders

Recurring orders are executed multiple times at defined intervals, up to a maximum number of executions.
Key fields controlling recurring behavior:
repeat_interval – the time between executions (e.g., 5 minutes, 1 hour)
repeat_unit – the unit of the interval (minutes, hours, days)
max_executions – the maximum number of times the order should execute
executions_count – tracks how many times the order has been executed so far
Each time the job runs, executions_count is incremented and got updated in database. Once it reaches max_executions, the recurring job is automatically stopped.


Job Linking: Database ↔ Bull Queue

Every order is associated with a job in Bull, identified by a unique job_id.
This link allows the backend to:
Track which job corresponds to which order
Cancel or update jobs if the user modifies or deletes an order
Maintain reliability and fault tolerance, ensuring jobs are executed even if the server restarts
For recurring orders, the job is repeatable in Bull, and its execution state is synchronized with the database using executions_count and status.


  User → place an order → DB → Bull Queue → Execution → Update DB → Log



  Reliability & Fault Tolerance
Fault tolerance
A bull queue allows the backend to decouple order creation from execution, meaning:
Users can schedule orders without waiting for them to execute Jobs are handled asynchronously so tha multiple jobs can be processed concurrently without blocking the server
Job queues also allow centralized tracking of execution state (pending, running, completed, failed).

Reliability
Scheduled jobs execute at the correct time andjJobs are not lost due to server crashes or failures.
Recurring jobs execute exactly the intended number of times (max_executions).
Failed jobs can be retried or tracked for manual intervention. 


API Documentation

1. http://localhost:3000/auth/signup -> user signup
2. http://localhost:3000/auth/login -> user login
3. http://localhost:3000/orders/create -> create orders (some feils are optional)
4. http://localhost:3000/orders/ -> view all orders for a user
5. http://localhost:3000/orders/: order_id -> update order
6. http://localhost:3000/orders/: order_id -> delete a specific order
7. http://localhost:3000/auth/me  -> get details of current user
8. http://localhost:3000/auth/logout  -> user log out



Setup & Installation

1. clone repo
2. set up env files with all details + install Mysql Workbench + Postman
3. install dependencies and modules.
      For backend
        -> in root directory: (1) npm install
                              (2) npm run dev   ( in the root directory )
                              (3) node src/workers.order.workers.js   ( in the root directory and in other terminal )
   
      For frontend
         (1) cd client
         (2) npm install
         (3) npm run dev

Order-System-Scheduling
├──────── src/
│          ├── app.js
│          ├── server.js
│          ├── config/
│          │   ├── db.js
│          │   ├── redis.js
│          │   └── queue.js
│          ├── auth/
│          │   ├── auth.controller.js
│          │   ├── auth.service.js
│          │   └── auth.routes.js
│          ├── orders/
│          │   ├── order.controller.js
│          │   ├── order.service.js
│          │   └── order.routes.js
│          ├── logs/
│          │   ├── orders.log
│          ├── middleware/
│          │   └── auth.middleware.js
│          └── workers/
│          │   └── order.workers.js
│          │──utils/
│          │   └── jwt.js
│          │   └── logger.js
│   
├──────── Client
               └── src/





















