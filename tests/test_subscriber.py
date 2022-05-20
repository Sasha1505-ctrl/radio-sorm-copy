import pytest
from cdr import Subscriber, UserType


@pytest.mark.parametrize(
    "user,types", [("tetra_user", UserType.inner), ("vss_user", UserType.outer)]
)
def test_stuff(user, types, request):
    user_fixture = request.getfixturevalue(user)
    for tupl in user_fixture:
        user, number = tupl
        assert user.get_type() == types
        assert user.get_number() == number
