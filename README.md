# Receipt Processor

Build a webservice that fulfils the documented API. The API is described below. A formal definition is provided 
in the [api.yml](./api.yml) file, but the information in this README is sufficient for completion of this challenge. We will use the 
described API to test your solution.

Provide any instructions required to run your application.

Data does not need to persist when your application stops. It is sufficient to store information in memory. There are too many different database solutions, we will not be installing a database on our system when testing your application.

## Project Structure
- `src/`
  - `app.py`: The main Flask application.
  - `utils.py`: Utility functions for validation and points calculation.
- `Dockerfile`: Dockerfile for building the Docker image.
- `requirements.txt`: Python dependencies file.

## Prerequisites
Before you get started, please make sure you have the following installed:
- Docker
- Git

### Installation

1. **Clone the repository**:

   ```bash
   git clone git@github.com:liujiawen0905/receipt-processor-challenge.git
   cd receipt-processor-challenge

2. **Build the Docker image**:

   ```bash
   docker build -t my-app .

1. **Run the Docker container**:

   ```bash
   docker run -p 8000:8000 my-app
