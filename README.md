# AI Safety Incident Log API

A simple RESTful API service to log and manage hypothetical AI safety incidents, with a web-based user interface.

## Technology Stack

- **Language**: Python
- **Framework**: Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript

## Setup Instructions

### Prerequisites

- Python 3.8+ installed
- pip package manager
- MySQL installed and running

<h3>🎥 Project Demo</h3>

<p align="center">
  <a href="https://drive.google.com/file/d/YOUR_VIDEO_ID/view?usp=sharing" target="_blank">
    <img src="https://img.youtube.com/vi/your_video_id/0.jpg" alt="Watch the video" width="60%">
    <!-- Note: You'll need to provide your own thumbnail image -->
  </a>
</p>

<p align="center">
  <a href="https://drive.google.com/file/d/YOUR_VIDEO_ID/view?usp=sharing" target="_blank">▶️ Click here to watch the demo video</a>
</p>

### ScreenShots

## login_page
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/login_page.png)

## incidents_api_response
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/incidents_api_response.png)

## single_incident_api_response
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/single_incident_api_response.png)

## post_request_image
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/post_request_image.png)

## database_schema
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/database_schema.png)

## delete_incident
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/delete_incident.png)

## project setup
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/project_setup.png)

## project structure
![API Error Responses](https://github.com/danthulurisaihemanth/HumanChain-AI-Safety-Incident-Log-API/blob/master/images/project_structure.png)


### Installation

1. Clone this repository or unzip the project files.

```bash
git clone https://github.com/yourusername/ai-safety-incident-log.git
```

2. Navigate to the project directory:

```bash
cd ai-safety-incident-log
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install flask flask-cors mysql-connector-python
```

### Project Structure

Make sure your project has the following structure:

```
project_directory/
├── app.py
├── README.md
├── static/
│   └── styles.css
└── templates/
    └── index.html
```

If the `static` and `templates` directories don't exist, the application will create them automatically when run.

### Database Setup

1. Install MySQL if not already installed
2. Create a MySQL database named `ai_safety_incidents`
3. Update the database configuration in `app.py` with your MySQL credentials:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'ai_safety_incidents'
   }
   ```
4. The database tables will be automatically created and populated with sample incidents when you first run the application

### Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

This will display the user interface where you can view, add, and delete incidents.

## API Endpoints

### 1. Get All Incidents

**Request**:
```
GET /incidents
```

**Example using curl**:

```bash
curl -X GET http://localhost:5000/incidents
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Unauthorized Data Access",
    "description": "AI system accessed restricted database without permission",
    "severity": "High",
    "reported_at": "2025-04-02T18:00:00Z"
  },
  {
    "id": 2,
    "title": "False Prediction",
    "description": "ML model produced false positives in critical medical diagnoses",
    "severity": "Medium",
    "reported_at": "2025-04-02T18:00:00Z"
  },
  {
    "id": 3,
    "title": "UI Confusion",
    "description": "Users misinterpreted AI recommendations due to unclear interface",
    "severity": "Low",
    "reported_at": "2025-04-02T18:00:00Z"
  }
]
```

### 2. Create New Incident

**Request**:
```
POST /incidents
Content-Type: application/json

{
  "title": "New Incident Title",
  "description": "Detailed description here.",
  "severity": "Medium"
}
```

**Example using curl**:
```bash
curl -X POST http://localhost:5000/incidents \
  -H "Content-Type: application/json" \
  -d '{"title": "New Incident Title", "description": "Detailed description here.", "severity": "Medium"}'
```

**Response** (201 Created):
```json
{
  "id": 4,
  "title": "New Incident Title",
  "description": "Detailed description here.",
  "severity": "Medium",
  "reported_at": "2025-04-02T18:00:00Z"
}
```

### 3. Get Specific Incident

**Request**:
```
GET /incidents/{id}
```

**Example using curl**:
```bash
curl -X GET http://localhost:5000/incidents/1
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Unauthorized Data Access",
  "description": "AI system accessed restricted database without permission",
  "severity": "High",
  "reported_at": "2025-04-02T18:00:00Z"
}
```

**Response** (404 Not Found):
```json
{
  "error": "Incident not found"
}
```

### 4. Delete Incident

**Request**:
```
DELETE /incidents/{id}
```

**Example using curl**:
```bash
curl -X DELETE http://localhost:5000/incidents/1
```

**Response** (200 OK):
```json
{
  "message": "Incident 1 deleted successfully"
}
```

**Response** (404 Not Found):
```json
{
  "error": "Incident not found"
}
```

## Web User Interface

The application includes a simple web interface that allows you to:

1. View all reported incidents
2. Add new incidents through a form
3. Delete existing incidents

The UI is styled with CSS and provides a responsive design that works on both desktop and mobile devices.

## Design Decisions

1. **MySQL Database**: Chosen for its reliability and widespread use in production environments. The database is automatically initialized with the required tables and sample data when the application first runs.

2. **Data Validation**: Basic validation is implemented to ensure required fields are provided and severity values are valid. Default values are set for missing fields.

3. **Error Handling**: The API returns appropriate HTTP status codes and error messages for various scenarios, including database connection failures.

4. **UTC Timestamps**: All timestamps are stored and returned in UTC format for consistency across different time zones.

5. **Simple Frontend**: Added a clean, responsive UI to make testing and interacting with the API easier without requiring external tools like Postman.

6. **CORS Support**: Added Flask-CORS to enable cross-origin requests, which allows the API to be used from different domains if needed.

## Future Improvements

1. Add user authentication and authorization
2. Implement pagination for large numbers of incidents
3. Add search and filtering capabilities
4. Implement data export functionality (CSV, JSON)
5. Add more detailed statistics and reporting features

## License
This project is licensed under the MIT License.

## Author
Developed by D. Sai Hemanth Varma


