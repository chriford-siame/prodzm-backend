from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        "view_question_papers": True,
        "upload_question_papers": True,
        "delete_question_papers": True,
        "update_question_papers": True,
        "approve_question_papers": True,
    }
