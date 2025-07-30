"""Tests for security audit tools."""

import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from eoms.core.security import (
    SecurityAuditor,
    SecurityAuditResult,
    SecurityConfig,
    SecurityIssue,
    VulnerabilityLevel,
    run_security_audit,
)


@pytest.fixture
def security_config():
    """Create test security configuration."""
    return SecurityConfig(
        enabled=True,
        fail_on_critical=True,
        fail_on_high=False,
        max_issues=50,
        bandit_enabled=True,
        safety_enabled=True,
        pip_audit_enabled=True,
        output_dir="test_security_reports",
        json_output=True,
    )


@pytest.fixture
def sample_security_issues():
    """Create sample security issues for testing."""
    return [
        SecurityIssue(
            tool="bandit",
            severity=VulnerabilityLevel.HIGH,
            title="Hard-coded password",
            description="Possible hard-coded password found",
            file_path="/app/config.py",
            line_number=42,
            cwe_id="CWE-259",
        ),
        SecurityIssue(
            tool="safety",
            severity=VulnerabilityLevel.CRITICAL,
            title="Vulnerable package: requests",
            description="Known security vulnerability",
            package="requests",
            affected_version="2.25.0",
            cve_id="CVE-2021-33503",
        ),
        SecurityIssue(
            tool="pip-audit",
            severity=VulnerabilityLevel.MEDIUM,
            title="Vulnerable package: flask",
            description="Cross-site scripting vulnerability",
            package="flask",
            affected_version="1.0.0",
            fixed_version="1.1.4",
            cve_id="CVE-2020-1234",
        ),
    ]


class TestSecurityConfig:
    """Test security configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = SecurityConfig()

        assert config.enabled is True
        assert config.fail_on_critical is True
        assert config.fail_on_high is False
        assert config.max_issues == 100
        assert config.bandit_enabled is True
        assert config.safety_enabled is True
        assert config.pip_audit_enabled is True
        assert config.output_dir == "security_reports"
        assert config.json_output is True

    def test_custom_config(self):
        """Test custom configuration."""
        config = SecurityConfig(
            enabled=False,
            fail_on_critical=False,
            fail_on_high=True,
            max_issues=25,
            bandit_enabled=False,
            safety_enabled=False,
            pip_audit_enabled=False,
            output_dir="custom_reports",
            json_output=False,
        )

        assert config.enabled is False
        assert config.fail_on_critical is False
        assert config.fail_on_high is True
        assert config.max_issues == 25
        assert config.bandit_enabled is False
        assert config.safety_enabled is False
        assert config.pip_audit_enabled is False
        assert config.output_dir == "custom_reports"
        assert config.json_output is False


class TestSecurityIssue:
    """Test security issue representation."""

    def test_security_issue_creation(self):
        """Test security issue creation."""
        issue = SecurityIssue(
            tool="bandit",
            severity=VulnerabilityLevel.HIGH,
            title="Test Issue",
            description="Test description",
            file_path="/test/file.py",
            line_number=42,
            cwe_id="CWE-123",
        )

        assert issue.tool == "bandit"
        assert issue.severity == VulnerabilityLevel.HIGH
        assert issue.title == "Test Issue"
        assert issue.description == "Test description"
        assert issue.file_path == "/test/file.py"
        assert issue.line_number == 42
        assert issue.cwe_id == "CWE-123"

    def test_security_issue_optional_fields(self):
        """Test security issue with optional fields."""
        issue = SecurityIssue(
            tool="safety",
            severity=VulnerabilityLevel.CRITICAL,
            title="Vulnerable Package",
            description="Package has known vulnerability",
            package="test-package",
            affected_version="1.0.0",
            fixed_version="1.1.0",
            cve_id="CVE-2021-12345",
            references=["https://example.com/advisory"],
        )

        assert issue.package == "test-package"
        assert issue.affected_version == "1.0.0"
        assert issue.fixed_version == "1.1.0"
        assert issue.cve_id == "CVE-2021-12345"
        assert issue.references == ["https://example.com/advisory"]


class TestSecurityAuditResult:
    """Test security audit result."""

    def test_audit_result_creation(self, sample_security_issues):
        """Test audit result creation."""
        result = SecurityAuditResult(
            timestamp="20231201_120000",
            success=True,
            issues=sample_security_issues,
            tools_run=["bandit", "safety", "pip-audit"],
            errors=[],
        )

        assert result.timestamp == "20231201_120000"
        assert result.success is True
        assert len(result.issues) == 3
        assert result.tools_run == ["bandit", "safety", "pip-audit"]
        assert result.errors == []

    def test_count_by_severity(self, sample_security_issues):
        """Test counting issues by severity."""
        result = SecurityAuditResult(
            timestamp="20231201_120000", success=True, issues=sample_security_issues
        )

        counts = result.count_by_severity()

        assert counts["low"] == 0
        assert counts["medium"] == 1
        assert counts["high"] == 1
        assert counts["critical"] == 1

    def test_has_critical_issues(self, sample_security_issues):
        """Test checking for critical issues."""
        result = SecurityAuditResult(
            timestamp="20231201_120000", success=True, issues=sample_security_issues
        )

        assert result.has_critical_issues() is True

        # Test without critical issues
        non_critical_issues = [
            issue
            for issue in sample_security_issues
            if issue.severity != VulnerabilityLevel.CRITICAL
        ]
        result_no_critical = SecurityAuditResult(
            timestamp="20231201_120000", success=True, issues=non_critical_issues
        )

        assert result_no_critical.has_critical_issues() is False

    def test_has_high_issues(self, sample_security_issues):
        """Test checking for high severity issues."""
        result = SecurityAuditResult(
            timestamp="20231201_120000", success=True, issues=sample_security_issues
        )

        assert result.has_high_issues() is True


class TestSecurityAuditor:
    """Test security auditor."""

    def test_auditor_initialization(self, security_config):
        """Test auditor initialization."""
        auditor = SecurityAuditor(security_config)

        assert auditor.config == security_config
        assert auditor.config.enabled is True

    def test_auditor_disabled(self):
        """Test auditor with disabled security."""
        config = SecurityConfig(enabled=False)
        auditor = SecurityAuditor(config)

        assert not auditor.config.enabled

    @pytest.mark.asyncio
    async def test_full_audit_disabled(self):
        """Test full audit when disabled."""
        config = SecurityConfig(enabled=False)
        auditor = SecurityAuditor(config)

        result = await auditor.run_full_audit()

        assert result.success is True
        assert len(result.tools_run) == 0
        assert len(result.issues) == 0

    @pytest.mark.asyncio
    async def test_run_command(self, security_config):
        """Test running shell commands."""
        auditor = SecurityAuditor(security_config)

        # Test successful command
        process = await auditor._run_command(["echo", "test"])

        assert process.returncode == 0
        assert "test" in process.stdout

    @pytest.mark.asyncio
    async def test_run_bandit_not_installed(self, security_config):
        """Test bandit when not installed."""
        auditor = SecurityAuditor(security_config)

        with patch.object(auditor, "_run_command") as mock_run:
            mock_run.side_effect = FileNotFoundError("bandit not found")

            issues = await auditor._run_bandit(".")

            assert len(issues) == 0

    @pytest.mark.asyncio
    async def test_run_bandit_with_results(self, security_config):
        """Test bandit with mock results."""
        auditor = SecurityAuditor(security_config)

        # Mock bandit output
        bandit_output = {
            "results": [
                {
                    "test_name": "hardcoded_password",
                    "issue_text": "Possible hardcoded password",
                    "issue_severity": "HIGH",
                    "filename": "/app/config.py",
                    "line_number": 42,
                    "test_id": "B106",
                }
            ]
        }

        mock_process = MagicMock()
        mock_process.returncode = 1  # Issues found
        mock_process.stdout = json.dumps(bandit_output)
        mock_process.stderr = ""

        with patch.object(auditor, "_run_command", return_value=mock_process):
            issues = await auditor._run_bandit(".")

            assert len(issues) == 1
            assert issues[0].tool == "bandit"
            assert issues[0].severity == VulnerabilityLevel.HIGH
            assert issues[0].title == "hardcoded_password"
            assert issues[0].file_path == "/app/config.py"
            assert issues[0].line_number == 42

    @pytest.mark.asyncio
    async def test_run_safety_with_results(self, security_config):
        """Test safety with mock results."""
        auditor = SecurityAuditor(security_config)

        # Mock safety output
        safety_output = [
            {
                "package": "requests",
                "installed_version": "2.25.0",
                "advisory": "Known vulnerability in requests",
                "id": "12345",
                "more_info_url": "https://pyup.io/12345",
            }
        ]

        mock_process = MagicMock()
        mock_process.returncode = 64  # Vulnerabilities found
        mock_process.stdout = json.dumps(safety_output)
        mock_process.stderr = ""

        with patch.object(auditor, "_run_command", return_value=mock_process):
            issues = await auditor._run_safety()

            assert len(issues) == 1
            assert issues[0].tool == "safety"
            assert issues[0].severity == VulnerabilityLevel.HIGH
            assert issues[0].package == "requests"
            assert issues[0].affected_version == "2.25.0"

    @pytest.mark.asyncio
    async def test_run_pip_audit_with_results(self, security_config):
        """Test pip-audit with mock results."""
        auditor = SecurityAuditor(security_config)

        # Mock pip-audit output
        pip_audit_output = {
            "dependencies": [
                {
                    "name": "flask",
                    "version": "1.0.0",
                    "vulns": [
                        {
                            "id": "CVE-2020-1234",
                            "description": "XSS vulnerability",
                            "fix_versions": ["1.1.4"],
                            "aliases": ["GHSA-1234"],
                            "cvss": {"score": 7.5},
                        }
                    ],
                }
            ]
        }

        mock_process = MagicMock()
        mock_process.returncode = 1  # Vulnerabilities found
        mock_process.stdout = json.dumps(pip_audit_output)
        mock_process.stderr = ""

        with patch.object(auditor, "_run_command", return_value=mock_process):
            issues = await auditor._run_pip_audit()

            assert len(issues) == 1
            assert issues[0].tool == "pip-audit"
            assert issues[0].severity == VulnerabilityLevel.HIGH  # Score 7.5
            assert issues[0].package == "flask"
            assert issues[0].affected_version == "1.0.0"
            assert issues[0].fixed_version == "1.1.4"

    @pytest.mark.asyncio
    async def test_save_results(self, security_config, sample_security_issues):
        """Test saving audit results."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SecurityConfig(output_dir=temp_dir, json_output=True)
            auditor = SecurityAuditor(config)

            result = SecurityAuditResult(
                timestamp="20231201_120000",
                success=True,
                issues=sample_security_issues,
                tools_run=["bandit", "safety"],
                errors=[],
            )

            await auditor._save_results(result)

            # Check that file was created
            json_file = Path(temp_dir) / "security_audit_20231201_120000.json"
            assert json_file.exists()

            # Verify content
            with open(json_file) as f:
                saved_data = json.load(f)

            assert saved_data["timestamp"] == "20231201_120000"
            assert saved_data["success"] is True
            assert len(saved_data["issues"]) == 3
            assert saved_data["tools_run"] == ["bandit", "safety"]

    @pytest.mark.asyncio
    async def test_full_audit_with_mocked_tools(self, security_config):
        """Test full audit with mocked security tools."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SecurityConfig(
                output_dir=temp_dir,
                fail_on_critical=False,  # Don't fail for test
                bandit_enabled=True,
                safety_enabled=True,
                pip_audit_enabled=True,
            )
            auditor = SecurityAuditor(config)

            # Mock all tool methods
            with patch.object(auditor, "_run_bandit", return_value=[]):
                with patch.object(auditor, "_run_safety", return_value=[]):
                    with patch.object(auditor, "_run_pip_audit", return_value=[]):
                        result = await auditor.run_full_audit()

            assert result.success is True
            assert "bandit" in result.tools_run
            assert "safety" in result.tools_run
            assert "pip-audit" in result.tools_run
            assert len(result.issues) == 0

    @pytest.mark.asyncio
    async def test_full_audit_with_critical_issues(self, security_config, sample_security_issues):
        """Test full audit with critical issues and fail_on_critical."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SecurityConfig(
                output_dir=temp_dir,
                fail_on_critical=True,
                bandit_enabled=True,  # Enable bandit to trigger the mock
                safety_enabled=False,
                pip_audit_enabled=False,
            )
            auditor = SecurityAuditor(config)

            # Mock to return critical issues
            with patch.object(auditor, "_run_bandit", return_value=sample_security_issues):
                result = await auditor.run_full_audit()

            # Should fail due to critical issues
            assert result.success is False
            assert result.has_critical_issues() is True


class TestConvenienceFunction:
    """Test convenience functions."""

    @pytest.mark.asyncio
    async def test_run_security_audit(self, security_config):
        """Test run_security_audit convenience function."""
        with patch("eoms.core.security.SecurityAuditor") as mock_auditor:
            mock_instance = mock_auditor.return_value
            mock_result = SecurityAuditResult(timestamp="20231201_120000", success=True)
            mock_instance.run_full_audit = AsyncMock(return_value=mock_result)

            result = await run_security_audit(security_config, ".")

            assert result == mock_result
            mock_auditor.assert_called_once_with(security_config)
            mock_instance.run_full_audit.assert_called_once_with(".")


class TestVulnerabilityLevels:
    """Test vulnerability level enumeration."""

    def test_vulnerability_levels(self):
        """Test vulnerability level values."""
        assert VulnerabilityLevel.LOW.value == "low"
        assert VulnerabilityLevel.MEDIUM.value == "medium"
        assert VulnerabilityLevel.HIGH.value == "high"
        assert VulnerabilityLevel.CRITICAL.value == "critical"


class TestRealWorldScenarios:
    """Test real-world security audit scenarios."""

    @pytest.mark.asyncio
    async def test_mixed_tool_results(self):
        """Test audit with mixed results from different tools."""
        config = SecurityConfig(
            enabled=True,
            fail_on_critical=False,
            bandit_enabled=True,
            safety_enabled=True,
            pip_audit_enabled=True,
        )
        auditor = SecurityAuditor(config)

        # Mock different results from each tool
        bandit_issues = [
            SecurityIssue(
                tool="bandit",
                severity=VulnerabilityLevel.MEDIUM,
                title="Weak cryptography",
                description="MD5 hash detected",
            )
        ]

        safety_issues = [
            SecurityIssue(
                tool="safety",
                severity=VulnerabilityLevel.HIGH,
                title="Vulnerable requests",
                description="CVE in requests package",
                package="requests",
            )
        ]

        pip_audit_issues = []  # No issues from pip-audit

        with patch.object(auditor, "_run_bandit", return_value=bandit_issues):
            with patch.object(auditor, "_run_safety", return_value=safety_issues):
                with patch.object(auditor, "_run_pip_audit", return_value=pip_audit_issues):
                    result = await auditor.run_full_audit()

        assert result.success is True
        assert len(result.issues) == 2
        assert len(result.tools_run) == 3

        # Check severity distribution
        counts = result.count_by_severity()
        assert counts["medium"] == 1
        assert counts["high"] == 1
        assert counts["critical"] == 0

    @pytest.mark.asyncio
    async def test_tool_failure_handling(self):
        """Test handling of tool failures."""
        config = SecurityConfig(
            enabled=True,
            fail_on_critical=False,
            bandit_enabled=True,
            safety_enabled=True,
            pip_audit_enabled=True,
        )
        auditor = SecurityAuditor(config)

        # Mock bandit to succeed, safety to fail, pip-audit to succeed
        with patch.object(auditor, "_run_bandit", return_value=[]):
            with patch.object(auditor, "_run_safety", side_effect=Exception("Safety failed")):
                with patch.object(auditor, "_run_pip_audit", return_value=[]):
                    result = await auditor.run_full_audit()

        # Should not be completely successful due to safety failure
        assert result.success is False
        assert len(result.errors) == 1
        assert "Safety scan failed" in result.errors[0]
        assert "bandit" in result.tools_run
        assert "safety" not in result.tools_run  # Failed tool not included
        assert "pip-audit" in result.tools_run
