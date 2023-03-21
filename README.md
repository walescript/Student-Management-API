# Student Management API
This API was created with Flask Rest x to enable school administrators to register accounts and manage student data on the PythonAnywhere-powered web app. CRUD operations can be carried out on the student data, with an easy-to-use Swagger UI setup for testing.

## Features
- User registration and login
- Student data management with CRUD operations
- Swagger UI for easy testing
- Limited student access
    * View profile, courses, grades, and CGPA
    * Edit profile information

## Usage

Follow these steps to utilize this API:

1. Launch the PythonAnywhere web app by going to https://walescript.pythonanywhere.com in your browser.

2. Make a student or administrator account:
* To create an admin account, select the '/admin/register' route then register an 'admin' via the selected route.
* To create an student account, select the '/student/register' route then register a 'student' via the selected route.
3. Sign in via the '/auth/login' route to generate a JWT token. This access token should be copied without the quotation marks

4. Navigate upwards to the top right corner and click 'Authorize' to enter the JWT token in the given format
<blockquote>
    Bearer this1is2a3rather4long5hex6string
</blockquote>

5. Select 'Authorize' and then close the authorization window
6. While authorized, you can create, view, update and delete students, courses, grades and admins via the routes seen in 'students', 'courses' and 'admin'. You can also perform the following operations:

* Get all students taking a course
* Get all courses taken by a student
* Get a student's grades in percentage (eg: 70.2%) and grade letters (eg: A)
* Get a student's CGPA, calculated based on all grades from all registered courses

7. When these operations have been completed , navigate upwards to the top right corner and select 'Logout'

In the admin section of the code, comments have been put in place to allow users of the API to determine how the administrator authentication and authorization should be handled. The comments explain that the @admin_required() decorator should be uncommented after registering the first admin. This decorator ensures that only an existing admin can register a new admin account on the app.

Similarly, the @admin_required() decorator is also mentioned in the comments for the get() and put() methods of the GetUpdateDeleteAdmins class, indicating that these endpoints should also only be accessible by existing admins. The comments explain how these methods can be used to retrieve, update, and delete admin accounts by ID, and that only the specific admin associated with the account should have access to these methods.

Overall, these comments serve as a guide to help users of the API understand how administrator authentication and authorization should be implemented in their use of the application.

## Authors
Adewale Babson - babsonadewale@gmail.com

## Acknowledgements
This project was made possible by:

[AltSchool Africa School of Engineering](https://www.altschoolafrica.com/schools/engineering)
