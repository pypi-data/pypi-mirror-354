"""
Xmemo - AI Agent Execution Reflection Tool.

This package provides tools for recording agent execution data,
analyzing performance patterns, identifying problems and success experiences,
and generating actionable insights for continuous improvement.

Key Components:
- ExecutionAnalyzer: Analyzes agent execution performance and patterns
- ExecutionReflectionEngine: Generates insights and recommendations
- Agent execution models: Data structures for tracking execution data
- Problem and success tracking: Identify issues and successful patterns
"""

from .analyzer import ExecutionAnalyzer
from .models import (
    AgentExecution,
    ExecutionContext,
    ExecutionStatus,
    ExecutionStep,
    Problem,
    ProblemCategory,
    ProblemSeverity,
    ReflectionInsight,
    ReflectionResult,
    SuccessCategory,
    SuccessExperience,
)
from .reflection import ExecutionReflectionEngine

__version__ = "0.1.11"

# Core exports for agent execution reflection
__all__ = [
    # Core classes
    "ExecutionAnalyzer",
    "ExecutionReflectionEngine",
    # Data models
    "AgentExecution",
    "ExecutionStep",
    "ExecutionContext",
    "Problem",
    "SuccessExperience",
    "ReflectionResult",
    "ReflectionInsight",
    # Enums
    "ExecutionStatus",
    "ProblemSeverity",
    "ProblemCategory",
    "SuccessCategory",
]
