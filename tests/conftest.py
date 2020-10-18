import pytest
from sorm.cdr import Subscriber, UserType

@pytest.fixture()
def tetra_user():
    return [
        (Subscriber(UserType.inner, '102025000075780046ff', 501, 501), '75780046'),
        (Subscriber(UserType.inner, '0e20250000755995ffffffffff', 65535, 65535), '75785995'),
        (Subscriber(UserType.inner, '102025000075782418ffffffffff', 506, 65535), '75782418'),
    ]

         
@pytest.fixture()
def vss_user():
    return [
        (Subscriber(UserType.outer, '62715810', 65535, 65535), '62715810'),
        (Subscriber(UserType.outer, '06733057ffffffffffffffffff', 65535, 65535), '62733057'),
        (Subscriber(UserType.outer, '06793400', 65535, 65535), '62793400'),
    ]

