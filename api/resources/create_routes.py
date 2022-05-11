from .authentication import (RegisterApi, LoginApi, IndexApi, LogoutApi, RefreshToken, DataUser, DataAdmin,
                             DataSuperAdmin, AdminApi, UserMetrics)
from .resource_manager import (ManageMajor, ManageEducation, ManageDepartment)
from .mailer import (MailStudent, MailSupervisor)
from flask_restful import Api


# Add API resources
def initialize_routes(api_instance):
    # initialize all the api resources
    api = Api(api_instance)
    # Authorization Apis
    api.add_resource(IndexApi, "/usiu-research/api/v1.0/", endpoint='home')
    api.add_resource(RegisterApi, '/usiu-research/api/v1.0/register', endpoint='register_user')
    api.add_resource(LoginApi, '/usiu-research/api/v1.0/login', endpoint='login_user')
    api.add_resource(LogoutApi, '/usiu-research/api/v1.0/logout', endpoint='logout_user')
    api.add_resource(RefreshToken, '/usiu-research/api/v1.0/refresh_token', endpoint='refresh_token')

    # Managing users Apis
    api.add_resource(DataUser, '/usiu-research/api/v1.0/data_user', endpoint='get_user')
    api.add_resource(DataAdmin, '/usiu-research/api/v1.0/data_admin', endpoint='admin_user')
    api.add_resource(DataSuperAdmin, '/usiu-research/api/v1.0/data_super_admin', endpoint='super_user')
    api.add_resource(UserMetrics, '/usiu-research/api/v1.0/metrics', endpoint='user_metrics')
    api.add_resource(AdminApi, '/usiu-research/api/v1.0/admin',  endpoint='admin')

    # Communication/Mailing Apis
    api.add_resource(MailStudent, '/usiu-research/api/v1.0/mail_student',  endpoint='mail_student')
    api.add_resource(MailSupervisor, '/usiu-research/api/v1.0/mail_supervisor', endpoint='mail_supervisor')

    # Manage resources Apis
    api.add_resource(ManageMajor, '/usiu-research/api/v1.0/major',  endpoint='major')
    api.add_resource(ManageEducation, '/usiu-research/api/v1.0/education',  endpoint='education')
    api.add_resource(ManageDepartment, '/usiu-research/api/v1.0/department',  endpoint='department')
