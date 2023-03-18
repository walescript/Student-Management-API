from ..utils import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False, default='user')
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.String, default='user', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': is_admin
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', secondary='student_courses')
    grades = db.relationship('Grade', backref='student', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', secondary='student_courses')
    grades = db.relationship('Grade', backref='course', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_courses_by_student(cls, id):
        courses = Course.query.join(cls).join(Student).filter(Student.id == id).all()
        return courses
    
    @classmethod
    def get_students_in_course(cls, course_id):
        students = Student.query.join(cls).join(Course).filter(Course.id == course_id).all()
        return students

    # @classmethod
    # def get_courses_by_student(cls, id):
    #     courses = Course.query.join(StudentCourse).join(Student).filter(Student.id == id).all()
    #     return courses
    
    # @classmethod
    # def get_students_in_course(cls, course_id):
    #     students = Student.query.join(StudentCourse).join(Course).filter(Course.id == course_id).all()
    #     return students


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    percent_grade = db.Column(db.Float(), nullable=False)
    letter_grade = db.Column(db.String(5), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)



# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer(), primary_key=True)
#     username = db.Column(db.String(45), nullable=False, unique=True)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     password_hash = db.Column(db.Text(), nullable=False)
#     is_admin = db.Column(db.Boolean(), default=False)
#     is_active = db.Column(db.Boolean(), default=False)
#     courses = db.relationship('Course', backref='user', lazy=True)
#     students = db.relationship('Student', backref='user', lazy=True)
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()


#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)

    

# class Course(db.Model):
#     __tablename__ = 'courses'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     teacher = db.Column(db.String(50), nullable=False)
#     credit_hours = db.Column(db.Integer(), nullable=False)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     students = db.relationship('Student', backref='course', lazy=True)
#     grades = db.relationship('Grade', backref='course', lazy=True)

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)

    

# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
#     course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=True)
#     grades = db.relationship('Grade', backref='student', lazy=True)

#     __table_args__ = (
#         CheckConstraint('course_id is null or course_id in (select id from courses)', name='valid_course_id'),
#     )

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)

    

# class Grade(db.Model):
#     __tablename__ = 'grades'
#     id = db.Column(db.Integer(), primary_key=True)
#     course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=False)
#     student_id = db.Column(db.Integer(), db.ForeignKey('students.id'), nullable=False)
#     score = db.Column(db.Float())

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)


