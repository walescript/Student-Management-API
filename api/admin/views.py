from flask_restx import Namespace, Resource, fields
from ..models.views import Admin
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity


admin_namespace = Namespace('admin', description='Namespace for Administrators')

admin_signup_model = admin_namespace.model(
    'AdminSignUp', {
    'username': fields.String(required=True, description='Admin username'),
    'email': fields.String(required=True, description='Admin email'),
    'password': fields.String(required=True, description='Admin password'),
    'name': fields.String(required=True, description='Admin name'),
})

admin_model = admin_namespace.model(
    'Admin', {
    'id': fields.Integer(description="Admin's User ID"),
    'username': fields.String(required=True, description='Admin username'),
    'email': fields.String(required=True, description='Admin email'),
    'name': fields.String(required=True, description='Admin name'),
})

@admin_namespace.route('')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Retrieve All Admins - Admins Only"
    )

    def get(self):
        """
            Retrieve All Admins - Admins Only
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK

@admin_namespace.route('/register')
class AdminRegistration(Resource):

    @admin_namespace.expect(admin_signup_model)
    # Uncomment the @admin_required() decorator below after registering the first admin
    # This ensures that only an existing admin can register a new admin account on the app
    # @admin_required()
    @admin_namespace.doc(
        description = "Register an Admin - Admins Only, after First Admin"
    )
    def post(self):
        """
            Register an Admin - Admins Only, after First Admin
        """        
        data = admin_namespace.payload

        # Check if the admin account already exists
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin:
            return {"message": "Admin Account Already Exists"}, HTTPStatus.CONFLICT

        # Register new admin
        new_admin = Admin(
            username = data['username'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            name = data['name']
        )

        new_admin.save()

        admin_resp = {}
        admin_resp['id'] = new_admin.id
        admin_resp['username'] = new_admin.username
        admin_resp['email'] = new_admin.email
        admin_resp['name'] = new_admin.name

        return admin_resp, HTTPStatus.CREATED
