from datetime import UTC

from ed_domain.core.aggregate_roots import Location
from jsons import datetime

from ed_infrastructure.common.generic import get_new_id


def get_location():
    return Location(
        id=get_new_id(),
        address="Bole Int'l Airport",
        latitude=10.0,
        longitude=20.0,
        postal_code="1000",
        city="Addis Ababa",
        country="Ethiopia",
        last_used=datetime.now(UTC),
        create_datetime=datetime.now(UTC),
        update_datetime=datetime.now(UTC),
        deleted_datetime=datetime.now(UTC),
        deleted=False,
    )
