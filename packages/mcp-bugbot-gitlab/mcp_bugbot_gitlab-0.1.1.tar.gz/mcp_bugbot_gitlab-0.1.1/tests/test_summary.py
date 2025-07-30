import pytest
from mcp_bugbot_gitlab.resources import generate_review_summary

def test_generate_review_summary_no_findings():
    summary = generate_review_summary([])
    assert "Strengths:\n- None noted." in summary
    assert "Concerns/Suggestions:\n- None noted." in summary

def test_generate_review_summary_only_suggestions():
    findings = [
        {"type": "suggestion", "severity": "low", "file": "main.py", "line": 2, "message": "Minor suggestion."}
    ]
    summary = generate_review_summary(findings)
    assert "Minor suggestion." in summary
    assert "Approve with minor suggestions" in summary

def test_generate_review_summary_high_severity():
    findings = [
        {"type": "security", "severity": "high", "file": "main.py", "line": 1, "message": "Critical issue."}
    ]
    summary = generate_review_summary(findings)
    assert "Critical issue." in summary
    assert "Request changes" in summary

def test_generate_review_summary_only_strengths():
    findings = [
        {"type": "testing", "severity": "info", "file": "main.py", "line": 1, "message": "Great test coverage."}
    ]
    summary = generate_review_summary(findings)
    assert "Great test coverage." in summary
    assert "Approve with minor suggestions" in summary
    assert "Concerns/Suggestions:\n- None noted." in summary

def test_generate_review_summary_only_concerns():
    findings = [
        {"type": "bug", "severity": "medium", "file": "main.py", "line": 1, "message": "Potential bug."}
    ]
    summary = generate_review_summary(findings)
    assert "Potential bug." in summary
    assert "Approve with suggestions" in summary
    assert "Strengths:\n- None noted." in summary

def test_generate_review_summary_mixed_severities():
    findings = [
        {"type": "bug", "severity": "medium", "file": "main.py", "line": 1, "message": "Potential bug."},
        {"type": "suggestion", "severity": "low", "file": "main.py", "line": 2, "message": "Minor suggestion."}
    ]
    summary = generate_review_summary(findings)
    assert "Potential bug." in summary
    assert "Minor suggestion." in summary
    assert "Approve with suggestions" in summary

def test_generate_review_summary_no_strengths_no_concerns():
    findings = []
    summary = generate_review_summary(findings)
    assert "Strengths:\n- None noted." in summary
    assert "Concerns/Suggestions:\n- None noted." in summary 