import pytest
from cdr import Subscriber, UserType


@pytest.fixture()
def tetra_user():
    return [
        (
            Subscriber(UserType.inner, "102025000075780046ff", 501, 501, None),
            "62780046",
        ),
        (
            Subscriber(
                UserType.inner, "0e20250000755995ffffffffff", 65535, 65535, None
            ),
            "62785995",
        ),
        (
            Subscriber(
                UserType.inner, "102025000075782418ffffffffff", 506, 65535, None
            ),
            "62782418",
        ),
    ]


@pytest.fixture()
def vss_user():
    return [
        # (Subscriber(UserType.outer, '62715810', 65535, 65535, None), '62715810'),
        (
            Subscriber(
                UserType.outer, "06733057ffffffffffffffffff", 65535, 65535, None
            ),
            "62733057",
        ),
        (Subscriber(UserType.outer, "06793400", 65535, 65535, None), "62793400"),
        (Subscriber(UserType.outer, "09162713789", 65535, 65535, None), "62713789"),
        (Subscriber(UserType.outer, "042208", 65535, 65535, None), "62792208"),
        (Subscriber(UserType.outer, "09002715711", 65535, 65535, None), "62715711"),
        (
            Subscriber(UserType.outer, "1120250000752715711", 65535, 65535, None),
            "62715711",
        ),
    ]
