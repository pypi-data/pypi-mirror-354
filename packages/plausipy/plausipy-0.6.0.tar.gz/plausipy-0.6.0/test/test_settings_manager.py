import json
import tempfile
from pathlib import Path

import pytest

from plausipy.user import SettingsManager


@pytest.fixture
def sm():
    with tempfile.NamedTemporaryFile() as temp_file:
        SettingsManager._settings_file = Path(temp_file.name)
        sm = SettingsManager.get()
        yield sm


def test_seting_history_enabled_default(sm):
    assert sm.history_enabled is False
    
def test_seting_history_enabled_true(sm):
    with sm:
        sm.history_enabled = True
    
    # load the settings file as json directly
    with open(sm._settings_file, "r") as f:
        data = json.load(f)
        
    # assert that value is set to True
    assert data["history_enabled"] is True
    
def test_seting_history_enabled_false(sm):
    with sm:
        sm.history_enabled = True
    
    # load the settings file as json directly
    with open(sm._settings_file, "r") as f:
        data = json.load(f)
        
    # assert that value is set to True
    assert data["history_enabled"] is True
    
def test_reset_and_load_defaults(sm):
    with sm:
        sm.history_enabled = True
        sm.logger_enabled = False
        sm.logger_level = "DEBUG"
        sm.logger_keep_days = 30
                
    # reset settings
    sm.reset()
    
    # assert default values after reset
    assert sm.history_enabled is False
    assert sm.logger_enabled is True
    assert sm.logger_level == "INFO"
    assert sm.logger_keep_days == 7