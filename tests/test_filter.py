"""
Tests for Aaj Kay Lavayche (Garden Planner)
Tests plant filtering, container rules, date handling, and garden log.
"""

import datetime
from pathlib import Path
import pytest

from planner import (
    load_plants,
    filter_plants,
    log_garden_entry,
    get_garden_history,
    build_prompt,
    PLANTS_FILE
)


@pytest.fixture
def sample_plants():
    return load_plants(PLANTS_FILE)


def test_plants_json_has_at_least_20_items(sample_plants):
    """Ensure catalog contains at least 20 curated plants for Solapur."""
    assert len(sample_plants) >= 20
    for p in sample_plants:
        assert "id" in p
        assert "marathi_name" in p
        assert "english_name" in p
        assert "sow_months" in p
        assert isinstance(p["sow_months"], list)
        assert len(p["sow_months"]) > 0
        assert "container_friendly" in p
        assert isinstance(p["container_friendly"], bool)
        assert "short_tip" in p


def test_filter_plants_october_rabi(sample_plants):
    """October (month 10) is the start of Rabi season in Solapur."""
    oct_plants = filter_plants(sample_plants, month=10, container_only=False)
    plant_ids = [p["id"] for p in oct_plants]

    # Rabi staples should be present
    assert "methi" in plant_ids
    assert "palak" in plant_ids
    assert "kothimbir" in plant_ids
    assert "lasun" in plant_ids
    assert "tomato" in plant_ids


def test_filter_plants_container_only(sample_plants):
    """Container filter should exclude large-space plants like dudhi/lauki and shevga."""
    all_oct = filter_plants(sample_plants, month=10, container_only=False)
    container_oct = filter_plants(sample_plants, month=10, container_only=True)

    assert len(container_oct) < len(all_oct)
    for p in container_oct:
        assert p["container_friendly"] is True

    container_ids = [p["id"] for p in container_oct]
    assert "shevga" not in container_ids  # Drumstick needs ground
    assert "kanda" not in container_ids   # Onion field crop in ground


def test_filter_plants_invalid_month(sample_plants):
    """Month must be 1-12."""
    with pytest.raises(ValueError):
        filter_plants(sample_plants, month=0)
    with pytest.raises(ValueError):
        filter_plants(sample_plants, month=13)


def test_garden_log_and_history(tmp_path):
    """Test garden activity logging and recent history fetching."""
    log_file = tmp_path / "test_garden_log.md"

    # Add 3 entries
    log_garden_entry("Sowed methi in 12in pot", log_path=log_file)
    log_garden_entry("Added vermicompost to tomato seedlings", log_path=log_file)
    log_garden_entry("Harvested fresh coriander", log_path=log_file)

    history = get_garden_history(log_path=log_file, limit=2)
    assert len(history) == 2
    assert "Harvested fresh coriander" in history[-1]
    assert "Added vermicompost" in history[-2]


def test_build_prompt_marathi(sample_plants):
    """Marathi prompt should include Devanagari names and instructions."""
    oct_plants = filter_plants(sample_plants, month=10, container_only=True)
    target_date = datetime.date(2026, 10, 10)
    prompt = build_prompt(oct_plants, target_date, lang="mr", container_only=True)

    assert "आज काय लावायचं" in prompt
    assert "सोलापूर" in prompt
    assert "मेथी" in prompt or "पालक" in prompt


def test_build_prompt_english(sample_plants):
    """English prompt should include English instructions and plant names."""
    oct_plants = filter_plants(sample_plants, month=10, container_only=False)
    target_date = datetime.date(2026, 10, 10)
    prompt = build_prompt(oct_plants, target_date, lang="en", container_only=False)

    assert "Aaj Kay Lavayche" in prompt
    assert "Solapur" in prompt
    assert "Fenugreek" in prompt or "Spinach" in prompt
