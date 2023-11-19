# CMPE 273 Hackathon: Macroeconomic Researcher Time Series Dashboard

## Overview

Our submission for CMPE 273 Hackathon challenges participants to develop a solution that addresses UN Sustainable Development Goal #1 - No Poverty. The focus of this hackathon is to create a Macroeconomic Researcher Time Series Dashboard, leveraging a variety of economic indicators and data sources provided in the `CMPE273_DataSources_20231111_Hackathon.zip`.

## Features

### Enterprise Distributed Architecture
- **Prompt Management:** Capable of receiving and storing prompts from numerous users.
- **Response Storage:** Efficiently stores responses for later retrieval and analysis.
- **Network and Local Mode:** Operates in both network-connected and local environments.
- **REST Deployment:** Utilizes RESTful APIs for seamless integration and communication.

### Natural Language Interaction with Data
- **User-Friendly Interface:** Allows users to interact with the dashboard using natural language, making data access and analysis more intuitive.

### Budget Speeches Integration
- **Real-Time Analysis:** Enables real-time analysis of budget speeches, providing valuable insights for economic researchers and government representatives.

## Data Tables

### Macroeconomic Table
- Indicators like GDP Growth Rate, Current Account Balance, and various forms of Foreign Direct Investment.

### Agricultural Table
- Covers indicators such as Agricultural Contribution to GDP, Manufacturing, Fertilizer Consumption, etc.

### Debt Table
- Includes Total Reserves, Debt Service, GNI, and more.

### Food Security (Imports)
- Data on agricultural imports like wheat and rice for countries like Saudi Arabia and Egypt.

## Personas

### ECON Researcher
- Utilizes the dashboard for in-depth economic research and analysis.

### Government Representative
- Leverages the tool for policy making, economic planning, and international trade insights.

## Redis
- Implemented for enhanced performance and scalability.


## Screenshots
![WhatsApp Image 2023-11-19 at 14 19 18](https://github.com/AtharvaJadhav/systems-hackathon/assets/55223872/35acce40-cf34-4ed1-9517-ff5936a1b37e)

![WhatsApp Image 2023-11-19 at 14 38 59](https://github.com/AtharvaJadhav/systems-hackathon/assets/55223872/f5293e2f-e53a-4f77-b1d0-8d4ca1fb982b)

### Architectural Diagram
<img width="1103" alt="Screen Shot 2023-11-18 at 3 34 57 PM" src="https://github.com/AtharvaJadhav/systems-hackathon/assets/55223872/bd34cae3-ee70-4cdd-a440-dfbc30f6207b">

---

## Getting Started

Installation and Configuration Instructions for the Systems-Hackathon Repository

Prerequisites:
- Python 3.8 or higher
- Docker and Docker Compose
- Git (for cloning the repository)

Step 1: Clone the Repository
First, clone the repository to your local machine:
git clone https://github.com/AtharvaJadhav/systems-hackathon.git
cd systems-hackathon

Step 2: Set Up Environment Variables
Create a .env file in the root directory of the project and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here
Replace your_openai_api_key_here with your actual OpenAI API key.

Step 3: Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

Step 4: Docker Compose Setup
Use Docker Compose to set up and start the Redis service:
docker-compose up -d
This command will download the necessary Docker images and start the Redis service in the background.

Step 5: Start the Flask Application
Run the Flask application:
python app.py
This will start the Flask server, typically accessible at http://localhost:5000.

Step 6: Access the Application
Open your web browser and navigate to http://localhost:5000 to access the Macroeconomic Researcher Time Series Dashboard.

Additional Configuration (Optional):
- If you need to customize the Redis configuration, you can modify the docker-compose.yml file.
- For production deployment, consider using a WSGI server like Gunicorn and running the Flask app in a more secure and scalable manner.

Troubleshooting:
- If you encounter any issues with the Docker setup, ensure Docker is running correctly on your system and you have the necessary permissions.
- For issues related to Python dependencies, ensure you are using the correct version of Python and have all the required packages installed.

---

## Team

- Omkar Nagarkar
- Sangram Jagtap
- Purvil Patel
- Atharva Jadhav

---

## License

This project is licensed under the MIT License.
