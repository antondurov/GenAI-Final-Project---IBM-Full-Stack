"""
CodeCraftHub - A Simple Learning Platform API
==============================================

This is a beginner-friendly REST API built with Flask.
It demonstrates CRUD operations (Create, Read, Update, Delete)
using a JSON file for data storage instead of a database.

Author: CodeCraftHub Tutorial
Python Version: 3.8+
"""

# ============================================================
# IMPORTS
# ============================================================

from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

# ============================================================
# FLASK APP CONFIGURATION
# ============================================================

# Create a Flask application instance
# __name__ tells Flask where to look for resources
app = Flask(__name__)

# Name of our JSON file that stores all course data
JSON_FILE = 'courses.json'

# Valid status values for a course
# We'll use this list to validate user input
VALID_STATUSES = ['Not Started', 'In Progress', 'Completed']


# ============================================================
# JSON FILE OPERATIONS
# These functions handle reading and writing to our JSON file
# ============================================================

def load_courses():
    """
    Load all courses from the JSON file.
    
    This function:
    1. Checks if the JSON file exists
    2. If not, creates a new file with empty data
    3. If yes, reads and returns the data
    
    Returns:
        dict: A dictionary containing:
            - 'courses': list of all course dictionaries
            - 'next_id': the next available ID for a new course
    
    Example of returned data:
        {
            "courses": [
                {"id": 1, "name": "Python", ...},
                {"id": 2, "name": "Flask", ...}
            ],
            "next_id": 3
        }
    """
    # Check if our data file exists
    if not os.path.exists(JSON_FILE):
        # File doesn't exist, create initial empty structure
        initial_data = {
            "courses": [],    # Empty list to store courses
            "next_id": 1      # First course will have ID 1
        }
        # Save this initial structure to create the file
        save_courses(initial_data)
        print(f"Created new file: {JSON_FILE}")
        return initial_data
    
    # File exists, try to read it
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Parse JSON into Python dict
            return data
    except json.JSONDecodeError as e:
        # File exists but contains invalid JSON
        print(f"Error reading JSON file: {e}")
        # Return empty structure to prevent crashes
        return {"courses": [], "next_id": 1}
    except IOError as e:
        # File system error (permissions, etc.)
        print(f"Error accessing file: {e}")
        return {"courses": [], "next_id": 1}


def save_courses(data):
    """
    Save course data to the JSON file.
    
    Args:
        data (dict): The complete data structure to save
    
    Returns:
        bool: True if successful, False if error occurred
    
    The JSON file is formatted with:
    - indent=4: Makes the file human-readable with 4-space indentation
    - ensure_ascii=False: Allows non-English characters
    """
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        # Handle file writing errors
        print(f"Error saving to file: {e}")
        return False


def find_course_by_id(courses, course_id):
    """
    Find a specific course by its ID.
    
    Args:
        courses (list): List of all course dictionaries
        course_id (int): The ID we're looking for
    
    Returns:
        tuple: (course, index)
            - course: The course dictionary if found, None if not
            - index: Position in the list
    """
    for index, course in enumerate(courses):
        if course['id'] == course_id:
            return course, index
    return None, None


# ============================================================
# API ROUTES
# ============================================================

@app.route('/', methods=['GET'])
def home():
    """Welcome endpoint - returns API information"""
    return jsonify({
        'message': 'Welcome to CodeCraftHub API',
        'version': '1.0',
        'endpoints': {
            'GET /': 'This welcome message',
            'GET /api/courses': 'Get all courses',
            'POST /api/courses': 'Create a new course',
            'GET /api/courses/<id>': 'Get a specific course',
            'PUT /api/courses/<id>': 'Update a course',
            'DELETE /api/courses/<id>': 'Delete a course'
        }
    }), 200


@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """Get all courses from the system"""
    data = load_courses()
    return jsonify({
        'total': len(data['courses']),
        'courses': data['courses']
    }), 200


@app.route('/api/courses', methods=['POST'])
def create_course():
    """Create a new course"""
    data = load_courses()
    
    # Get JSON data from request
    request_data = request.get_json()
    
    # Validate required fields
    if not request_data or 'name' not in request_data:
        return jsonify({'error': 'Course name is required'}), 400
    
    # Create new course object
    new_course = {
        'id': data['next_id'],
        'name': request_data.get('name'),
        'description': request_data.get('description', ''),
        'status': request_data.get('status', 'Not Started'),
        'created_at': datetime.now().isoformat()
    }
    
    # Validate status
    if new_course['status'] not in VALID_STATUSES:
        return jsonify({'error': f'Status must be one of: {VALID_STATUSES}'}), 400
    
    # Add to courses list
    data['courses'].append(new_course)
    data['next_id'] += 1
    
    # Save and return
    if save_courses(data):
        return jsonify(new_course), 201
    else:
        return jsonify({'error': 'Failed to save course'}), 500


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by ID"""
    data = load_courses()
    course, _ = find_course_by_id(data['courses'], course_id)
    
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    
    return jsonify(course), 200


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Update a course"""
    data = load_courses()
    course, index = find_course_by_id(data['courses'], course_id)
    
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    
    request_data = request.get_json()
    
    # Update fields if provided
    if 'name' in request_data:
        course['name'] = request_data['name']
    if 'description' in request_data:
        course['description'] = request_data['description']
    if 'status' in request_data:
        if request_data['status'] not in VALID_STATUSES:
            return jsonify({'error': f'Status must be one of: {VALID_STATUSES}'}), 400
        course['status'] = request_data['status']
    
    course['updated_at'] = datetime.now().isoformat()
    
    # Save and return
    if save_courses(data):
        return jsonify(course), 200
    else:
        return jsonify({'error': 'Failed to save course'}), 500


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete a course"""
    data = load_courses()
    course, index = find_course_by_id(data['courses'], course_id)
    
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    
    # Remove the course
    deleted_course = data['courses'].pop(index)
    
    # Save and return
    if save_courses(data):
        return jsonify({'message': 'Course deleted', 'course': deleted_course}), 200
    else:
        return jsonify({'error': 'Failed to delete course'}), 500


@app.route('/api/courses/stats', methods=['GET'])
def get_course_stats():
    """Get statistics about all courses"""
    data = load_courses()
    courses = data['courses']

    # Count courses per status
    status_counts = {status: 0 for status in VALID_STATUSES}
    for course in courses:
        status = course.get('status', 'Not Started')
        if status in status_counts:
            status_counts[status] += 1

    return jsonify({
        'total': len(courses),
        'by_status': status_counts
    }), 200

# ============================================================
# RUN THE APP
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
