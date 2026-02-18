from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import Users


class CustomAuthentication(BaseAuthentication):
    """
    Custom authentication to use the user set by the middleware
    based on the 'X-USER-ID' header.
    """

    def authenticate(self, request):
        user_id = request.headers.get('X-USER-ID')

        if not user_id:
            raise AuthenticationFailed(
                "Authentication creadentials were not provided.")
        try:
            user = Users.objects.get(id=user_id)
        except Exception as e:
            raise AuthenticationFailed("Invalid User")

        request.user = user
        return (user, None)
