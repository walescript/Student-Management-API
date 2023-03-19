from flask_restx import Namespace, Resource, fields
from flask import Flask, jsonify, request
from ..models.views import User, Student, Course, Grade, StudentCourse
from ..utils import db, get_letter_grade, convert_grade_to_gpa
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import json

student_namespace = Namespace('students', description='namespace for students')

student_signup_model = student_namespace.model(
    'StudentSignup', {
        'name': fields.String(required=True, description="Student's Name"),
        'username': fields.String(required=True, description="Student's Username"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, description="Student's Temporary Password")
    }
)

student_model = student_namespace.model(
    'Student', {
    'name': fields.String(required=True, description='Student name'),
    'username': fields.String(required=True, description='Student username'),
    'email': fields.String(required=True, description='Student email'),
    'password': fields.String(required=True, description='Student password'),
    'user_type': fields.String(required=True, description="Type of User")
})

grade_model = student_namespace.model(
    'Grade', {
        'id': fields.Integer(description="Grade ID"),
        'course_id': fields.Integer(required=True, description="Course ID"),
        'percent_grade': fields.Float(required=True, description="Grade in Percentage: Number Only")       
    }
)

grade_update_model = student_namespace.model(
    'GradeUpdate', {
        'percent_grade': fields.Float(required=True, description="Grade in Percentage: Number Only")       
    }
)


@student_namespace.route('')
class GetAllStudents(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Retrieve All Students - Admins Only"
    )

    @admin_required()
    def get(self):
        """
            Retrieve All Students - Admins Only
        """
        students = Student.query.all()

        return students, HTTPStatus.OK

@student_namespace.route('/register')
class StudentRegistration(Resource):
    @student_namespace.expect(student_signup_model)
    @admin_required()
    def post(self):
        """
            Register a Student - Admins Only
        """        
        data = student_namespace.payload

        # Check if student already exists
        student = Student.query.filter_by(email=data['email']).first()
        if student:
            return {"message": "Student account already exists"}, HTTPStatus.CONFLICT

        # Register new student
        new_student = Student(
            name = data['name'],
            username = data['username'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            user_type = 'student'
        )

        new_student.save()

        student_resp = {}  
        student_resp['id'] = new_student.id
        student_resp['email'] = new_student.email
        student_resp['name'] = new_student.name
        student_resp['username'] = new_student.username
        student_resp['user_type'] = new_student.user_type
        student_resp['password_hash'] = new_student.password_hash

        return student_resp, HTTPStatus.CREATED

@student_namespace.route('/student/<int:id>')
class GetUpdateDeleteStudents(Resource):
    # @student_namespace.route('/student/<int:id>')
    @student_namespace.doc(
        description = "Retrieve a Student's Details by ID - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        })
    @jwt_required()
    def get(self, id):
        """
            Retrieve a Student's Details by ID - Admins or Specific Student Only
        """
        if Student.query.filter_by(id=id).first():
    # student with the given id exists, so retrieve their details
            student = Student.get_by_id(id)

            student_resp = {}  
            student_resp['id'] = student.id
            student_resp['username'] = student.username
            student_resp['email'] = student.email
            student_resp['name'] = student.name
            student_resp['user_type'] = student.user_type
            student_resp['password_hash'] = new_student.password_hash

            return student_resp, HTTPStatus.OK
        
        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN

    
    @student_namespace.expect(student_signup_model)
    @student_namespace.doc(
        description = "Update a Student's Details by ID - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def put(self, id):
        """
            Update a Student's Details by ID - Admins or Specific Student Only
        """
        if Student.query.filter_by(id=id).first():
    # student with the given id exists, so retrieve their details
            student = Student.get_by_id(id)
            
            data = student_namespace.payload

            student.name = data['name']
            student.username = data['username']
            student.email = data['email']
            student.password_hash = generate_password_hash(data['password'])

            student.update()

            student_resp = {}  
            student_resp['id'] = student.id
            student_resp['username'] = student.username
            student_resp['email'] = student.email
            student_resp['name'] = student.name
            student_resp['user_type'] = student.user_type
            student_resp['password_hash'] = new_student.password_hash

            return student_resp, HTTPStatus.OK

        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN
    
    @student_namespace.doc(
        description = 'Delete a Student by ID',
        params = {
            'student_id': "The Student's ID"
        }
    )

    @admin_required()
    def delete(self, id):
        """
            Delete a Student by ID - Admins Only
        """
        student = Student.get_by_id(id)

        student.delete()

        return {"message": "Student Successfully Deleted"}, HTTPStatus.OK

@student_namespace.route('/student/<int:id>/courses')
# /student/<int:id>
class GetStudentCourses(Resource):

    @student_namespace.doc(
        description = "Retrieve a Student's Courses - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self, id):
        """
            Retrieve a Student's Courses - Admins or Specific Student Only
        """
        if Student.query.filter_by(id=id).first():
    # student with the given id exists, so retrieve their details
            courses = StudentCourse.get_courses_by_student(id)
            resp = []

            for course in courses:
                course_resp = {}
                course_resp['id'] = course.id
                course_resp['name'] = course.name
                course_resp['teacher'] = course.teacher

                resp.append(course_resp)

            return resp, HTTPStatus.OK
    
        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN

@student_namespace.route('/student/<int:id>/grades')
class GetAddUpdateGrades(Resource):

    @student_namespace.doc(
        description = "Retrieve a Student's Grades - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self, id):
        """
            Retrieve a Student's Grades - Admins or Specific Student Only
        """
        if Student.query.filter_by(id=id).first():
    # student with the given id exists, so retrieve their details
            student = Student.get_by_id(id)
            if not student:
                return {"message": "Student Not Found"}, HTTPStatus.NOT_FOUND
            
            # Retrieve the student's grades        
            courses = StudentCourse.get_courses_by_student(id)
            resp = []

            for course in courses:
                grade_resp = {}
                grade_in_course = Grade.query.filter_by(
                        student_id=id, course_id=course.id
                    ).first()
                grade_resp['course_name'] = course.name

                if grade_in_course:
                    grade_resp['grade_id'] = grade_in_course.id
                    grade_resp['percent_grade'] = grade_in_course.percent_grade
                    grade_resp['letter_grade'] = grade_in_course.letter_grade
                else:
                    grade_resp['percent_grade'] = None
                    grade_resp['letter_grade'] = None
                
                resp.append(grade_resp)
            
            return resp, HTTPStatus.OK
        
        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN
        
    @student_namespace.expect(grade_model)
    @student_namespace.doc(
        description = "Upload a Student's Grade in a Course - Admins Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @admin_required()
    def post(self, id):
        """
        Upload a Student's Grade in a Course - Admins Only
        """
        data = student_namespace.payload

        student = Student.get_by_id(id)
        course = Course.get_by_id(id=data['course_id'])
            
        # Confirm that the student is taking the course
        student_course = StudentCourse.query.filter_by(student_id=id, course_id=course.id).first()
        if not student_course:
            return {"message": f"{student.name} is not taking {course.name}"}, HTTPStatus.NOT_FOUND

        # Confirm that the course_id specified in the payload corresponds to a course that the student is taking
        student_courses = StudentCourse.get_courses_by_student(id)
        if course not in student_courses:
            return {"message": f"{student.name} is not taking {course.name}"}, HTTPStatus.NOT_FOUND
            
        # Add a new grade
        new_grade = Grade(
            student_id=id,
            course_id=data['course_id'],
            percent_grade=data['percent_grade'],
            letter_grade=get_letter_grade(data['percent_grade'])
        )

        new_grade.save()

        grade_resp = {}
        grade_resp['grade_id'] = new_grade.id
        grade_resp['student_id'] = new_grade.id
        grade_resp['course_id'] = new_grade.course_id
        grade_resp['course_name'] = course.name
        grade_resp['course_teacher'] = course.teacher
        grade_resp['percent_grade'] = new_grade.percent_grade
        grade_resp['letter_grade'] = new_grade.letter_grade

        return grade_resp, HTTPStatus.CREATED

    

@student_namespace.route('/grades/<int:grade_id>')
class UpdateDeleteGrade(Resource):

    @student_namespace.expect(grade_update_model)
    @student_namespace.doc(
        description = "Update a Grade - Admins Only",
        params = {
            'grade_id': "The Grade's ID"
        }
    )
    @admin_required()
    def put(self, grade_id):
        """
            Update a Grade - Admins Only
        """
        data = student_namespace.payload

        grade = Grade.get_by_id(grade_id)
        
        grade.percent_grade = data['percent_grade']
        grade.letter_grade = get_letter_grade(data['percent_grade'])
        
        grade.update()

        grade_resp = {}
        grade_resp['grade_id'] = grade.id
        grade_resp['student_id'] = grade.id
        grade_resp['course_id'] = grade.course_id
        grade_resp['percent_grade'] = grade.percent_grade
        grade_resp['letter_grade'] = grade.letter_grade

        return grade_resp, HTTPStatus.OK
    
    @student_namespace.doc(
        description = "Delete a Grade - Admins Only",
        params = {
            'grade_id': "The Grade's ID"
        }
    )
    @admin_required()
    def delete(self, grade_id):
        """
            Delete a Grade - Admins Only
        """
        grade = Grade.get_by_id(grade_id)
        
        grade.delete()

        return {"message": "Grade Successfully Deleted"}, HTTPStatus.OK
        
    
@student_namespace.route('/<int:id>/cgpa')
class GetStudentCGPA(Resource):

    @student_namespace.doc(
        description = "Calculate a Student's CGPA - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self, id):
        """
            Calculate a Student's CGPA - Admins or Specific Student Only
        """
        if Student.query.filter_by(id=id).first():
    # student with the given id exists, so retrieve their details
            student = Student.get_by_id(id)
            
            courses = StudentCourse.get_courses_by_student(id)
            total_gpa = 0
            
            for course in courses:
                grade = Grade.query.filter_by(
                        student_id=id, course_id=course.id
                    ).first()
                
                if grade:
                    letter_grade = grade.letter_grade
                    gpa = convert_grade_to_gpa(letter_grade)
                    total_gpa += gpa
                
            cgpa = total_gpa / len(courses)
            round_cgpa = float("{:.2f}".format(cgpa))

            return {"message": f"{student.name}'s CGPA is {round_cgpa}"}, HTTPStatus.OK
    
        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN