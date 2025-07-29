"""
Data models for Xmemo - AI Agent Execution Reflection Tool.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Agent execution status."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


class ProblemSeverity(str, Enum):
    """Problem severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProblemCategory(str, Enum):
    """Problem categories."""

    LOGIC_ERROR = "logic_error"
    DATA_ISSUE = "data_issue"
    API_ERROR = "api_error"
    TIMEOUT = "timeout"
    RESOURCE_LIMIT = "resource_limit"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    PERFORMANCE = "performance"
    USER_INPUT = "user_input"
    OTHER = "other"


class SuccessCategory(str, Enum):
    """Success experience categories."""

    EFFICIENT_SOLUTION = "efficient_solution"
    CREATIVE_APPROACH = "creative_approach"
    ERROR_RECOVERY = "error_recovery"
    OPTIMIZATION = "optimization"
    BEST_PRACTICE = "best_practice"
    NOVEL_PATTERN = "novel_pattern"
    USER_SATISFACTION = "user_satisfaction"
    OTHER = "other"


class ExecutionStep(BaseModel):
    """A single step in agent execution."""

    step_id: str
    name: str
    description: Optional[str] = None
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Problem(BaseModel):
    """A problem encountered during execution."""

    problem_id: str = Field(
        default_factory=lambda: f"prob_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    category: ProblemCategory
    severity: ProblemSeverity
    title: str
    description: str
    step_id: Optional[str] = None  # Which step this problem occurred in
    error_details: Optional[str] = None
    impact_assessment: str
    suggested_solutions: List[str] = Field(default_factory=list)
    root_cause: Optional[str] = None
    frequency: int = Field(default=1)  # How often this problem occurs
    first_seen: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    resolved: bool = Field(default=False)
    resolution_notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SuccessExperience(BaseModel):
    """A successful experience or pattern."""

    experience_id: str = Field(
        default_factory=lambda: f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    category: SuccessCategory
    title: str
    description: str
    step_id: Optional[str] = None  # Which step this success occurred in
    approach_details: str
    benefits: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(
        default_factory=list
    )  # Under what conditions this works
    reusability_score: float = Field(
        ge=0.0, le=1.0, default=0.5
    )  # How reusable is this experience
    performance_impact: Optional[str] = None
    lessons_learned: List[str] = Field(default_factory=list)
    frequency: int = Field(default=1)  # How often this pattern is successful
    first_seen: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentExecution(BaseModel):
    """Complete record of an agent execution."""

    execution_id: str
    agent_name: str
    agent_version: Optional[str] = None
    task_description: str
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    total_duration_ms: Optional[int] = None
    steps: List[ExecutionStep] = Field(default_factory=list)
    final_output: Dict[str, Any] = Field(default_factory=dict)
    success_metrics: Dict[str, float] = Field(default_factory=dict)
    resource_usage: Dict[str, Any] = Field(default_factory=dict)
    environment: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_step(self, step: ExecutionStep) -> None:
        """Add an execution step."""
        self.steps.append(step)

    def get_failed_steps(self) -> List[ExecutionStep]:
        """Get all failed steps."""
        return [step for step in self.steps if step.status == ExecutionStatus.FAILED]

    def get_successful_steps(self) -> List[ExecutionStep]:
        """Get all successful steps."""
        return [step for step in self.steps if step.status == ExecutionStatus.SUCCESS]

    def calculate_success_rate(self) -> float:
        """Calculate overall success rate."""
        if not self.steps:
            return 0.0
        successful = len(self.get_successful_steps())
        return successful / len(self.steps)


class ReflectionInsight(BaseModel):
    """An insight generated from reflection."""

    insight_id: str = Field(
        default_factory=lambda: f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    type: str  # "problem_pattern", "success_pattern", "improvement_opportunity", "risk_assessment"
    title: str
    description: str
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_evidence: List[str] = Field(default_factory=list)
    actionable_recommendations: List[str] = Field(default_factory=list)
    priority: str = Field(default="medium")  # "low", "medium", "high", "critical"
    relevant_executions: List[str] = Field(default_factory=list)  # execution_ids
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ReflectionResult(BaseModel):
    """Result of reflection analysis on agent execution(s)."""

    reflection_id: str = Field(
        default_factory=lambda: f"refl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    execution_ids: List[str]  # Executions analyzed
    problems_identified: List[Problem] = Field(default_factory=list)
    success_experiences: List[SuccessExperience] = Field(default_factory=list)
    insights: List[ReflectionInsight] = Field(default_factory=list)
    summary: str
    overall_assessment: str
    improvement_priorities: List[str] = Field(default_factory=list)
    success_patterns: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    reflection_timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def get_critical_problems(self) -> List[Problem]:
        """Get critical problems."""
        return [
            p
            for p in self.problems_identified
            if p.severity == ProblemSeverity.CRITICAL
        ]

    def get_high_value_experiences(self) -> List[SuccessExperience]:
        """Get high-value success experiences."""
        return [e for e in self.success_experiences if e.reusability_score >= 0.7]

    def get_actionable_insights(self) -> List[ReflectionInsight]:
        """Get insights with actionable recommendations."""
        return [i for i in self.insights if i.actionable_recommendations]


class ExecutionContext(BaseModel):
    """Context information for agent execution."""

    user_id: Optional[str] = None
    session_id: Optional[str] = None
    environment: str = "production"
    agent_config: Dict[str, Any] = Field(default_factory=dict)
    external_dependencies: List[str] = Field(default_factory=list)
    resource_constraints: Dict[str, Any] = Field(default_factory=dict)
    business_context: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
