from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS  # Import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import json


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'hemanth',  # Your MySQL password
    'database': 'ai_safety_incidents'  # The database you want to connect to
}

# Create MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Initialize the database
def initialize_database():
    try:
        # First connect without specifying database
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        conn.commit()
        
        # Switch to the database
        cursor.execute(f"USE {db_config['database']}")
        
        # Create incidents table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS incidents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                severity VARCHAR(20) NOT NULL,
                reported_at DATETIME NOT NULL
            )
        ''')
        conn.commit()
        
        # Check if table is empty and add sample data
        cursor.execute("SELECT COUNT(*) FROM incidents")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Add sample incidents
            sample_incidents = [
                {
                    "title": "Unauthorized Data Access",
                    "description": "AI system accessed restricted database without permission",
                    "severity": "High",
                    "reported_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    "title": "False Prediction",
                    "description": "ML model produced false positives in critical medical diagnoses",
                    "severity": "Medium",
                    "reported_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    "title": "UI Confusion",
                    "description": "Users misinterpreted AI recommendations due to unclear interface",
                    "severity": "Low",
                    "reported_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
            
            for incident in sample_incidents:
                cursor.execute(''' 
                    INSERT INTO incidents (title, description, severity, reported_at)
                    VALUES (%s, %s, %s, %s)
                ''', (incident["title"], incident["description"], incident["severity"], incident["reported_at"]))
            
            conn.commit()
            print("Sample incidents added!")
        
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Error as e:
        print(f"Error initializing database: {e}")

# Ensure static directory exists
def ensure_static_dir():
    for directory in ['static', 'templates']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{directory} directory created!")

# Convert MySQL rows to dictionaries
def row_to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

# Validation function for incident data
def validate_incident_data(data):
    # Set default values for missing fields
    if 'severity' not in data or data['severity'] not in ['Low', 'Medium', 'High']:
        data['severity'] = 'Medium'  # Default to Medium severity
    if 'title' not in data or not data['title']:
        data['title'] = 'Untitled Incident'  # Default title
    if 'description' not in data or not data['description']:
        data['description'] = 'No description provided'  # Default description
    return data

# Format the incident data in the desired key order
def format_incident_data(incident):
    return {
        "id": incident["id"],
        "title": incident["title"],
        "description": incident["description"],
        "severity": incident["severity"],
        "reported_at": incident["reported_at"].isoformat() + 'Z'
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/incidents', methods=['GET'])
def get_all_incidents():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
        incidents = cursor.fetchall()
        
        # Format datetime objects
        formatted_incidents = [format_incident_data(incident) for incident in incidents]
        
        cursor.close()
        conn.close()
        
        # Ensure we're returning a list even if empty
        if incidents is None:
            incidents = []
            
        return jsonify(formatted_incidents), 200
    except Error as e:
        print(f"Error fetching incidents: {e}")
        return jsonify({"error": "Failed to fetch incidents"}), 500

@app.route('/incidents', methods=['POST'])
def create_incident():
    try:
        data = request.json
        
        # Validate and set default values
        data = validate_incident_data(data)
        
        # Get current timestamp
        reported_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO incidents (title, description, severity, reported_at)
            VALUES (%s, %s, %s, %s)
        ''', (data['title'], data['description'], data['severity'], reported_at))
        
        conn.commit()
        new_incident_id = cursor.lastrowid
        
        # Fetch the newly created incident
        cursor.execute("SELECT * FROM incidents WHERE id = %s", (new_incident_id,))
        new_incident = cursor.fetchone()
        
        # Format datetime
        new_incident = format_incident_data(new_incident)
        
        cursor.close()
        conn.close()
        
        return jsonify(new_incident), 201
    except Error as e:
        print(f"Error creating incident: {e}")
        return jsonify({"error": "Failed to create incident"}), 500

@app.route('/incidents/<int:id>', methods=['GET'])
def get_incident(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM incidents WHERE id = %s", (id,))
        incident = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if incident is None:
            return jsonify({"error": "Incident not found"}), 404
        
        # Format datetime
        incident = format_incident_data(incident)
        
        return jsonify(incident), 200
    except Error as e:
        print(f"Error fetching incident: {e}")
        return jsonify({"error": "Failed to fetch incident"}), 500

@app.route('/incidents/<int:id>', methods=['DELETE'])
def delete_incident(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        
        # Check if incident exists
        cursor.execute("SELECT COUNT(*) FROM incidents WHERE id = %s", (id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Incident not found"}), 404
        
        # Delete the incident
        cursor.execute("DELETE FROM incidents WHERE id = %s", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"message": f"Incident {id} deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting incident: {e}")
        return jsonify({"error": "Failed to delete incident"}), 500


if __name__ == '__main__':
    ensure_static_dir()
    initialize_database()
    app.run(debug=True)
