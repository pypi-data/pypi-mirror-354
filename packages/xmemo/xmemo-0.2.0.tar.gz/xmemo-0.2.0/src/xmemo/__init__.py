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
    LangGraphEdgeType,
    LangGraphExecution,
    LangGraphNode,
    LangGraphNodeType,
    LangGraphState,
    Problem,
    ProblemCategory,
    ProblemSeverity,
    ReflectionInsight,
    ReflectionResult,
    SuccessCategory,
    SuccessExperience,
)
from .reflection import ExecutionReflectionEngine

# Optional LangGraph integration
try:
    from .langgraph_tracker import LangGraphTracker
except ImportError:
    # LangGraph not available
    LangGraphTracker = None

__version__ = "0.2.0"

# Core exports for agent execution reflection
__all__ = [
    # Core classes
    "ExecutionAnalyzer",
    "ExecutionReflectionEngine",
    "LangGraphTracker",
    # Data models
    "AgentExecution",
    "ExecutionStep",
    "ExecutionContext",
    "LangGraphExecution",
    "LangGraphNode",
    "LangGraphState",
    "Problem",
    "SuccessExperience",
    "ReflectionResult",
    "ReflectionInsight",
    # Enums
    "ExecutionStatus",
    "LangGraphNodeType",
    "LangGraphEdgeType",
    "ProblemSeverity",
    "ProblemCategory",
    "SuccessCategory",
]
