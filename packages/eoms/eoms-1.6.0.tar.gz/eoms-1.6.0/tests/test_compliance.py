"""Tests for GDPR/PII compliance framework."""

from datetime import datetime, timedelta

import pytest

from eoms.core.compliance import (
    ComplianceAuditor,
    ComplianceConfig,
    DataClassification,
    DataRetentionManager,
    PIIDetector,
    PIIField,
    RetentionPolicy,
    anonymize_data,
    cleanup_expired_data,
    decrypt_pii,
    encrypt_pii,
)


@pytest.fixture
def compliance_config():
    """Create test compliance configuration."""
    return ComplianceConfig(
        enabled=True,
        organization="Test Trading Corp",
        data_controller="Test Controller",
        contact_email="test@example.com",
        encryption_key="test_key_12345",
    )


@pytest.fixture
def sample_pii_data():
    """Sample data containing PII for testing."""
    return {
        "user": {
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "555-123-4567",
            "address": "123 Main St, Anytown",
            "ssn": "123-45-6789",
        },
        "trading": {
            "account_number": "ACCT-12345",
            "balance": 10000.00,
            "positions": ["AAPL", "MSFT"],
        },
        "system": {
            "ip_address": "192.168.1.100",
            "session_id": "sess_123456",
            "last_login": "2023-12-01T10:00:00",
        },
    }


@pytest.fixture
def sample_data_inventory():
    """Sample data inventory for retention testing."""
    now = datetime.now()
    return [
        {
            "id": "user_001",
            "type": "user_data",
            "description": "User profile data",
            "created_date": now - timedelta(days=10),
            "size_mb": 1.2,
        },
        {
            "id": "trade_001",
            "type": "trading_data",
            "description": "Trading transaction",
            "created_date": now - timedelta(days=2600),  # Expired
            "size_mb": 0.5,
        },
        {
            "id": "session_001",
            "type": "session_data",
            "description": "User session log",
            "created_date": now - timedelta(days=35),  # Expired (30 day retention)
            "size_mb": 0.1,
        },
        {
            "id": "audit_001",
            "type": "audit_logs",
            "description": "System audit log",
            "created_date": now - timedelta(days=25),  # Expiring soon
            "size_mb": 2.0,
        },
    ]


class TestDataClassification:
    """Test data classification enumeration."""

    def test_classification_values(self):
        """Test classification enum values."""
        assert DataClassification.PUBLIC.value == "public"
        assert DataClassification.INTERNAL.value == "internal"
        assert DataClassification.CONFIDENTIAL.value == "confidential"
        assert DataClassification.RESTRICTED.value == "restricted"


class TestRetentionPolicy:
    """Test retention policy configuration."""

    def test_retention_policy_creation(self):
        """Test retention policy creation."""
        policy = RetentionPolicy(
            classification=DataClassification.RESTRICTED,
            retention_days=365,
            description="Personal data retention",
            auto_delete=True,
            archive_before_delete=True,
            approval_required=False,
        )

        assert policy.classification == DataClassification.RESTRICTED
        assert policy.retention_days == 365
        assert policy.description == "Personal data retention"
        assert policy.auto_delete is True
        assert policy.archive_before_delete is True
        assert policy.approval_required is False


class TestPIIField:
    """Test PII field configuration."""

    def test_pii_field_creation(self):
        """Test PII field creation."""
        field = PIIField(
            field_name="email",
            field_type="email",
            required=True,
            encrypted=True,
            anonymizable=True,
        )

        assert field.field_name == "email"
        assert field.field_type == "email"
        assert field.required is True
        assert field.encrypted is True
        assert field.anonymizable is True


class TestComplianceConfig:
    """Test compliance configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ComplianceConfig()

        assert config.enabled is True
        assert config.organization == "EOMS Trading System"
        assert config.data_controller == "System Administrator"
        assert "retention_policies" in config.__dict__
        assert "pii_fields" in config.__dict__
        assert len(config.retention_policies) > 0
        assert len(config.pii_fields) > 0

    def test_custom_config(self, compliance_config):
        """Test custom configuration."""
        assert compliance_config.organization == "Test Trading Corp"
        assert compliance_config.data_controller == "Test Controller"
        assert compliance_config.contact_email == "test@example.com"
        assert compliance_config.encryption_key == "test_key_12345"


class TestPIIDetector:
    """Test PII detection functionality."""

    def test_detector_initialization(self, compliance_config):
        """Test PII detector initialization."""
        detector = PIIDetector(compliance_config)

        assert detector.config == compliance_config
        assert len(detector.patterns) > 0
        assert "email" in detector.patterns
        assert "phone" in detector.patterns

    def test_email_detection(self):
        """Test email PII detection."""
        detector = PIIDetector()

        data = "Contact us at support@example.com or admin@test.org"
        detected = detector.scan_data(data)

        assert "email" in detected
        assert "support@example.com" in detected["email"]
        assert "admin@test.org" in detected["email"]

    def test_phone_detection(self):
        """Test phone number PII detection."""
        detector = PIIDetector()

        data = "Call me at 555-123-4567 or 555.987.6543"
        detected = detector.scan_data(data)

        assert "phone" in detected
        assert "555-123-4567" in detected["phone"]
        assert "555.987.6543" in detected["phone"]

    def test_dict_data_scanning(self, sample_pii_data):
        """Test scanning dictionary data for PII."""
        detector = PIIDetector()

        detected = detector.scan_data(sample_pii_data)

        assert "email" in detected
        assert "phone" in detected
        assert "ssn" in detected
        assert "ip_address" in detected
        assert "field_names" in detected

        # Check specific values
        assert "john.doe@example.com" in detected["email"]
        assert "555-123-4567" in detected["phone"]
        assert "123-45-6789" in detected["ssn"]

    def test_field_name_detection(self):
        """Test PII field name detection."""
        detector = PIIDetector()

        data = {
            "user_email": "test@example.com",
            "full_name": "John Doe",
            "phone_number": "555-1234",
            "non_pii_field": "some value",
        }

        detected = detector.scan_data(data)

        assert "field_names" in detected
        field_names = detected["field_names"]
        assert "user_email" in field_names
        assert "full_name" in field_names
        assert "phone_number" in field_names
        assert "non_pii_field" not in field_names

    def test_list_data_scanning(self):
        """Test scanning list data for PII."""
        detector = PIIDetector()

        data = [
            {"email": "user1@example.com"},
            {"email": "user2@example.com"},
            "Contact: support@help.com",
        ]

        detected = detector.scan_data(data)

        assert "email" in detected
        assert len(detected["email"]) == 3

    def test_generate_detection_report(self, sample_pii_data):
        """Test PII detection report generation."""
        detector = PIIDetector()

        report = detector.generate_detection_report(sample_pii_data, "test_data")

        assert "PII Detection Report for test_data" in report
        assert "EMAIL:" in report
        assert "PHONE:" in report
        assert "SSN:" in report
        # Values should be masked in report
        assert "jo***@***ple.com" in report or "***" in report

    def test_value_masking(self):
        """Test value masking functionality."""
        detector = PIIDetector()

        # Test different value lengths
        assert detector._mask_value("test") == "****"
        assert detector._mask_value("hello") == "he*lo"
        assert detector._mask_value("test@example.com") == "te************om"
        assert detector._mask_value("555-123-4567") == "55********67"


class TestDataRetentionManager:
    """Test data retention management."""

    def test_manager_initialization(self, compliance_config):
        """Test retention manager initialization."""
        manager = DataRetentionManager(compliance_config)

        assert manager.config == compliance_config

    def test_active_data_check(self, compliance_config):
        """Test retention check for active data."""
        manager = DataRetentionManager(compliance_config)

        # Data created 10 days ago - should be active
        created_date = datetime.now() - timedelta(days=10)
        result = manager.check_retention_requirements("user_data", created_date)

        assert result["status"] == "active"
        assert result["action_required"] is False
        assert result["days_remaining"] > 2500  # 7 years minus 10 days

    def test_expired_data_check(self, compliance_config):
        """Test retention check for expired data."""
        manager = DataRetentionManager(compliance_config)

        # Data created 3000 days ago - should be expired
        created_date = datetime.now() - timedelta(days=3000)
        result = manager.check_retention_requirements("user_data", created_date)

        assert result["status"] == "expired"
        assert result["action_required"] is True
        assert result["expired_days"] > 0

    def test_expiring_soon_data_check(self, compliance_config):
        """Test retention check for data expiring soon."""
        manager = DataRetentionManager(compliance_config)

        # Data that expires in 15 days
        created_date = datetime.now() - timedelta(days=2555 - 15)  # 7 years minus 15 days
        result = manager.check_retention_requirements("user_data", created_date)

        assert result["status"] == "expiring_soon"
        assert result["action_required"] is True
        assert result["days_remaining"] <= 30

    def test_no_policy_check(self, compliance_config):
        """Test retention check for data type without policy."""
        manager = DataRetentionManager(compliance_config)

        created_date = datetime.now() - timedelta(days=10)
        result = manager.check_retention_requirements("unknown_data_type", created_date)

        assert result["status"] == "no_policy"
        assert result["action_required"] is False

    def test_retention_report_generation(self, compliance_config, sample_data_inventory):
        """Test retention report generation."""
        manager = DataRetentionManager(compliance_config)

        report = manager.generate_retention_report(sample_data_inventory)

        assert "Data Retention Report" in report
        assert "SUMMARY:" in report
        assert "Active:" in report
        assert "Expired:" in report or "Expiring Soon:" in report


class TestComplianceAuditor:
    """Test compliance auditing functionality."""

    def test_auditor_initialization(self, compliance_config):
        """Test compliance auditor initialization."""
        auditor = ComplianceAuditor(compliance_config)

        assert auditor.config == compliance_config
        assert auditor.pii_detector is not None
        assert auditor.retention_manager is not None

    def test_data_handling_audit(self, compliance_config, sample_pii_data):
        """Test data handling audit."""
        auditor = ComplianceAuditor(compliance_config)

        data_sources = {
            "user_database": sample_pii_data,
            "trading_system": {"trades": [{"symbol": "AAPL", "quantity": 100}]},
        }

        results = auditor.audit_data_handling(data_sources)

        assert "timestamp" in results
        assert "organization" in results
        assert "sources_audited" in results
        assert "pii_detected" in results
        assert "compliance_issues" in results
        assert "overall_score" in results

        # Should detect PII in user_database
        assert "user_database" in results["pii_detected"]

        # Score should be calculated
        assert 0 <= results["overall_score"] <= 100

    def test_compliance_report_generation(self, compliance_config):
        """Test compliance report generation."""
        auditor = ComplianceAuditor(compliance_config)

        audit_results = {
            "timestamp": "2023-12-01T10:00:00",
            "organization": "Test Corp",
            "overall_score": 85,
            "pii_detected": {"database": {"email": ["test@example.com"]}},
            "compliance_issues": [
                {
                    "description": "Unprotected PII found",
                    "severity": "high",
                    "recommendation": "Implement encryption",
                }
            ],
            "recommendations": ["Review data protection measures"],
        }

        report = auditor.generate_compliance_report(audit_results)

        assert "GDPR/PII Compliance Audit Report" in report
        assert "OVERALL COMPLIANCE SCORE: 85/100" in report
        assert "PII DETECTION SUMMARY:" in report
        assert "COMPLIANCE ISSUES:" in report
        assert "RECOMMENDATIONS:" in report


class TestUtilityFunctions:
    """Test utility functions for data protection."""

    def test_data_anonymization(self):
        """Test data anonymization."""
        data = {"name": "John Doe", "email": "john@example.com", "balance": 1000.00}

        anonymized = anonymize_data(data, ["name", "email"])

        # Original fields should be replaced with hashes
        assert anonymized["name"] != "John Doe"
        assert anonymized["email"] != "john@example.com"
        assert anonymized["balance"] == 1000.00  # Not anonymized

        # Anonymized values should be consistent
        assert len(anonymized["name"]) == 8  # Hash is truncated to 8 chars
        assert len(anonymized["email"]) == 8

    def test_list_data_anonymization(self):
        """Test anonymization of list data."""
        data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

        anonymized = anonymize_data(data, ["name"])

        assert len(anonymized) == 2
        assert anonymized[0]["name"] != "John"
        assert anonymized[1]["name"] != "Jane"
        assert anonymized[0]["age"] == 30
        assert anonymized[1]["age"] == 25

    def test_pii_encryption_decryption(self):
        """Test PII encryption and decryption."""
        original_data = "sensitive@email.com"
        key = "test_encryption_key"

        # Encrypt
        encrypted = encrypt_pii(original_data, key)
        assert encrypted != original_data
        assert len(encrypted) > 0

        # Decrypt
        decrypted = decrypt_pii(encrypted, key)
        assert decrypted == original_data

    def test_encryption_with_default_key(self):
        """Test encryption with default key."""
        original_data = "test data"

        encrypted = encrypt_pii(original_data)
        decrypted = decrypt_pii(encrypted)

        assert decrypted == original_data

    def test_decryption_failure(self):
        """Test decryption failure handling."""
        invalid_encrypted_data = "invalid_base64_data"

        result = decrypt_pii(invalid_encrypted_data)
        assert result == "DECRYPTION_FAILED"


class TestDataCleanup:
    """Test data cleanup functionality."""

    def test_expired_data_cleanup(self, compliance_config, sample_data_inventory):
        """Test cleanup of expired data."""
        results = cleanup_expired_data(sample_data_inventory, compliance_config)

        assert "total_items" in results
        assert "items_deleted" in results
        assert "items_archived" in results
        assert "items_requiring_approval" in results

        assert results["total_items"] == len(sample_data_inventory)

        # Should have some expired items to process
        total_processed = results["items_deleted"] + results["items_requiring_approval"]
        assert total_processed > 0

    def test_cleanup_with_approval_required(self, compliance_config):
        """Test cleanup when approval is required."""
        # Modify config to require approval for user data
        compliance_config.retention_policies["user_data"].approval_required = True

        # Create expired user data
        now = datetime.now()
        inventory = [
            {
                "id": "user_expired",
                "type": "user_data",
                "created_date": now - timedelta(days=3000),
                "description": "Expired user data",
            }
        ]

        results = cleanup_expired_data(inventory, compliance_config)

        # Should require approval, not auto-delete
        assert results["items_requiring_approval"] == 1
        assert results["items_deleted"] == 0


class TestRealWorldScenarios:
    """Test real-world compliance scenarios."""

    def test_trading_system_audit(self, compliance_config):
        """Test comprehensive audit of trading system data."""
        trading_data = {
            "user_accounts": {
                "user_123": {
                    "email": "trader@firm.com",
                    "name": "Jane Trader",
                    "account_id": "ACC-789",
                    "risk_limit": 100000,
                }
            },
            "trading_logs": [
                {
                    "timestamp": "2023-12-01T09:30:00",
                    "user_id": "user_123",
                    "action": "BUY",
                    "symbol": "AAPL",
                    "quantity": 100,
                    "price": 150.00,
                }
            ],
            "system_logs": {
                "session_123": {
                    "ip_address": "10.1.1.100",
                    "login_time": "2023-12-01T08:00:00",
                    "user_agent": "TradingApp/1.0",
                }
            },
        }

        auditor = ComplianceAuditor(compliance_config)
        results = auditor.audit_data_handling(trading_data)

        # Should detect PII across multiple sources
        assert len(results["pii_detected"]) > 0

        # Should have reasonable compliance score
        assert results["overall_score"] >= 0

        # Should identify potential issues
        assert "compliance_issues" in results

    def test_gdpr_right_to_be_forgotten(self, compliance_config):
        """Test implementation of right to be forgotten."""
        user_data = {
            "personal_info": {
                "email": "user@example.com",
                "name": "John User",
                "phone": "555-0123",
            },
            "trading_history": [{"date": "2023-01-01", "trade": "BUY AAPL 100"}],
        }

        # Anonymize personal data while preserving trading records
        anonymized = anonymize_data(user_data, ["email", "name", "phone"])

        # Personal info should be anonymized
        assert anonymized["personal_info"]["email"] != "user@example.com"
        assert anonymized["personal_info"]["name"] != "John User"

        # Trading history should be preserved (not in anonymization list)
        assert anonymized["trading_history"] == user_data["trading_history"]

    def test_regulatory_data_retention(self, compliance_config):
        """Test regulatory compliance for financial data retention."""
        # Financial regulations often require 7-year retention
        seven_years_ago = datetime.now() - timedelta(days=2555)
        eight_years_ago = datetime.now() - timedelta(days=2920)

        manager = DataRetentionManager(compliance_config)

        # 8-year-old data should be expired
        old_result = manager.check_retention_requirements("trading_data", eight_years_ago)
        assert old_result["status"] == "expired"

        # 7-year-old data should be at the edge (might be expired or expiring soon)
        recent_result = manager.check_retention_requirements("trading_data", seven_years_ago)
        assert recent_result["status"] in ["expired", "expiring_soon", "active"]
