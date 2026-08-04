"""Who may do what. Authentication answers WHO; these classes answer MAY THEY.

Roles are Django Groups -- named sets of users, managed in the admin with
zero extra code.
"""

from rest_framework.permissions import BasePermission


class IsAccountManager(BasePermission):
    """Running the matcher proposes people to clients -- a business decision.

    Recruiters and specialists can look; only account managers can act.
    """

    message = "Only account managers can propose candidates."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Account Managers").exists()
