"""Security audit tools for EOMS.

This module provides comprehensive security scanning and vulnerability
assessment capabilities for the EOMS trading system.
"""

import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

__all__ = [
    "SecurityConfig",
    "VulnerabilityLevel",
    "SecurityIssue",
    "SecurityAuditResult",
    "SecurityAuditor",
    "run_security_audit",
]


class VulnerabilityLevel(Enum):
    """Security vulnerability severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityIssue:
    """Represents a security issue found during audit."""

    tool: str
    severity: VulnerabilityLevel
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    cwe_id: Optional[str] = None
    cve_id: Optional[str] = None
    package: Optional[str] = None
    affected_version: Optional[str] = None
    fixed_version: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class SecurityAuditResult:
    """Results of a security audit run."""

    timestamp: str
    success: bool
    issues: List[SecurityIssue] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    tools_run: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def count_by_severity(self) -> Dict[str, int]:
        """Count issues by severity level."""
        counts = {level.value: 0 for level in VulnerabilityLevel}
        for issue in self.issues:
            counts[issue.severity.value] += 1
        return counts

    def has_critical_issues(self) -> bool:
        """Check if there are any critical security issues."""
        return any(issue.severity == VulnerabilityLevel.CRITICAL for issue in self.issues)

    def has_high_issues(self) -> bool:
        """Check if there are any high severity issues."""
        return any(issue.severity == VulnerabilityLevel.HIGH for issue in self.issues)


@dataclass
class SecurityConfig:
    """Configuration for security auditing."""

    enabled: bool = True
    fail_on_critical: bool = True
    fail_on_high: bool = False
    max_issues: int = 100

    # Tool configurations
    bandit_enabled: bool = True
    bandit_config_file: Optional[str] = None
    bandit_exclude_dirs: List[str] = field(
        default_factory=lambda: ["tests", ".venv", "node_modules"]
    )

    safety_enabled: bool = True
    safety_ignore_vulns: List[str] = field(default_factory=list)

    pip_audit_enabled: bool = True
    pip_audit_ignore_vulns: List[str] = field(default_factory=list)

    # Output configuration
    output_dir: str = "security_reports"
    json_output: bool = True
    html_output: bool = False


class SecurityAuditor:
    """Main security auditing orchestrator."""

    def __init__(self, config: Optional[SecurityConfig] = None):
        """Initialize security auditor.

        Args:
            config: Security audit configuration
        """
        self.config = config or SecurityConfig()
        self.logger = logging.getLogger(__name__)

        if not self.config.enabled:
            self.logger.info("Security auditing disabled")

    async def run_full_audit(self, target_path: str = ".") -> SecurityAuditResult:
        """Run complete security audit.

        Args:
            target_path: Path to audit (default: current directory)

        Returns:
            Complete audit results
        """
        if not self.config.enabled:
            self.logger.info("Security audit skipped - disabled")
            return SecurityAuditResult(timestamp=self._get_timestamp(), success=True, tools_run=[])

        self.logger.info("Starting comprehensive security audit")

        result = SecurityAuditResult(
            timestamp=self._get_timestamp(), success=True, tools_run=[], errors=[]
        )

        # Ensure output directory exists
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(exist_ok=True)

        # Run individual tools
        if self.config.bandit_enabled:
            try:
                bandit_issues = await self._run_bandit(target_path)
                result.issues.extend(bandit_issues)
                result.tools_run.append("bandit")
                self.logger.info(f"Bandit found {len(bandit_issues)} issues")
            except Exception as e:
                error_msg = f"Bandit scan failed: {e}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
                result.success = False

        if self.config.safety_enabled:
            try:
                safety_issues = await self._run_safety()
                result.issues.extend(safety_issues)
                result.tools_run.append("safety")
                self.logger.info(f"Safety found {len(safety_issues)} issues")
            except Exception as e:
                error_msg = f"Safety scan failed: {e}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
                result.success = False

        if self.config.pip_audit_enabled:
            try:
                pip_audit_issues = await self._run_pip_audit()
                result.issues.extend(pip_audit_issues)
                result.tools_run.append("pip-audit")
                self.logger.info(f"pip-audit found {len(pip_audit_issues)} issues")
            except Exception as e:
                error_msg = f"pip-audit scan failed: {e}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
                result.success = False

        # Generate summary
        result.summary = result.count_by_severity()

        # Check failure conditions
        if self.config.fail_on_critical and result.has_critical_issues():
            result.success = False
            self.logger.error("Audit failed due to critical security issues")

        if self.config.fail_on_high and result.has_high_issues():
            result.success = False
            self.logger.error("Audit failed due to high severity security issues")

        # Save results
        await self._save_results(result)

        self._log_summary(result)

        return result

    async def _run_bandit(self, target_path: str) -> List[SecurityIssue]:
        """Run Bandit security scanner.

        Args:
            target_path: Path to scan

        Returns:
            List of security issues found
        """
        issues = []

        try:
            cmd = ["bandit", "-r", target_path, "-f", "json"]

            # Add configuration file if specified
            if self.config.bandit_config_file:
                cmd.extend(["-c", self.config.bandit_config_file])

            # Add exclude directories
            if self.config.bandit_exclude_dirs:
                exclude_pattern = ",".join(self.config.bandit_exclude_dirs)
                cmd.extend(["--exclude", exclude_pattern])

            self.logger.debug(f"Running: {' '.join(cmd)}")

            # Run bandit
            process = await self._run_command(cmd)

            if process.returncode not in [0, 1]:  # 1 is expected when issues are found
                raise RuntimeError(
                    f"Bandit failed with return code {process.returncode}: {process.stderr}"
                )

            if process.stdout:
                bandit_result = json.loads(process.stdout)

                # Parse results
                for result in bandit_result.get("results", []):
                    severity_map = {
                        "LOW": VulnerabilityLevel.LOW,
                        "MEDIUM": VulnerabilityLevel.MEDIUM,
                        "HIGH": VulnerabilityLevel.HIGH,
                    }

                    severity = severity_map.get(
                        result.get("issue_severity", "MEDIUM"),
                        VulnerabilityLevel.MEDIUM,
                    )

                    issue = SecurityIssue(
                        tool="bandit",
                        severity=severity,
                        title=result.get("test_name", "Security Issue"),
                        description=result.get("issue_text", ""),
                        file_path=result.get("filename"),
                        line_number=result.get("line_number"),
                        cwe_id=result.get("test_id"),
                    )
                    issues.append(issue)

        except FileNotFoundError:
            self.logger.warning("Bandit not found - install with: pip install bandit")
        except Exception as e:
            self.logger.error(f"Bandit scan error: {e}")
            raise

        return issues

    async def _run_safety(self) -> List[SecurityIssue]:
        """Run Safety vulnerability scanner.

        Returns:
            List of security issues found
        """
        issues = []

        try:
            cmd = ["safety", "check", "--json"]

            # Add ignored vulnerabilities
            if self.config.safety_ignore_vulns:
                for vuln_id in self.config.safety_ignore_vulns:
                    cmd.extend(["--ignore", vuln_id])

            self.logger.debug(f"Running: {' '.join(cmd)}")

            process = await self._run_command(cmd)

            if process.returncode not in [0, 64]:  # 64 indicates vulnerabilities found
                raise RuntimeError(
                    f"Safety failed with return code {process.returncode}: {process.stderr}"
                )

            if process.stdout:
                safety_result = json.loads(process.stdout)

                # Parse vulnerabilities
                for vuln in safety_result:
                    issue = SecurityIssue(
                        tool="safety",
                        # Safety reports are generally high severity
                        severity=VulnerabilityLevel.HIGH,
                        title=f"Vulnerable package: {vuln.get('package')}",
                        description=vuln.get("advisory", ""),
                        package=vuln.get("package"),
                        affected_version=vuln.get("installed_version"),
                        cve_id=vuln.get("id"),
                        references=[vuln.get("more_info_url", "")],
                    )
                    issues.append(issue)

        except FileNotFoundError:
            self.logger.warning("Safety not found - install with: pip install safety")
        except Exception as e:
            self.logger.error(f"Safety scan error: {e}")
            raise

        return issues

    async def _run_pip_audit(self) -> List[SecurityIssue]:
        """Run pip-audit vulnerability scanner.

        Returns:
            List of security issues found
        """
        issues = []

        try:
            cmd = ["pip-audit", "--format", "json"]

            # Add ignored vulnerabilities
            if self.config.pip_audit_ignore_vulns:
                for vuln_id in self.config.pip_audit_ignore_vulns:
                    cmd.extend(["--ignore-vuln", vuln_id])

            self.logger.debug(f"Running: {' '.join(cmd)}")

            process = await self._run_command(cmd)

            if process.returncode not in [0, 1]:  # 1 indicates vulnerabilities found
                raise RuntimeError(
                    f"pip-audit failed with return code {process.returncode}: {process.stderr}"
                )

            if process.stdout:
                audit_result = json.loads(process.stdout)

                # Parse vulnerabilities
                for entry in audit_result.get("dependencies", []):
                    for vuln in entry.get("vulns", []):
                        # Determine severity based on CVSS score if available
                        severity = VulnerabilityLevel.MEDIUM
                        if "cvss" in vuln:
                            score = vuln.get("cvss", {}).get("score", 0)
                            if score >= 9.0:
                                severity = VulnerabilityLevel.CRITICAL
                            elif score >= 7.0:
                                severity = VulnerabilityLevel.HIGH
                            elif score >= 4.0:
                                severity = VulnerabilityLevel.MEDIUM
                            else:
                                severity = VulnerabilityLevel.LOW

                        issue = SecurityIssue(
                            tool="pip-audit",
                            severity=severity,
                            title=f"Vulnerable package: {entry.get('name')}",
                            description=vuln.get("description", ""),
                            package=entry.get("name"),
                            affected_version=entry.get("version"),
                            fixed_version=(
                                vuln.get("fix_versions", [None])[0]
                                if vuln.get("fix_versions")
                                else None
                            ),
                            cve_id=vuln.get("id"),
                            references=vuln.get("aliases", []),
                        )
                        issues.append(issue)

        except FileNotFoundError:
            self.logger.warning("pip-audit not found - install with: pip install pip-audit")
        except Exception as e:
            self.logger.error(f"pip-audit scan error: {e}")
            raise

        return issues

    async def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Run a shell command asynchronously.

        Args:
            cmd: Command and arguments

        Returns:
            Completed process result
        """
        import asyncio

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        # Decode bytes to text
        stdout_text = stdout.decode("utf-8") if stdout else ""
        stderr_text = stderr.decode("utf-8") if stderr else ""

        # Create a CompletedProcess-like object
        class ProcessResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        return ProcessResult(process.returncode, stdout_text, stderr_text)

    async def _save_results(self, result: SecurityAuditResult) -> None:
        """Save audit results to files.

        Args:
            result: Audit results to save
        """
        output_dir = Path(self.config.output_dir)

        if self.config.json_output:
            json_file = output_dir / f"security_audit_{result.timestamp}.json"

            # Convert result to JSON-serializable format
            result_dict = {
                "timestamp": result.timestamp,
                "success": result.success,
                "summary": result.summary,
                "tools_run": result.tools_run,
                "errors": result.errors,
                "issues": [
                    {
                        "tool": issue.tool,
                        "severity": issue.severity.value,
                        "title": issue.title,
                        "description": issue.description,
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "cwe_id": issue.cwe_id,
                        "cve_id": issue.cve_id,
                        "package": issue.package,
                        "affected_version": issue.affected_version,
                        "fixed_version": issue.fixed_version,
                        "references": issue.references,
                    }
                    for issue in result.issues
                ],
            }

            with open(json_file, "w") as f:
                json.dump(result_dict, f, indent=2)

            self.logger.info(f"Security audit results saved to {json_file}")

    def _log_summary(self, result: SecurityAuditResult) -> None:
        """Log audit summary.

        Args:
            result: Audit results to summarize
        """
        self.logger.info("=== Security Audit Summary ===")
        self.logger.info(f"Tools run: {', '.join(result.tools_run)}")
        self.logger.info(f"Total issues found: {len(result.issues)}")

        for severity, count in result.summary.items():
            if count > 0:
                level_name = severity.upper()
                self.logger.info(f"  {level_name}: {count}")

        if result.errors:
            self.logger.warning(f"Errors encountered: {len(result.errors)}")
            for error in result.errors:
                self.logger.warning(f"  - {error}")

        if result.success:
            self.logger.info("✓ Security audit completed successfully")
        else:
            self.logger.error("✗ Security audit failed")

    def _get_timestamp(self) -> str:
        """Get current timestamp for file naming."""
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")


async def run_security_audit(
    config: Optional[SecurityConfig] = None, target_path: str = "."
) -> SecurityAuditResult:
    """Convenience function to run security audit.

    Args:
        config: Security audit configuration
        target_path: Path to audit

    Returns:
        Audit results
    """
    auditor = SecurityAuditor(config)
    return await auditor.run_full_audit(target_path)


# CLI integration for running audits
def main():
    """Main entry point for command-line security auditing."""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="EOMS Security Auditor")
    parser.add_argument("--target", default=".", help="Target path to audit")
    parser.add_argument("--config", help="Configuration file")
    parser.add_argument(
        "--fail-on-critical", action="store_true", help="Fail if critical issues found"
    )
    parser.add_argument(
        "--fail-on-high", action="store_true", help="Fail if high severity issues found"
    )
    parser.add_argument(
        "--output-dir", default="security_reports", help="Output directory for reports"
    )

    args = parser.parse_args()

    # Create configuration
    config = SecurityConfig(
        fail_on_critical=args.fail_on_critical,
        fail_on_high=args.fail_on_high,
        output_dir=args.output_dir,
    )

    # Run audit
    async def run_audit():
        result = await run_security_audit(config, args.target)
        return result.success

    success = asyncio.run(run_audit())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
