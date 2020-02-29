import pytest
from sorm.cdr import Subscriber, UserType

@pytest.fixture()
def tetra_user():
    return [
        (Subscriber(UserType.inner, '102025000075780046ff', 501, 501), '102025000075780046'),
        (Subscriber(UserType.inner, '0e20250000755995ffffffffff', 65535, 65535), '0e20250000755995'),
        (Subscriber(UserType.inner, '102025000075782418ffffffffff', 506, 65535), '102025000075782418'),
    ]

         
@pytest.fixture()
def vss_user():
    return [
        (Subscriber(UserType.outer, '62715810', 65535, 65535), '62715810'),
        (Subscriber(UserType.outer, '06733057ffffffffffffffffff', 65535, 65535), '06733057'),
        (Subscriber(UserType.outer, '793400', 65535, 65535), '793400'),
    ]

