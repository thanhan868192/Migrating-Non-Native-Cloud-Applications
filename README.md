# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource              | Service Tier    | Monthly Cost    |
| ----------------------------| ----------------| ----------------|
| *Azure Postgres Database*   |  Standard_B1ms  |  $35.84        |
| *Azure Service Bus*         |  Standard       |  $0.05         |
| *Azure Fuction App*         |  Consumption    |  $0.00         |
| *Azure Web App*             |  Basic (B1)     |  $13.87        |  
| *Storage Account*           |  Standard       |  $16,594.17    |
| *Total*                     |                 |  $16,643.93    |
## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

- The Azure Web App hosts the frontend of the application, providing a scalable and reliable platform for serving web pages to users.
It ensures the application can handle increased traffic by automatically scaling resources as needed, making it suitable for applications with varying workloads.
Azure Web App simplifies deployment and management tasks, allowing developers to focus on building and improving the frontend user experience.
By separating the frontend from the backend, it enables easier maintenance, upgrades, and debugging, as changes to one component don't directly impact the other.
Azure Functions:

- Azure Functions serve as the backend processing layer, handling various tasks asynchronously.
They can process user requests for data, handle background tasks, or respond to events triggered by other services or components.
Azure Functions reduce operational overhead by automatically scaling based on incoming events, ensuring efficient resource utilization and cost-effectiveness.
Their event-driven nature makes them well-suited for scenarios where actions need to be triggered based on specific events or conditions.
By offloading processing tasks to Azure Functions, the web application's responsiveness is improved, as heavy computational tasks don't block the main execution thread.
Scalability and Flexibility:

- The combined use of Azure Web App and Azure Functions provides a flexible architecture that can adapt to various application requirements and scale seamlessly to meet demand.
Azure Functions' auto-scaling capabilities ensure that resources are allocated efficiently, reducing the risk of under utilization or over-provisioning.
As traffic to the application increases, both Azure Web App and Azure Functions can dynamically scale resources to handle the load, ensuring a consistent user experience.
Efficient Resource Utilization:

- Azure Functions' pay-as-you-go pricing model allows for efficient resource utilization, as you only pay for the compute resources used during execution.
This cost-effective approach makes Azure Functions suitable for applications with sporadic or unpredictable workloads, as resources are allocated dynamically based on demand.