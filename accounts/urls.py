from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    RegistrationView,
    VerificationView,
    UsernameValidationView,
    EmailValidationView,
    AdminLoginView,
    FrontLoginView,
    LogoutView,
    AddUserView,
    EditUserView,
    ListUsersView,
    DeleteUserView,
    ConnectedUsersView,
    ChangeUserPasswordView,
    SetNewPasswordView,
    ResetCodeView,
    ResetPasswordWithCodeView,


    ListRolesView,
    RoleFormView,
    DeleteRoleView,

    # GROUPES
    ListGroupsView,
    GroupFormView,
    DeleteGroupView,

     # MODULES
    ListModulesView,
    ModuleFormView,
    DeleteModuleView,

    # TABLEAU DE BORD (namespace 'administration' -> monté sur ce même
    # urls.py depuis config/urls.py, il n'y a pas de administration/urls.py)
    AdministrationIndexView,
)

app_name = "accounts"

urlpatterns = [
    # ==================================================
    # TABLEAU DE BORD
    # ==================================================
    path("", AdministrationIndexView.as_view(), name="index"),

    # ==================================================
    # FRONT-END
    # ==================================================
    path("front/register/", RegistrationView.as_view(), name="front_register"),
    path("front/login/", FrontLoginView.as_view(), name="front_login"),
    path("front/logout/", LogoutView.as_view(), name="front_logout"),

    # ==================================================
    # ADMIN
    # ==================================================
    path("register/", RegistrationView.as_view(), name="admin_register"),
    path("login/", AdminLoginView.as_view(), name="admin_login"),
    path("logout/", LogoutView.as_view(), name="admin_logout"),

    # ==================================================
    # ACTIVATION COMPTE
    # ==================================================
    path("activate/<uidb64>/<token>/", VerificationView.as_view(), name="activate"),

    # ==================================================
    # VALIDATION AJAX
    # ==================================================
    path("validate-username/", csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path("validate-email/", csrf_exempt(EmailValidationView.as_view()), name="validate-email"),

    # ==================================================
    # GESTION DES UTILISATEURS
    # ==================================================
    path("add_user/", AddUserView.as_view(), name="add_user"),
    path("edit-user/<int:user_id>/", EditUserView.as_view(), name="edit_user"),
    path("list-users/", ListUsersView.as_view(), name="list_users"),
    path("delete-user/<int:user_id>/", DeleteUserView.as_view(), name="delete_user"),
    path("connected-users/", ConnectedUsersView.as_view(), name="connected_users"),

    # ==================================================
    # MOT DE PASSE
    # ==================================================
    path("change-password/<int:user_id>/", ChangeUserPasswordView.as_view(), name="change_user_password"),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set_new_password"),
    path("request-reset-code/", ResetCodeView.as_view(), name="request_reset_code"),
    path("reset-password/<int:user_id>/", ResetPasswordWithCodeView.as_view(), name="reset_code_verify"),

    # ==================================================
    # RÔLES & PERMISSIONS
    # ==================================================
    path("roles/", ListRolesView.as_view(), name="list_roles"),
    path("roles/add/", RoleFormView.as_view(), name="add_role"),
    path("roles/<int:role_id>/edit/", RoleFormView.as_view(), name="edit_role"),
    path("roles/<int:role_id>/delete/", DeleteRoleView.as_view(), name="delete_role"),


    # =========================================================
    # GROUPES
    # =========================================================

    path(
        "groups/",
        ListGroupsView.as_view(),
        name="list_groups",
    ),

    path(
        "groups/add/",
        GroupFormView.as_view(),
        name="add_group",
    ),

    path(
        "groups/<int:group_id>/edit/",
        GroupFormView.as_view(),
        name="edit_group",
    ),

    path(
        "groups/<int:group_id>/delete/",
        DeleteGroupView.as_view(),
        name="delete_group",
    ),


    # =========================================================
    # MODULES
    # =========================================================

    path(
        "modules/",
        ListModulesView.as_view(),
        name="list_modules",
    ),

    path(
        "modules/add/",
        ModuleFormView.as_view(),
        name="add_module",
    ),

    path(
        "modules/<int:module_id>/edit/",
        ModuleFormView.as_view(),
        name="edit_module",
    ),

    path(
        "modules/<int:module_id>/delete/",
        DeleteModuleView.as_view(),
        name="delete_module",
    ),
]