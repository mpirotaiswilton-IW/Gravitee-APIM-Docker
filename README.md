# Gravitee-APIM-Docker
This repo contains a dockerized Gravitee API Manager deployment and python script to initialize it with 2 exported APIs and 3 Applications
 
## Summary
[Oracle-Invoice-Kong](#oracle-invoice-kong) 
* [Summary](#summary)
* [Setup and Pre-requisites](#setup-and-pre-requisites)
* [Deployment](#deployment)
* [Verifying the API Manager deployment](#verifying-the-api-manager-deployment)
* [Stop the API Manager](#stop-the-api-manager)
---
## Setup and Pre-requisites

1. If not already installed:

- Install Docker on your device (you can use the following link for a guide: <https://docs.docker.com/get-docker/)>)
- Install Python on your device (you can find the version used to develop the initialization script with the following link: <https://www.python.org/downloads/release/python-3120/>)

2. Clone this repository or download the .zip file from GitHub (extract the downloaded zip file)

## Deployment

1. Using a Command Line Interface of your choosing, change directory to the downloaded/cloned repository.

2. To deploy the Gravitee API Manager, run the following command:

    ```
    docker-compose up
    ```

    If you want to deploy the Gravitee API Manager in detached mode, run the command below:

    ```
    docker-compose up -d
    ``` 

    This deployment will take roughly a minute (excluding the time to pull the gravitee container images).

3. 6 Docker containers should now be running:
    - `gio_apim_elasticsearch`
    - `gio_apim_mongodb`
    - `gio_apim_gateway`
    - `gio_apim_portal_ui`
    - `gio_apim_management_ui`
    - `gio_apim_management_api`

## Verifying the API Manager deployment

1. On a web browser, go to the API Manager Management GUI <http://localhost:8084/>.
2. If prompted, login with the following credentials:
    ```
    username: admin
    password: admin
    ```
3. Once you are redirected to the dashboard, you should see a count of APIs and Applications. At this stage you should see 0 APIs and 1 Application.

## Setting up the API Manager

At this current state, the API manager has no APIs and only an automatically generated Application. To populate it with APIs and Applications, you'll need to run an initializing python script. 

### Run the initializing Python script

1. Using a Command Line Interface of your choosing, change directory to the downloaded/cloned repository.
2. Change directory again to the `/init` directory.
3. Run the python script with the following command: 
```
python init-gravitee.py
```
4. When the script has finished, you should see the following message in your CLI:
```
Initialization now finished. Exiting Program...
```
### Verifying the Initialization

1. On a web browser, go to the API Manager Management GUI <http://localhost:8084/>.
2. If prompted, login with the following credentials:
    ```
    username: admin
    password: admin
    ```
3. Once you are redirected to the dashboard, you should see a count of APIs and Applications. At this stage you should see 2 APIs and 4 Application.
4. On the left-hand side, click the `APIs` button and you should see a list with 2 APIs:
    - `REST API for Oracle Fusion Cloud Financials - Invoice (2023.12.14)`
    - `Swagger Petstore - OpenAPI 3.0 (1.0.17)`
5. Both APIs should also have 2 plans:
    - `Standalone App`
    - `Multi-API App`

    You can see both plans in each API by clicking on the API name in the list and then, on the left-hand side, clicking `Plans`.
6. On the left-hand side, click the `Applications` button and you should see a list with 3 new Applications: 
    - `Centralized App`
    - `Oracle Cloud Finance Invoice App`
    - `Pet Store App`
7. the `Centralized App` will have 2 Subscription from both API with the `Multi-API App` plan name and the `Oracle Cloud Finance Invoice App` and `Pet Store App` will have 1 plan each with the `Standalone App` plan. 

    You can see these in each applications by clicking on the Application name in the list and then, on the left-hand side, clicking `Subscriptions`.

## Stop the API Manager

To stop the Gravitee API Manager container, run the following command:
```
docker-compose down
```