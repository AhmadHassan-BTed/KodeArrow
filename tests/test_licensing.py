import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kode_arrow.services.licensing import LicensingService

def test_community_email_bypass():
    # Mock firebase service and DB
    mock_firebase = MagicMock()
    mock_db = MagicMock()
    mock_firebase.db = mock_db
    
    # Setup LicensingService
    service = LicensingService(mock_firebase)
    
    # Mock DB document retrieval for community email
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.get.return_value = "2099-12-31" # expiration date
    
    # Mock devices collection query with 5 devices (exceeding standard limit of 4)
    mock_device_doc = MagicMock()
    mock_device_doc.to_dict.return_value = {'id': 'existing_device_id'}
    
    mock_devices_ref = MagicMock()
    mock_devices_ref.get.return_value = [mock_device_doc] * 5
    
    mock_user_ref = MagicMock()
    mock_user_ref.get.return_value = mock_doc
    mock_user_ref.collection.return_value = mock_devices_ref
    
    mock_db.collection.return_value.document.return_value = mock_user_ref
    
    # Call validate_and_activate with patching
    with patch('kode_arrow.services.licensing.check_internet_connection', return_value=True), \
         patch('kode_arrow.services.licensing.create_hidden_file') as mock_create_file:
        
        result = service.validate_and_activate(
            email="freeforever@kodearrow.dev",
            hardware_id="new_device_id",
            premium_file_path="dummy_path.txt",
            is_research=False
        )
        
        # Assert collection is resolved to ControlGroup instead of users
        mock_db.collection.assert_called_with("ControlGroup")
        
        # Assert that device registry document set is called to save stats
        mock_devices_ref.document.assert_called_with("device6")
        mock_devices_ref.document.return_value.set.assert_called_with({'id': 'new_device_id'})
        
        # Check success
        assert result is True
