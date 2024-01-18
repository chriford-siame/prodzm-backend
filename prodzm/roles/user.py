from rolepermissions.roles import AbstractUserRole


class User(AbstractUserRole):
    available_permissions = {
        "view_question_papers": True,
    }
