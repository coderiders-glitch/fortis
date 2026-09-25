from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import or_

from app.services.doctor_search import build_search_conditions


def test_search_conditions_use_case_insensitive_matching_for_all_search_fields():
    conditions = build_search_conditions("Cardiology")
    compiled = str(or_(*conditions).compile(dialect=postgresql.dialect()))

    assert compiled.count(" ILIKE ") == 4
    assert len(conditions) == 4
    assert all("%Cardiology%" in str(condition.compile().params.values()) for condition in conditions)
