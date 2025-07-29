"""
Agent Execution Reflection Engine for Xmemo.

This module provides tools for analyzing agent executions, identifying problems,
extracting success experiences, and generating actionable insights.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from .models import (
    AgentExecution,
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


class ExecutionReflectionEngine:
    """
    Engine for analyzing agent executions and generating reflective insights.
    """

    def __init__(self):
        """Initialize the reflection engine."""
        self.problem_patterns = self._setup_problem_patterns()
        self.success_patterns = self._setup_success_patterns()

    def reflect_on_execution(
        self, execution: AgentExecution, context: Optional[Dict[str, Any]] = None
    ) -> ReflectionResult:
        """
        Perform reflection on a single agent execution.

        Args:
            execution: The agent execution to analyze
            context: Optional context information

        Returns:
            ReflectionResult containing problems, successes, and insights
        """
        problems = self._analyze_problems(execution)
        successes = self._analyze_successes(execution)
        insights = self._generate_insights([execution], problems, successes)

        summary = self._generate_summary(execution, problems, successes)
        assessment = self._generate_assessment(execution, problems, successes)

        return ReflectionResult(
            execution_ids=[execution.execution_id],
            problems_identified=problems,
            success_experiences=successes,
            insights=insights,
            summary=summary,
            overall_assessment=assessment,
            improvement_priorities=self._prioritize_improvements(problems, insights),
            success_patterns=self._extract_success_patterns(successes),
            risk_factors=self._identify_risk_factors(problems),
            confidence_score=self._calculate_confidence_score(
                [execution], problems, successes
            ),
            metadata=context or {},
        )

    def reflect_on_multiple_executions(
        self, executions: List[AgentExecution], context: Optional[Dict[str, Any]] = None
    ) -> ReflectionResult:
        """
        Perform reflection on multiple agent executions to identify patterns.

        Args:
            executions: List of agent executions to analyze
            context: Optional context information

        Returns:
            ReflectionResult containing aggregated analysis
        """
        all_problems = []
        all_successes = []

        for execution in executions:
            problems = self._analyze_problems(execution)
            successes = self._analyze_successes(execution)
            all_problems.extend(problems)
            all_successes.extend(successes)

        # Aggregate similar problems and successes
        aggregated_problems = self._aggregate_problems(all_problems)
        aggregated_successes = self._aggregate_successes(all_successes)

        insights = self._generate_insights(
            executions, aggregated_problems, aggregated_successes
        )

        summary = self._generate_multi_execution_summary(
            executions, aggregated_problems, aggregated_successes
        )
        assessment = self._generate_multi_execution_assessment(
            executions, aggregated_problems, aggregated_successes
        )

        return ReflectionResult(
            execution_ids=[e.execution_id for e in executions],
            problems_identified=aggregated_problems,
            success_experiences=aggregated_successes,
            insights=insights,
            summary=summary,
            overall_assessment=assessment,
            improvement_priorities=self._prioritize_improvements(
                aggregated_problems, insights
            ),
            success_patterns=self._extract_success_patterns(aggregated_successes),
            risk_factors=self._identify_risk_factors(aggregated_problems),
            confidence_score=self._calculate_confidence_score(
                executions, aggregated_problems, aggregated_successes
            ),
            metadata=context or {},
        )

    def _analyze_problems(self, execution: AgentExecution) -> List[Problem]:
        """Analyze an execution for problems."""
        problems = []

        # Analyze failed steps
        failed_steps = execution.get_failed_steps()
        for step in failed_steps:
            problem = self._create_problem_from_failed_step(execution, step)
            if problem:
                problems.append(problem)

        # Analyze performance issues
        performance_problems = self._analyze_performance_issues(execution)
        problems.extend(performance_problems)

        # Analyze pattern-based problems
        pattern_problems = self._analyze_pattern_problems(execution)
        problems.extend(pattern_problems)

        return problems

    def _analyze_successes(self, execution: AgentExecution) -> List[SuccessExperience]:
        """Analyze an execution for success experiences."""
        successes = []

        # Analyze successful steps
        successful_steps = execution.get_successful_steps()
        for step in successful_steps:
            success = self._create_success_from_step(execution, step)
            if success:
                successes.append(success)

        # Analyze overall execution success
        if execution.status == ExecutionStatus.SUCCESS:
            overall_success = self._create_overall_success_experience(execution)
            if overall_success:
                successes.append(overall_success)

        # Analyze efficient patterns
        efficiency_successes = self._analyze_efficiency_patterns(execution)
        successes.extend(efficiency_successes)

        return successes

    def _create_problem_from_failed_step(
        self, execution: AgentExecution, step: ExecutionStep
    ) -> Optional[Problem]:
        """Create a problem from a failed execution step."""
        if not step.error_message:
            return None

        category = self._categorize_problem(step.error_message)
        severity = self._assess_problem_severity(step, execution)

        return Problem(
            category=category,
            severity=severity,
            title=f"Step '{step.name}' failed in {execution.agent_name}",
            description=f"Step failed during {execution.task_description}",
            step_id=step.step_id,
            error_details=step.error_message,
            impact_assessment=self._assess_problem_impact(step, execution),
            suggested_solutions=self._suggest_solutions(category, step.error_message),
            metadata={
                "execution_id": execution.execution_id,
                "agent_name": execution.agent_name,
            },
        )

    def _create_success_from_step(
        self, execution: AgentExecution, step: ExecutionStep
    ) -> Optional[SuccessExperience]:
        """Create a success experience from a successful step."""
        if step.status != ExecutionStatus.SUCCESS:
            return None

        category = self._categorize_success(step, execution)

        return SuccessExperience(
            category=category,
            title=f"Successful '{step.name}' in {execution.agent_name}",
            description=f"Successfully completed {step.description or step.name}",
            step_id=step.step_id,
            approach_details=self._extract_approach_details(step),
            benefits=["Successful execution", "Task completed"],
            reusability_score=0.7,
            metadata={
                "execution_id": execution.execution_id,
                "agent_name": execution.agent_name,
            },
        )

    def _categorize_problem(self, error_message: str) -> ProblemCategory:
        """Categorize a problem based on error message."""
        error_lower = error_message.lower()

        if "timeout" in error_lower:
            return ProblemCategory.TIMEOUT
        elif "api" in error_lower or "http" in error_lower:
            return ProblemCategory.API_ERROR
        elif "memory" in error_lower or "resource" in error_lower:
            return ProblemCategory.RESOURCE_LIMIT
        elif "data" in error_lower or "format" in error_lower:
            return ProblemCategory.DATA_ISSUE
        elif "logic" in error_lower:
            return ProblemCategory.LOGIC_ERROR
        else:
            return ProblemCategory.OTHER

    def _categorize_success(
        self, step: ExecutionStep, execution: AgentExecution
    ) -> SuccessCategory:
        """Categorize a success based on step details."""
        if step.duration_ms and step.duration_ms < 1000:
            return SuccessCategory.EFFICIENT_SOLUTION
        else:
            return SuccessCategory.BEST_PRACTICE

    def _assess_problem_severity(
        self, step: ExecutionStep, execution: AgentExecution
    ) -> ProblemSeverity:
        """Assess the severity of a problem."""
        if execution.status == ExecutionStatus.FAILED:
            return ProblemSeverity.CRITICAL
        else:
            return ProblemSeverity.MEDIUM

    def _generate_insights(
        self,
        executions: List[AgentExecution],
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> List[ReflectionInsight]:
        """Generate insights from analysis."""
        insights = []

        if problems:
            insights.append(
                ReflectionInsight(
                    type="problem_analysis",
                    title="Issues identified requiring attention",
                    description=f"Found {len(problems)} problems in execution",
                    confidence=0.8,
                    actionable_recommendations=[
                        "Review failed steps",
                        "Implement error handling",
                    ],
                )
            )

        if successes:
            insights.append(
                ReflectionInsight(
                    type="success_pattern",
                    title="Successful patterns identified",
                    description=f"Found {len(successes)} successful experiences",
                    confidence=0.9,
                    actionable_recommendations=[
                        "Document successful approaches",
                        "Reuse proven patterns",
                    ],
                )
            )

        return insights

    def _generate_summary(
        self,
        execution: AgentExecution,
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> str:
        """Generate a summary of the reflection analysis."""
        status_text = execution.status.value
        success_rate = execution.calculate_success_rate()

        return (
            f"Agent '{execution.agent_name}' execution {status_text} "
            f"with {len(execution.steps)} steps and {success_rate:.1%} success rate. "
            f"Identified {len(problems)} problems and {len(successes)} success experiences."
        )

    def _generate_assessment(
        self,
        execution: AgentExecution,
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> str:
        """Generate an overall assessment."""
        if execution.status == ExecutionStatus.SUCCESS and not problems:
            return "Excellent execution with no significant issues identified."
        elif execution.status == ExecutionStatus.SUCCESS:
            return "Good execution with minor issues that should be addressed."
        elif execution.status == ExecutionStatus.FAILED:
            return "Failed execution requiring immediate attention to critical issues."
        else:
            return "Execution completed with mixed results requiring analysis."

    def _setup_problem_patterns(self) -> Dict[str, List[str]]:
        """Setup problem detection patterns."""
        return {
            "timeout_patterns": ["timeout", "deadline exceeded"],
            "api_error_patterns": ["api error", "http error", "connection failed"],
        }

    def _setup_success_patterns(self) -> Dict[str, List[str]]:
        """Setup success detection patterns."""
        return {
            "efficiency_patterns": ["optimized", "fast execution"],
            "innovation_patterns": ["novel approach", "creative solution"],
        }

    # Helper methods for detailed analysis
    def _analyze_performance_issues(self, execution: AgentExecution) -> List[Problem]:
        """Analyze performance-related issues."""
        problems = []

        # Check for slow steps
        slow_steps = [
            step
            for step in execution.steps
            if step.duration_ms and step.duration_ms > 30000
        ]  # > 30 seconds

        for step in slow_steps:
            problems.append(
                Problem(
                    category=ProblemCategory.PERFORMANCE,
                    severity=ProblemSeverity.MEDIUM,
                    title=f"Slow execution in step '{step.name}'",
                    description=f"Step took {step.duration_ms}ms to complete",
                    step_id=step.step_id,
                    impact_assessment="May affect user experience and system throughput",
                    suggested_solutions=[
                        "Optimize algorithm",
                        "Add caching",
                        "Parallel processing",
                    ],
                    metadata={
                        "execution_id": execution.execution_id,
                        "duration_ms": step.duration_ms,
                    },
                )
            )

        return problems

    def _analyze_pattern_problems(self, execution: AgentExecution) -> List[Problem]:
        """Analyze pattern-based problems."""
        # Implementation for pattern-based problem detection
        return []

    def _analyze_efficiency_patterns(
        self, execution: AgentExecution
    ) -> List[SuccessExperience]:
        """Analyze efficiency patterns in successful execution."""
        # Implementation for efficiency pattern detection
        return []

    def _aggregate_problems(self, problems: List[Problem]) -> List[Problem]:
        """Aggregate similar problems across multiple executions."""
        # Group problems by category and similarity
        problem_groups = defaultdict(list)

        for problem in problems:
            key = (problem.category, problem.title)
            problem_groups[key].append(problem)

        aggregated = []
        for (category, title), group in problem_groups.items():
            if len(group) == 1:
                aggregated.append(group[0])
            else:
                # Merge similar problems
                merged = Problem(
                    category=category,
                    severity=max(p.severity for p in group),
                    title=title,
                    description=f"Recurring issue (occurred {len(group)} times)",
                    impact_assessment=group[0].impact_assessment,
                    suggested_solutions=list(
                        set(sum([p.suggested_solutions for p in group], []))
                    ),
                    frequency=len(group),
                    first_seen=min(p.first_seen for p in group),
                    last_seen=max(p.last_seen for p in group),
                )
                aggregated.append(merged)

        return aggregated

    def _aggregate_successes(
        self, successes: List[SuccessExperience]
    ) -> List[SuccessExperience]:
        """Aggregate similar success experiences across multiple executions."""
        # Similar to problem aggregation but for successes
        success_groups = defaultdict(list)

        for success in successes:
            key = (success.category, success.title)
            success_groups[key].append(success)

        aggregated = []
        for (category, title), group in success_groups.items():
            if len(group) == 1:
                aggregated.append(group[0])
            else:
                # Merge similar successes
                avg_reusability = sum(s.reusability_score for s in group) / len(group)
                merged = SuccessExperience(
                    category=category,
                    title=title,
                    description=f"Proven pattern (successful {len(group)} times)",
                    approach_details=group[0].approach_details,
                    benefits=list(set(sum([s.benefits for s in group], []))),
                    conditions=list(set(sum([s.conditions for s in group], []))),
                    reusability_score=avg_reusability,
                    lessons_learned=list(
                        set(sum([s.lessons_learned for s in group], []))
                    ),
                    frequency=len(group),
                    first_seen=min(s.first_seen for s in group),
                    last_seen=max(s.last_seen for s in group),
                )
                aggregated.append(merged)

        return aggregated

    # Additional helper methods would be implemented here
    def _assess_problem_impact(
        self, step: ExecutionStep, execution: AgentExecution
    ) -> str:
        """Assess the impact of a problem."""
        return "Problem impacted execution flow and may affect overall results"

    def _suggest_solutions(
        self, category: ProblemCategory, error_message: str
    ) -> List[str]:
        """Suggest solutions based on problem category."""
        solutions_map = {
            ProblemCategory.TIMEOUT: ["Increase timeout limit", "Optimize processing"],
            ProblemCategory.API_ERROR: [
                "Add error handling",
                "Implement retry mechanism",
            ],
            ProblemCategory.RESOURCE_LIMIT: [
                "Optimize memory usage",
                "Scale resources",
            ],
            ProblemCategory.DATA_ISSUE: ["Validate input data", "Add data cleaning"],
            ProblemCategory.LOGIC_ERROR: ["Review logic flow", "Add unit tests"],
        }
        return solutions_map.get(category, ["Review and debug the issue"])

    def _extract_approach_details(self, step: ExecutionStep) -> str:
        """Extract approach details from a successful step."""
        return f"Successful approach used in {step.name}: {step.description or 'Standard execution'}"

    def _create_overall_success_experience(
        self, execution: AgentExecution
    ) -> Optional[SuccessExperience]:
        """Create success experience for overall execution success."""
        return SuccessExperience(
            category=SuccessCategory.BEST_PRACTICE,
            title=f"Successful execution of {execution.agent_name}",
            description=f"Complete successful execution of {execution.task_description}",
            approach_details="End-to-end successful execution",
            benefits=["Task completed successfully", "No critical errors"],
            reusability_score=0.8,
            metadata={"execution_id": execution.execution_id},
        )

    def _generate_problem_pattern_insights(
        self, problems: List[Problem]
    ) -> List[ReflectionInsight]:
        """Generate insights from problem patterns."""
        insights = []

        # Group problems by category
        problem_counts = Counter(p.category for p in problems)

        for category, count in problem_counts.most_common(3):
            if count > 1:
                insights.append(
                    ReflectionInsight(
                        type="problem_pattern",
                        title=f"Recurring {category.value} issues",
                        description=f"Detected {count} instances of {category.value} problems",
                        confidence=min(0.8, count * 0.2),
                        supporting_evidence=[
                            f"{count} occurrences of {category.value}"
                        ],
                        actionable_recommendations=[
                            f"Investigate root cause of {category.value} issues",
                            f"Implement preventive measures for {category.value}",
                        ],
                    )
                )

        return insights

    def _generate_success_pattern_insights(
        self, successes: List[SuccessExperience]
    ) -> List[ReflectionInsight]:
        """Generate insights from success patterns."""
        insights = []

        high_reusability_patterns = [s for s in successes if s.reusability_score >= 0.7]

        if high_reusability_patterns:
            insights.append(
                ReflectionInsight(
                    type="success_pattern",
                    title="High-value reusable patterns identified",
                    description=f"Found {len(high_reusability_patterns)} highly reusable success patterns",
                    confidence=0.9,
                    supporting_evidence=[
                        f"Pattern: {s.title}" for s in high_reusability_patterns[:3]
                    ],
                    actionable_recommendations=[
                        "Document these patterns for reuse",
                        "Create templates based on successful patterns",
                        "Train team on proven approaches",
                    ],
                )
            )

        return insights

    def _generate_performance_insights(
        self, executions: List[AgentExecution]
    ) -> List[ReflectionInsight]:
        """Generate performance-related insights."""
        insights = []

        avg_duration = (
            sum(e.total_duration_ms or 0 for e in executions) / len(executions)
            if executions
            else 0
        )

        if avg_duration > 60000:  # > 1 minute
            insights.append(
                ReflectionInsight(
                    type="improvement_opportunity",
                    title="Performance optimization opportunity",
                    description=f"Average execution time is {avg_duration/1000:.1f} seconds",
                    confidence=0.7,
                    actionable_recommendations=[
                        "Profile execution to identify bottlenecks",
                        "Consider parallel processing",
                        "Optimize slow steps",
                    ],
                )
            )

        return insights

    def _generate_risk_insights(
        self, problems: List[Problem]
    ) -> List[ReflectionInsight]:
        """Generate risk assessment insights."""
        insights = []

        critical_problems = [
            p for p in problems if p.severity == ProblemSeverity.CRITICAL
        ]

        if critical_problems:
            insights.append(
                ReflectionInsight(
                    type="risk_assessment",
                    title="Critical issues require immediate attention",
                    description=f"Identified {len(critical_problems)} critical problems",
                    confidence=1.0,
                    priority="critical",
                    actionable_recommendations=[
                        "Address critical issues immediately",
                        "Implement monitoring for early detection",
                        "Create incident response procedures",
                    ],
                )
            )

        return insights

    def _generate_improvement_insights(
        self,
        executions: List[AgentExecution],
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> List[ReflectionInsight]:
        """Generate improvement opportunity insights."""
        insights = []

        success_rate = (
            sum(e.calculate_success_rate() for e in executions) / len(executions)
            if executions
            else 0
        )

        if success_rate < 0.8:
            insights.append(
                ReflectionInsight(
                    type="improvement_opportunity",
                    title="Success rate improvement needed",
                    description=f"Overall success rate is {success_rate:.1%}",
                    confidence=0.8,
                    actionable_recommendations=[
                        "Analyze failed steps for common patterns",
                        "Improve error handling and recovery",
                        "Add more comprehensive testing",
                    ],
                )
            )

        return insights

    def _prioritize_improvements(
        self, problems: List[Problem], insights: List[ReflectionInsight]
    ) -> List[str]:
        """Prioritize improvement areas."""
        priorities = []

        # Critical problems first
        critical_problems = [
            p for p in problems if p.severity == ProblemSeverity.CRITICAL
        ]
        if critical_problems:
            priorities.append("Address critical issues immediately")

        # High-impact insights
        high_priority_insights = [i for i in insights if i.priority == "critical"]
        if high_priority_insights:
            priorities.extend([i.title for i in high_priority_insights])

        # Recurring problems
        recurring_problems = [p for p in problems if p.frequency > 1]
        if recurring_problems:
            priorities.append("Fix recurring issues")

        return priorities[:5]  # Top 5 priorities

    def _extract_success_patterns(
        self, successes: List[SuccessExperience]
    ) -> List[str]:
        """Extract patterns from successful experiences."""
        return [s.title for s in successes if s.reusability_score >= 0.7]

    def _identify_risk_factors(self, problems: List[Problem]) -> List[str]:
        """Identify risk factors from problems."""
        risks = []

        # Critical problem categories
        critical_categories = set(
            p.category for p in problems if p.severity == ProblemSeverity.CRITICAL
        )
        risks.extend([f"Critical {cat.value} issues" for cat in critical_categories])

        # Recurring problem patterns
        recurring_categories = Counter(p.category for p in problems if p.frequency > 1)
        for category, count in recurring_categories.items():
            risks.append(f"Recurring {category.value} problems")

        return risks

    def _calculate_confidence_score(
        self,
        executions: List[AgentExecution],
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> float:
        """Calculate confidence score for the reflection analysis."""
        return 0.8  # Default confidence score

    def _generate_multi_execution_summary(
        self,
        executions: List[AgentExecution],
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> str:
        """Generate summary for multiple executions."""
        total_steps = sum(len(e.steps) for e in executions)
        avg_success_rate = sum(e.calculate_success_rate() for e in executions) / len(
            executions
        )

        return (
            f"Analyzed {len(executions)} executions with {total_steps} total steps. "
            f"Average success rate: {avg_success_rate:.1%}. "
            f"Found {len(problems)} problems and {len(successes)} success patterns."
        )

    def _generate_multi_execution_assessment(
        self,
        executions: List[AgentExecution],
        problems: List[Problem],
        successes: List[SuccessExperience],
    ) -> str:
        """Generate assessment for multiple executions."""
        critical_count = len(
            [p for p in problems if p.severity == ProblemSeverity.CRITICAL]
        )
        high_value_successes = len([s for s in successes if s.reusability_score >= 0.7])

        if critical_count == 0 and high_value_successes > 0:
            return "Strong performance with valuable patterns identified for reuse."
        elif critical_count > 0:
            return f"Performance needs improvement with {critical_count} critical issues to address."
        else:
            return "Moderate performance with opportunities for optimization."
