# FastAPI App

## Overview

A FastAPI application designed for item prioritization and data analysis. This application includes endpoints for retrieving items by stage, predicting stages based on input data, and calculating percentages and frequencies of attributes.

## Features

- **Get Items by Stage**: Retrieve items based on their priority stage.
- **Predict Stage**: Predict the stage of items using a machine learning model.
- **Show Percentages**: Calculate and show the percentage of items for a given attribute.

## Getting Started

### Prerequisites

- Python 3.10.1
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/daxermanGit/hailcoto-back-data.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd your-repository
   ```

3. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API**:
   - Open your browser and go to [http://localhost:8000/item/](http://localhost:8000/item/) to see the FastAPI app in action.
   - Visit [http://localhost:8000/item/docs](http://localhost:8000/item/docs) for the interactive Swagger documentation.

## API Endpoints

### **1. Get Items by Stage**

- **Endpoint**: `POST /item/items_per_priorities/`
- **Description**: Retrieve items based on their priority stage.
- **Request Body**:
  ```json
  [1, 2, 3]
  ```
  This is a list of integer stages you want to filter by.

- **Response**:
  ```json
  {
    "body": [
      {"id": 1, "name": "Item 1", "expiresAt": "2024-12-31", "price": 19.99, "weight": "1kg", "packagingUnit": "Box", "available": 10, "SalesRateDay": 5.0},
      {"id": 2, "name": "Item 2", "expiresAt": "2024-11-30", "price": 29.99, "weight": "2kg", "packagingUnit": "Bag", "available": 5, "SalesRateDay": 3.0}
    ]
  }
  ```

### **2. Predict Stage**

- **Endpoint**: `POST /item/predict_stage/`
- **Description**: Predict the stage of items based on provided data.
- **Request Body**:
  ```json
  [
    {
      "id": 1,
      "name": "Item 1",
      "expiresAt": "2024-12-31",
      "price": 19.99,
      "weight": "1kg",
      "packagingUnit": "Box",
      "available": 10,
      "SalesRateDay": 5.0
    },
    {
      "id": 2,
      "name": "Item 2",
      "expiresAt": "2024-11-30",
      "price": 29.99,
      "weight": "2kg",
      "packagingUnit": "Bag",
      "available": 5,
      "SalesRateDay": 3.0
    }
  ]
  ```

- **Response**:
  ```json
  {
    "body": "Predicted stages: [1, 2]"
  }
  ```

### **3. Show Percentages**

- **Endpoint**: `GET /item/percentage/{atribute}`
- **Description**: Calculate and show the percentage of items for a given attribute.
- **Path Parameter**: `atribute` - The attribute to analyze (e.g., "priority").
  - Example: `priority`

- **Response**:
  ```json
  {
    "frequency": {"priority1": 50, "priority2": 30, "priority3": 20},
    "percentage": {"priority1": 50.0, "priority2": 30.0, "priority3": 20.0}
  }
  ```
## Contributing

Guidelines for contributing to the project.

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature-branch
   ```
3. **Make your changes**.
4. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature-branch
   ```
5. **Open a pull request**.

## License

Include licensing information if applicable.
```

You can copy this Markdown content into your `README.md` file. If you need more adjustments or details, just let me know!
