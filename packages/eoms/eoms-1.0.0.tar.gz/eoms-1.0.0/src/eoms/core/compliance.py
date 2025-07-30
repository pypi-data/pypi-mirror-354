"""GDPR/PII compliance framework for EOMS.

This module provides tools and guidelines for handling Personally Identifiable
Information (PII) and ensuring GDPR compliance in the trading system.
"""

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Pattern

__all__ = [
    "DataClassification",
    "RetentionPolicy",
    "PIIField",
    "ComplianceConfig",
    "PIIDetector",
    "DataRetentionManager",
    "ComplianceAuditor",
    "anonymize_data",
    "encrypt_pii",
    "decrypt_pii",
]


class DataClassification(Enum):
    """Data classification levels for compliance."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"  # PII/sensitive data


@dataclass
class RetentionPolicy:
    """Data retention policy configuration."""

    classification: DataClassification
    retention_days: int
    description: str
    auto_delete: bool = False
    archive_before_delete: bool = True
    approval_required: bool = False


@dataclass
class PIIField:
    """PII field configuration."""

    field_name: str
    field_type: str  # email, phone, name, address, etc.
    required: bool = False
    encrypted: bool = True
    anonymizable: bool = True
    retention_policy: Optional[RetentionPolicy] = None


@dataclass
class ComplianceConfig:
    """Configuration for GDPR/PII compliance."""

    enabled: bool = True
    organization: str = "EOMS Trading System"
    data_controller: str = "System Administrator"
    contact_email: str = "compliance@example.com"

    # Retention policies by data type
    retention_policies: Dict[str, RetentionPolicy] = field(
        default_factory=lambda: {
            "user_data": RetentionPolicy(
                classification=DataClassification.RESTRICTED,
                retention_days=2555,  # 7 years for financial data
                description="User personal information",
                auto_delete=False,
                approval_required=True,
            ),
            "trading_data": RetentionPolicy(
                classification=DataClassification.CONFIDENTIAL,
                retention_days=2555,  # 7 years regulatory requirement
                description="Trading records and positions",
                auto_delete=False,
            ),
            "audit_logs": RetentionPolicy(
                classification=DataClassification.INTERNAL,
                retention_days=2555,  # 7 years
                description="System audit logs",
                auto_delete=True,
            ),
            "session_data": RetentionPolicy(
                classification=DataClassification.INTERNAL,
                retention_days=30,
                description="User session information",
                auto_delete=True,
            ),
        }
    )

    # PII field definitions
    pii_fields: List[PIIField] = field(
        default_factory=lambda: [
            PIIField("email", "email", required=True, encrypted=True),
            PIIField("first_name", "name", required=True, encrypted=False, anonymizable=True),
            PIIField("last_name", "name", required=True, encrypted=False, anonymizable=True),
            PIIField("phone", "phone", required=False, encrypted=True),
            PIIField("address", "address", required=False, encrypted=True),
            PIIField("tax_id", "tax_identifier", required=False, encrypted=True),
            PIIField("account_number", "financial_account", required=False, encrypted=True),
        ]
    )

    # Privacy settings
    encryption_key: Optional[str] = None
    anonymization_enabled: bool = True
    right_to_be_forgotten: bool = True
    data_portability: bool = True

    # Compliance reporting
    audit_enabled: bool = True
    audit_log_path: str = "compliance_audit.log"
    report_generation: bool = True


class PIIDetector:
    """Detects PII in data structures and text."""

    def __init__(self, config: Optional[ComplianceConfig] = None):
        """Initialize PII detector.

        Args:
            config: Compliance configuration
        """
        self.config = config or ComplianceConfig()
        self.logger = logging.getLogger(__name__)

        # Compile regex patterns for PII detection
        self.patterns: Dict[str, Pattern] = {
            "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "phone": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
            "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
            "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
        }

    def scan_data(self, data: Any, context: str = "") -> Dict[str, List[str]]:
        """Scan data for PII.

        Args:
            data: Data to scan (dict, list, string, etc.)
            context: Context description for logging

        Returns:
            Dictionary of detected PII types and their values
        """
        detected_pii = {}

        if isinstance(data, dict):
            for key, value in data.items():
                # Check field names for PII indicators
                if self._is_pii_field_name(key):
                    detected_pii.setdefault("field_names", []).append(key)

                # Recursively scan values
                nested_pii = self.scan_data(value, f"{context}.{key}")
                for pii_type, values in nested_pii.items():
                    detected_pii.setdefault(pii_type, []).extend(values)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                nested_pii = self.scan_data(item, f"{context}[{i}]")
                for pii_type, values in nested_pii.items():
                    detected_pii.setdefault(pii_type, []).extend(values)

        elif isinstance(data, str):
            # Scan text for PII patterns
            for pii_type, pattern in self.patterns.items():
                matches = pattern.findall(data)
                if matches:
                    detected_pii.setdefault(pii_type, []).extend(matches)

        return detected_pii

    def _is_pii_field_name(self, field_name: str) -> bool:
        """Check if field name indicates PII.

        Args:
            field_name: Field name to check

        Returns:
            True if field name suggests PII
        """
        pii_indicators = [
            "email",
            "mail",
            "name",
            "first",
            "last",
            "phone",
            "tel",
            "mobile",
            "address",
            "street",
            "city",
            "zip",
            "postal",
            "ssn",
            "social",
            "tax",
            "id",
            "account",
            "card",
            "credit",
            "passport",
            "license",
        ]

        field_lower = field_name.lower()
        return any(indicator in field_lower for indicator in pii_indicators)

    def generate_detection_report(self, data: Any, context: str = "data") -> str:
        """Generate a PII detection report.

        Args:
            data: Data to analyze
            context: Context description

        Returns:
            Formatted report string
        """
        detected_pii = self.scan_data(data, context)

        if not detected_pii:
            return f"No PII detected in {context}"

        report = f"PII Detection Report for {context}:\n"
        report += "=" * 50 + "\n"

        for pii_type, values in detected_pii.items():
            report += f"\n{pii_type.upper()}:\n"
            for value in set(values):  # Remove duplicates
                # Partially mask values for security
                masked_value = self._mask_value(value)
                report += f"  - {masked_value}\n"

        return report

    def _mask_value(self, value: str, mask_char: str = "*") -> str:
        """Mask a value for safe display.

        Args:
            value: Value to mask
            mask_char: Character to use for masking

        Returns:
            Masked value
        """
        if len(value) <= 4:
            return mask_char * len(value)

        visible_chars = 2
        masked_length = len(value) - (2 * visible_chars)

        return value[:visible_chars] + (mask_char * masked_length) + value[-visible_chars:]


class DataRetentionManager:
    """Manages data retention policies and cleanup."""

    def __init__(self, config: Optional[ComplianceConfig] = None):
        """Initialize data retention manager.

        Args:
            config: Compliance configuration
        """
        self.config = config or ComplianceConfig()
        self.logger = logging.getLogger(__name__)

    def check_retention_requirements(
        self, data_type: str, created_date: datetime
    ) -> Dict[str, Any]:
        """Check retention requirements for data.

        Args:
            data_type: Type of data to check
            created_date: When the data was created

        Returns:
            Retention status information
        """
        policy = self.config.retention_policies.get(data_type)
        if not policy:
            self.logger.warning(f"No retention policy found for data type: {data_type}")
            return {
                "status": "no_policy",
                "action_required": False,
                "message": f"No retention policy defined for {data_type}",
            }

        # Calculate expiry date
        expiry_date = created_date + timedelta(days=policy.retention_days)
        now = datetime.now()

        days_until_expiry = (expiry_date - now).days

        if days_until_expiry < 0:
            # Data has expired
            return {
                "status": "expired",
                "action_required": True,
                "action": "delete" if policy.auto_delete else "review_for_deletion",
                "expired_days": abs(days_until_expiry),
                "policy": policy,
                "message": f"Data expired {abs(days_until_expiry)} days ago",
            }
        elif days_until_expiry <= 30:
            # Data expires soon
            return {
                "status": "expiring_soon",
                "action_required": True,
                "action": "prepare_for_deletion",
                "days_remaining": days_until_expiry,
                "policy": policy,
                "message": f"Data expires in {days_until_expiry} days",
            }
        else:
            # Data is within retention period
            return {
                "status": "active",
                "action_required": False,
                "days_remaining": days_until_expiry,
                "policy": policy,
                "message": f"Data is within retention period ({days_until_expiry} days remaining)",
            }

    def generate_retention_report(self, data_inventory: List[Dict[str, Any]]) -> str:
        """Generate a data retention report.

        Args:
            data_inventory: List of data items with type and creation date

        Returns:
            Formatted retention report
        """
        report = "Data Retention Report\n"
        report += "=" * 50 + "\n"
        report += f"Generated: {datetime.now().isoformat()}\n\n"

        status_counts = {"active": 0, "expiring_soon": 0, "expired": 0, "no_policy": 0}

        expired_items = []
        expiring_items = []

        for item in data_inventory:
            data_type = item.get("type", "unknown")
            created_date = item.get("created_date")

            if not isinstance(created_date, datetime):
                continue

            retention_info = self.check_retention_requirements(data_type, created_date)
            status = retention_info["status"]
            status_counts[status] += 1

            if status == "expired":
                expired_items.append((item, retention_info))
            elif status == "expiring_soon":
                expiring_items.append((item, retention_info))

        # Summary
        report += "SUMMARY:\n"
        for status, count in status_counts.items():
            report += f"  {status.replace('_', ' ').title()}: {count}\n"

        # Expired items
        if expired_items:
            report += "\nEXPIRED ITEMS (Action Required):\n"
            for item, info in expired_items:
                report += f"  - {item.get('description', 'Unknown')} "
                report += f"(Type: {item.get('type')}, "
                report += f"Expired: {info['expired_days']} days ago)\n"

        # Expiring items
        if expiring_items:
            report += "\nITEMS EXPIRING SOON:\n"
            for item, info in expiring_items:
                report += f"  - {item.get('description', 'Unknown')} "
                report += f"(Type: {item.get('type')}, "
                report += f"Expires in: {info['days_remaining']} days)\n"

        return report


class ComplianceAuditor:
    """Audits system compliance with GDPR/PII requirements."""

    def __init__(self, config: Optional[ComplianceConfig] = None):
        """Initialize compliance auditor.

        Args:
            config: Compliance configuration
        """
        self.config = config or ComplianceConfig()
        self.logger = logging.getLogger(__name__)
        self.pii_detector = PIIDetector(config)
        self.retention_manager = DataRetentionManager(config)

    def audit_data_handling(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """Audit data handling practices.

        Args:
            data_sources: Dictionary of data sources to audit

        Returns:
            Audit results
        """
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "organization": self.config.organization,
            "auditor": "ComplianceAuditor",
            "sources_audited": list(data_sources.keys()),
            "pii_detected": {},
            "compliance_issues": [],
            "recommendations": [],
            "overall_score": 0,
        }

        total_issues = 0

        for source_name, data in data_sources.items():
            self.logger.info(f"Auditing data source: {source_name}")

            # Detect PII
            detected_pii = self.pii_detector.scan_data(data, source_name)
            if detected_pii:
                audit_results["pii_detected"][source_name] = detected_pii

                # Check if PII is properly protected
                for pii_type, _values in detected_pii.items():
                    if not self._is_pii_protected(source_name, pii_type):
                        issue = {
                            "source": source_name,
                            "type": "unprotected_pii",
                            "description": f"PII type '{pii_type}' found but not protected",
                            "severity": "high",
                            "recommendation": f"Implement encryption/anonymization for {pii_type}",
                        }
                        audit_results["compliance_issues"].append(issue)
                        total_issues += 1

        # Check retention policies
        missing_policies = []
        for source_name in data_sources.keys():
            if not self._has_retention_policy(source_name):
                missing_policies.append(source_name)

        if missing_policies:
            issue = {
                "type": "missing_retention_policy",
                "description": f"Missing retention policies for: {', '.join(missing_policies)}",
                "severity": "medium",
                "recommendation": "Define retention policies for all data sources",
            }
            audit_results["compliance_issues"].append(issue)
            total_issues += 1

        # Calculate compliance score
        max_score = 100
        penalty_per_issue = 10
        audit_results["overall_score"] = max(0, max_score - (total_issues * penalty_per_issue))

        # Generate recommendations
        if audit_results["overall_score"] < 80:
            audit_results["recommendations"].append(
                "Immediate action required to address compliance issues"
            )
        elif audit_results["overall_score"] < 90:
            audit_results["recommendations"].append("Minor improvements needed for full compliance")
        else:
            audit_results["recommendations"].append("Good compliance posture, continue monitoring")

        return audit_results

    def _is_pii_protected(self, source_name: str, pii_type: str) -> bool:
        """Check if PII is properly protected.

        Args:
            source_name: Name of data source
            pii_type: Type of PII

        Returns:
            True if PII appears to be protected
        """
        # This is a simplified check - in practice, you'd verify actual encryption/anonymization
        protected_sources = ["encrypted_database", "secure_storage", "anonymized_data"]
        return any(protected in source_name.lower() for protected in protected_sources)

    def _has_retention_policy(self, source_name: str) -> bool:
        """Check if data source has a retention policy.

        Args:
            source_name: Name of data source

        Returns:
            True if retention policy exists
        """
        # Check if source matches any configured retention policies
        return any(
            policy_name in source_name.lower()
            for policy_name in self.config.retention_policies.keys()
        )

    def generate_compliance_report(self, audit_results: Dict[str, Any]) -> str:
        """Generate a formatted compliance report.

        Args:
            audit_results: Results from audit_data_handling

        Returns:
            Formatted compliance report
        """
        report = "GDPR/PII Compliance Audit Report\n"
        report += f"Organization: {audit_results['organization']}\n"
        report += f"Generated: {audit_results['timestamp']}\n"
        report += "=" * 60 + "\n\n"

        # Overall score
        score = audit_results["overall_score"]
        report += f"OVERALL COMPLIANCE SCORE: {score}/100\n"

        if score >= 90:
            report += "Status: EXCELLENT ✓\n"
        elif score >= 80:
            report += "Status: GOOD ⚠\n"
        elif score >= 70:
            report += "Status: NEEDS IMPROVEMENT ⚠\n"
        else:
            report += "Status: NON-COMPLIANT ✗\n"

        report += "\n"

        # PII Detection Summary
        pii_detected = audit_results.get("pii_detected", {})
        if pii_detected:
            report += "PII DETECTION SUMMARY:\n"
            for source, pii_types in pii_detected.items():
                report += f"  {source}:\n"
                for pii_type, count in pii_types.items():
                    report += f"    - {pii_type}: {len(count)} instances\n"
            report += "\n"

        # Compliance Issues
        issues = audit_results.get("compliance_issues", [])
        if issues:
            report += "COMPLIANCE ISSUES:\n"
            for i, issue in enumerate(issues, 1):
                report += f"  {i}. {issue['description']}\n"
                report += f"     Severity: {issue['severity'].upper()}\n"
                report += f"     Recommendation: {issue['recommendation']}\n\n"
        else:
            report += "No compliance issues found.\n\n"

        # Recommendations
        recommendations = audit_results.get("recommendations", [])
        if recommendations:
            report += "RECOMMENDATIONS:\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"  {i}. {rec}\n"

        return report


# Utility functions for data anonymization and encryption


def anonymize_data(data: Any, fields_to_anonymize: List[str]) -> Any:
    """Anonymize specified fields in data.

    Args:
        data: Data to anonymize
        fields_to_anonymize: List of field names to anonymize

    Returns:
        Anonymized data
    """
    if isinstance(data, dict):
        anonymized = {}
        for key, value in data.items():
            if key in fields_to_anonymize:
                # Simple anonymization - replace with hash
                original_value = str(value)
                anonymized[key] = hashlib.sha256(original_value.encode()).hexdigest()[:8]
            else:
                # Recursively process nested data
                anonymized[key] = anonymize_data(value, fields_to_anonymize)
        return anonymized

    elif isinstance(data, list):
        return [anonymize_data(item, fields_to_anonymize) for item in data]

    else:
        return data


def encrypt_pii(data: str, key: Optional[str] = None) -> str:
    """Encrypt PII data (simplified implementation).

    Args:
        data: Data to encrypt
        key: Encryption key (if None, uses a default)

    Returns:
        Encrypted data (base64 encoded)
    """
    # This is a simplified implementation - use proper encryption in production
    import base64

    if key is None:
        key = "default_encryption_key_change_in_production"

    # Simple XOR encryption (NOT suitable for production)
    encrypted = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted.append(encrypted_char)

    encrypted_bytes = "".join(encrypted).encode("utf-8")
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def decrypt_pii(encrypted_data: str, key: Optional[str] = None) -> str:
    """Decrypt PII data (simplified implementation).

    Args:
        encrypted_data: Encrypted data to decrypt
        key: Decryption key (if None, uses default)

    Returns:
        Decrypted data
    """
    import base64

    if key is None:
        key = "default_encryption_key_change_in_production"

    try:
        # Decode from base64
        encrypted_bytes = base64.b64decode(encrypted_data.encode("utf-8"))
        encrypted_string = encrypted_bytes.decode("utf-8")

        # Simple XOR decryption
        decrypted = []
        for i, char in enumerate(encrypted_string):
            key_char = key[i % len(key)]
            decrypted_char = chr(ord(char) ^ ord(key_char))
            decrypted.append(decrypted_char)

        return "".join(decrypted)

    except Exception:
        return "DECRYPTION_FAILED"


# Example data retention cleanup
def cleanup_expired_data(
    data_inventory: List[Dict[str, Any]], config: Optional[ComplianceConfig] = None
) -> Dict[str, Any]:
    """Clean up expired data according to retention policies.

    Args:
        data_inventory: List of data items to check
        config: Compliance configuration

    Returns:
        Cleanup results
    """
    retention_manager = DataRetentionManager(config)

    cleanup_results = {
        "total_items": len(data_inventory),
        "items_deleted": 0,
        "items_archived": 0,
        "items_requiring_approval": 0,
        "deleted_items": [],
        "archived_items": [],
        "approval_required_items": [],
    }

    for item in data_inventory:
        data_type = item.get("type", "unknown")
        created_date = item.get("created_date")

        if not isinstance(created_date, datetime):
            continue

        retention_info = retention_manager.check_retention_requirements(data_type, created_date)

        if retention_info["status"] == "expired":
            policy = retention_info.get("policy")

            if policy and policy.approval_required:
                cleanup_results["approval_required_items"].append(item)
                cleanup_results["items_requiring_approval"] += 1

            elif policy and policy.auto_delete:
                # Simulate deletion
                cleanup_results["deleted_items"].append(item)
                cleanup_results["items_deleted"] += 1

                if policy.archive_before_delete:
                    cleanup_results["archived_items"].append(item)
                    cleanup_results["items_archived"] += 1

    return cleanup_results
