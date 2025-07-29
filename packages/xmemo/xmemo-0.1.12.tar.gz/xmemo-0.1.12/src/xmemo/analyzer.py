"""
Agent Execution Analyzer for Xmemo.

This module provides tools for analyzing agent execution data,
tracking performance metrics, and identifying patterns.
"""

from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import (
    AgentExecution,
    ExecutionContext,
    ExecutionStatus,
    ExecutionStep,
    ProblemCategory,
    ProblemSeverity,
)


class ExecutionAnalyzer:
    """Analyzes agent execution data for performance and patterns."""

    def __init__(self):
        """Initialize the execution analyzer."""
        self.config = {}  # Configuration for the analyzer
        self.execution_history = []  # Store execution history for pattern analysis

    def analyze_execution(self, execution: AgentExecution) -> Dict[str, Any]:
        """
        Analyze a single agent execution for metrics and insights.

        Args:
            execution: AgentExecution object to analyze

        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            "execution_id": execution.execution_id,
            "agent_name": execution.agent_name,
            "analysis_timestamp": datetime.now(),
            "performance_metrics": self._calculate_performance_metrics(execution),
            "success_analysis": self._analyze_success_patterns(execution),
            "failure_analysis": self._analyze_failure_patterns(execution),
            "resource_analysis": self._analyze_resource_usage(execution),
            "step_breakdown": self._analyze_step_breakdown(execution),
            "recommendations": self._generate_recommendations(execution),
        }

        # Store for pattern analysis
        self.execution_history.append(execution)

        return analysis

    def analyze_execution_batch(
        self, executions: List[AgentExecution]
    ) -> Dict[str, Any]:
        """
        Analyze multiple executions for trends and patterns.

        Args:
            executions: List of AgentExecution objects

        Returns:
            Dictionary containing batch analysis results
        """
        return {
            "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "execution_count": len(executions),
            "analysis_timestamp": datetime.now(),
            "aggregate_metrics": self._calculate_aggregate_metrics(executions),
            "trend_analysis": self._analyze_trends(executions),
            "pattern_analysis": self._analyze_execution_patterns(executions),
            "performance_comparison": self._compare_performances(executions),
            "common_issues": self._identify_common_issues(executions),
            "best_practices": self._identify_best_practices(executions),
        }

    def track_execution_progress(self, execution: AgentExecution) -> Dict[str, Any]:
        """
        Track progress of an ongoing execution.

        Args:
            execution: AgentExecution object (potentially ongoing)

        Returns:
            Progress tracking information
        """
        completed_steps = [
            s
            for s in execution.steps
            if s.status in [ExecutionStatus.SUCCESS, ExecutionStatus.FAILED]
        ]
        pending_steps = [
            s for s in execution.steps if s.status == ExecutionStatus.PENDING
        ]
        running_steps = [
            s for s in execution.steps if s.status == ExecutionStatus.RUNNING
        ]

        progress_percentage = (
            len(completed_steps) / len(execution.steps) * 100 if execution.steps else 0
        )

        return {
            "execution_id": execution.execution_id,
            "status": execution.status,
            "progress_percentage": progress_percentage,
            "completed_steps": len(completed_steps),
            "pending_steps": len(pending_steps),
            "running_steps": len(running_steps),
            "total_steps": len(execution.steps),
            "estimated_remaining_time": self._estimate_remaining_time(execution),
            "current_performance": self._calculate_current_performance(execution),
        }

    def _calculate_performance_metrics(
        self, execution: AgentExecution
    ) -> Dict[str, Any]:
        """Calculate performance metrics for an execution."""
        metrics = {
            "total_duration_ms": execution.total_duration_ms or 0,
            "success_rate": execution.calculate_success_rate(),
            "failed_steps": len(execution.get_failed_steps()),
            "successful_steps": len(execution.get_successful_steps()),
            "average_step_duration": self._calculate_average_step_duration(execution),
            "slowest_step": self._find_slowest_step(execution),
            "fastest_step": self._find_fastest_step(execution),
            "error_rate": self._calculate_error_rate(execution),
            "completion_status": execution.status.value,
        }

        # Add resource metrics if available
        if execution.resource_usage:
            metrics["resource_metrics"] = execution.resource_usage

        return metrics

    def _analyze_success_patterns(self, execution: AgentExecution) -> Dict[str, Any]:
        """Analyze patterns in successful execution steps."""
        successful_steps = execution.get_successful_steps()

        if not successful_steps:
            return {"patterns": [], "insights": []}

        patterns = {
            "common_step_types": self._identify_common_step_types(successful_steps),
            "optimal_durations": self._analyze_optimal_durations(successful_steps),
            "success_conditions": ["Valid input data", "Adequate resources"],
            "efficient_sequences": self._identify_efficient_sequences(successful_steps),
        }

        insights = [
            f"Successfully completed {len(successful_steps)} steps",
            f"Most efficient step type: {patterns['common_step_types'][0] if patterns['common_step_types'] else 'N/A'}",
            f"Average successful step duration: {self._calculate_average_duration(successful_steps):.2f}ms",
        ]

        return {"patterns": patterns, "insights": insights}

    def _analyze_failure_patterns(self, execution: AgentExecution) -> Dict[str, Any]:
        """Analyze patterns in failed execution steps."""
        failed_steps = execution.get_failed_steps()

        if not failed_steps:
            return {"patterns": [], "insights": []}

        patterns = {
            "common_failure_types": self._categorize_failures(failed_steps),
            "failure_timing": self._analyze_failure_timing(failed_steps),
            "error_clustering": self._cluster_errors(failed_steps),
            "critical_failure_points": self._identify_critical_failures(failed_steps),
        }

        insights = [
            f"Failed {len(failed_steps)} steps out of {len(execution.steps)}",
            f"Most common failure type: {patterns['common_failure_types'][0] if patterns['common_failure_types'] else 'N/A'}",
            f"Critical failures: {len(patterns['critical_failure_points'])}",
        ]

        return {"patterns": patterns, "insights": insights}

    def _analyze_resource_usage(self, execution: AgentExecution) -> Dict[str, Any]:
        """Analyze resource usage patterns."""
        if not execution.resource_usage:
            return {"status": "no_data", "insights": []}

        analysis = {
            "peak_memory": execution.resource_usage.get("peak_memory_mb", 0),
            "average_cpu": execution.resource_usage.get("average_cpu_percent", 0),
            "io_operations": execution.resource_usage.get("io_operations", 0),
            "network_usage": execution.resource_usage.get("network_kb", 0),
        }

        insights = []
        if analysis["peak_memory"] > 1000:  # > 1GB
            insights.append("High memory usage detected")
        if analysis["average_cpu"] > 80:  # > 80%
            insights.append("High CPU utilization detected")

        return {"metrics": analysis, "insights": insights}

    def _analyze_step_breakdown(
        self, execution: AgentExecution
    ) -> List[Dict[str, Any]]:
        """Provide detailed breakdown of each execution step."""
        breakdown = []

        for step in execution.steps:
            step_analysis = {
                "step_id": step.step_id,
                "name": step.name,
                "status": step.status.value,
                "duration_ms": step.duration_ms or 0,
                "performance_rating": self._rate_step_performance(step),
                "issues": self._identify_step_issues(step),
                "optimizations": self._suggest_step_optimizations(step),
            }
            breakdown.append(step_analysis)

        return breakdown

    def _generate_recommendations(self, execution: AgentExecution) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Performance recommendations
        if (
            execution.total_duration_ms and execution.total_duration_ms > 60000
        ):  # > 1 minute
            recommendations.append(
                "Consider optimizing execution time - current duration exceeds 1 minute"
            )

        # Success rate recommendations
        success_rate = execution.calculate_success_rate()
        if success_rate < 0.8:
            recommendations.append("Improve error handling - success rate below 80%")

        # Step-specific recommendations
        failed_steps = execution.get_failed_steps()
        if failed_steps:
            recommendations.append(
                f"Address {len(failed_steps)} failed steps to improve reliability"
            )

        return recommendations

    # Helper methods
    def _calculate_average_step_duration(self, execution: AgentExecution) -> float:
        """Calculate average duration of steps."""
        durations = [step.duration_ms for step in execution.steps if step.duration_ms]
        return sum(durations) / len(durations) if durations else 0

    def _find_slowest_step(self, execution: AgentExecution) -> Optional[Dict[str, Any]]:
        """Find the slowest step in execution."""
        steps_with_duration = [step for step in execution.steps if step.duration_ms]
        if not steps_with_duration:
            return None

        slowest = max(steps_with_duration, key=lambda x: x.duration_ms)
        return {
            "step_id": slowest.step_id,
            "name": slowest.name,
            "duration_ms": slowest.duration_ms,
        }

    def _find_fastest_step(self, execution: AgentExecution) -> Optional[Dict[str, Any]]:
        """Find the fastest step in execution."""
        steps_with_duration = [step for step in execution.steps if step.duration_ms]
        if not steps_with_duration:
            return None

        fastest = min(steps_with_duration, key=lambda x: x.duration_ms)
        return {
            "step_id": fastest.step_id,
            "name": fastest.name,
            "duration_ms": fastest.duration_ms,
        }

    def _calculate_error_rate(self, execution: AgentExecution) -> float:
        """Calculate error rate for execution."""
        if not execution.steps:
            return 0.0
        failed_steps = len(execution.get_failed_steps())
        return failed_steps / len(execution.steps)

    def _identify_common_step_types(self, steps: List[ExecutionStep]) -> List[str]:
        """Identify most common step types."""
        step_names = [step.name for step in steps]
        counter = Counter(step_names)
        return [name for name, count in counter.most_common(5)]

    def _analyze_optimal_durations(
        self, steps: List[ExecutionStep]
    ) -> Dict[str, float]:
        """Analyze optimal durations for different step types."""
        step_durations = {}
        for step in steps:
            if step.duration_ms:
                if step.name not in step_durations:
                    step_durations[step.name] = []
                step_durations[step.name].append(step.duration_ms)

        optimal_durations = {}
        for step_name, durations in step_durations.items():
            optimal_durations[step_name] = sum(durations) / len(durations)

        return optimal_durations

    def _identify_efficient_sequences(self, steps: List[ExecutionStep]) -> List[str]:
        """Identify efficient step sequences."""
        efficient_sequences = []

        for i in range(len(steps) - 1):
            current_step = steps[i]
            next_step = steps[i + 1]

            if (
                current_step.duration_ms
                and next_step.duration_ms
                and current_step.duration_ms < 5000
                and next_step.duration_ms < 5000
            ):
                sequence = f"{current_step.name} -> {next_step.name}"
                efficient_sequences.append(sequence)

        return efficient_sequences

    def _calculate_average_duration(self, steps: List[ExecutionStep]) -> float:
        """Calculate average duration of given steps."""
        durations = [step.duration_ms for step in steps if step.duration_ms]
        return sum(durations) / len(durations) if durations else 0

    def _categorize_failures(self, failed_steps: List[ExecutionStep]) -> List[str]:
        """Categorize types of failures."""
        failure_types = []

        for step in failed_steps:
            if step.error_message:
                error_msg = step.error_message.lower()
                if "timeout" in error_msg:
                    failure_types.append("timeout")
                elif "memory" in error_msg:
                    failure_types.append("memory")
                elif "api" in error_msg:
                    failure_types.append("api_error")
                else:
                    failure_types.append("general_error")

        counter = Counter(failure_types)
        return [failure_type for failure_type, count in counter.most_common(3)]

    def _analyze_failure_timing(
        self, failed_steps: List[ExecutionStep]
    ) -> Dict[str, Any]:
        """Analyze when failures typically occur."""
        failure_times = []
        for step in failed_steps:
            if step.start_time:
                time_of_day = (
                    step.start_time.hour * 3600
                    + step.start_time.minute * 60
                    + step.start_time.second
                )
                failure_times.append(time_of_day)

        if failure_times:
            avg_failure_time = sum(failure_times) / len(failure_times)
            return {
                "average_failure_time_seconds": avg_failure_time,
                "failure_count": len(failure_times),
            }

        return {"average_failure_time_seconds": 0, "failure_count": 0}

    def _cluster_errors(
        self, failed_steps: List[ExecutionStep]
    ) -> Dict[str, List[str]]:
        """Cluster similar errors together."""
        error_clusters = {}

        for step in failed_steps:
            if step.error_message:
                first_word = (
                    step.error_message.split()[0].lower()
                    if step.error_message.split()
                    else "unknown"
                )
                if first_word not in error_clusters:
                    error_clusters[first_word] = []
                error_clusters[first_word].append(step.step_id)

        return error_clusters

    def _identify_critical_failures(
        self, failed_steps: List[ExecutionStep]
    ) -> List[str]:
        """Identify critical failure points."""
        critical_failures = []

        for step in failed_steps:
            if step.error_message:
                error_msg = step.error_message.lower()
                if any(
                    keyword in error_msg
                    for keyword in ["critical", "fatal", "severe", "system"]
                ):
                    critical_failures.append(step.step_id)

        return critical_failures

    def _rate_step_performance(self, step: ExecutionStep) -> str:
        """Rate the performance of a step."""
        if step.status == ExecutionStatus.FAILED:
            return "poor"
        elif step.duration_ms and step.duration_ms < 1000:
            return "excellent"
        elif step.duration_ms and step.duration_ms < 5000:
            return "good"
        elif step.duration_ms and step.duration_ms < 15000:
            return "fair"
        else:
            return "poor"

    def _identify_step_issues(self, step: ExecutionStep) -> List[str]:
        """Identify issues with a specific step."""
        issues = []

        if step.status == ExecutionStatus.FAILED:
            issues.append("Step failed to complete")

        if step.duration_ms and step.duration_ms > 30000:  # > 30 seconds
            issues.append("Step took longer than expected")

        if step.error_message:
            issues.append(f"Error occurred: {step.error_message[:50]}...")

        return issues

    def _suggest_step_optimizations(self, step: ExecutionStep) -> List[str]:
        """Suggest optimizations for a step."""
        optimizations = []

        if step.duration_ms and step.duration_ms > 10000:  # > 10 seconds
            optimizations.append("Consider optimizing step execution time")

        if step.status == ExecutionStatus.FAILED:
            optimizations.append("Add error handling and retry logic")

        return optimizations

    def _estimate_remaining_time(self, execution: AgentExecution) -> int:
        """Estimate remaining execution time."""
        completed_steps = [
            s
            for s in execution.steps
            if s.status in [ExecutionStatus.SUCCESS, ExecutionStatus.FAILED]
        ]
        pending_steps = [
            s for s in execution.steps if s.status == ExecutionStatus.PENDING
        ]

        if not completed_steps:
            return 0

        avg_duration = self._calculate_average_step_duration(execution)
        return int(avg_duration * len(pending_steps))

    def _calculate_current_performance(
        self, execution: AgentExecution
    ) -> Dict[str, Any]:
        """Calculate current performance metrics for ongoing execution."""
        return {
            "current_success_rate": execution.calculate_success_rate(),
            "current_duration_ms": execution.total_duration_ms or 0,
            "steps_completed": len(
                [
                    s
                    for s in execution.steps
                    if s.status in [ExecutionStatus.SUCCESS, ExecutionStatus.FAILED]
                ]
            ),
            "current_status": execution.status.value,
        }

    def _calculate_aggregate_metrics(
        self, executions: List[AgentExecution]
    ) -> Dict[str, Any]:
        """Calculate aggregate metrics across multiple executions."""
        if not executions:
            return {}

        total_executions = len(executions)
        successful_executions = len(
            [e for e in executions if e.status == ExecutionStatus.SUCCESS]
        )
        failed_executions = len(
            [e for e in executions if e.status == ExecutionStatus.FAILED]
        )

        total_steps = sum(len(e.steps) for e in executions)
        total_duration = sum(e.total_duration_ms or 0 for e in executions)

        return {
            "total_executions": total_executions,
            "success_rate": successful_executions / total_executions,
            "failure_rate": failed_executions / total_executions,
            "average_duration_ms": (
                total_duration / total_executions if total_executions > 0 else 0
            ),
            "total_steps": total_steps,
            "average_steps_per_execution": (
                total_steps / total_executions if total_executions > 0 else 0
            ),
            "overall_step_success_rate": (
                sum(e.calculate_success_rate() for e in executions) / total_executions
                if total_executions > 0
                else 0
            ),
        }

    def _analyze_trends(self, executions: List[AgentExecution]) -> Dict[str, Any]:
        """Analyze trends across executions."""
        sorted_executions = sorted(executions, key=lambda x: x.start_time)

        trends = {
            "performance_trend": self._calculate_performance_trend(sorted_executions),
            "success_rate_trend": self._calculate_success_rate_trend(sorted_executions),
            "duration_trend": self._calculate_duration_trend(sorted_executions),
            "error_trend": self._calculate_error_trend(sorted_executions),
        }

        return trends

    def _analyze_execution_patterns(
        self, executions: List[AgentExecution]
    ) -> Dict[str, Any]:
        """Identify common patterns across executions."""
        patterns = {
            "common_agent_types": self._identify_common_agents(executions),
            "typical_step_sequences": self._identify_step_sequences(executions),
            "success_patterns": self._identify_success_patterns(executions),
            "failure_patterns": self._identify_failure_patterns(executions),
        }

        return patterns

    def _calculate_performance_trend(self, executions: List[AgentExecution]) -> str:
        """Calculate performance trend."""
        if len(executions) < 2:
            return "insufficient_data"

        recent_performance = (
            executions[-3:] if len(executions) >= 3 else executions[-2:]
        )
        earlier_performance = executions[: -len(recent_performance)]

        recent_avg = sum(e.calculate_success_rate() for e in recent_performance) / len(
            recent_performance
        )
        earlier_avg = (
            sum(e.calculate_success_rate() for e in earlier_performance)
            / len(earlier_performance)
            if earlier_performance
            else recent_avg
        )

        if recent_avg > earlier_avg + 0.1:
            return "improving"
        elif recent_avg < earlier_avg - 0.1:
            return "declining"
        else:
            return "stable"

    def _calculate_success_rate_trend(
        self, executions: List[AgentExecution]
    ) -> Dict[str, float]:
        """Calculate success rate trend."""
        success_rates = [e.calculate_success_rate() for e in executions]

        if len(success_rates) >= 2:
            recent_avg = sum(success_rates[-3:]) / min(3, len(success_rates))
            overall_avg = sum(success_rates) / len(success_rates)
            return {
                "recent_average": recent_avg,
                "overall_average": overall_avg,
                "trend": "improving" if recent_avg > overall_avg else "declining",
            }

        return {"recent_average": 0, "overall_average": 0, "trend": "insufficient_data"}

    def _calculate_duration_trend(
        self, executions: List[AgentExecution]
    ) -> Dict[str, float]:
        """Calculate duration trend."""
        durations = [e.total_duration_ms or 0 for e in executions]

        if len(durations) >= 2:
            recent_avg = sum(durations[-3:]) / min(3, len(durations))
            overall_avg = sum(durations) / len(durations)
            return {
                "recent_average_ms": recent_avg,
                "overall_average_ms": overall_avg,
                "trend": "faster" if recent_avg < overall_avg else "slower",
            }

        return {
            "recent_average_ms": 0,
            "overall_average_ms": 0,
            "trend": "insufficient_data",
        }

    def _calculate_error_trend(
        self, executions: List[AgentExecution]
    ) -> Dict[str, Any]:
        """Calculate error trend."""
        error_rates = [self._calculate_error_rate(e) for e in executions]

        if len(error_rates) >= 2:
            recent_avg = sum(error_rates[-3:]) / min(3, len(error_rates))
            overall_avg = sum(error_rates) / len(error_rates)
            return {
                "recent_error_rate": recent_avg,
                "overall_error_rate": overall_avg,
                "trend": "improving" if recent_avg < overall_avg else "worsening",
            }

        return {
            "recent_error_rate": 0,
            "overall_error_rate": 0,
            "trend": "insufficient_data",
        }

    def _identify_common_agents(self, executions: List[AgentExecution]) -> List[str]:
        """Identify most commonly used agents."""
        agent_names = [e.agent_name for e in executions]
        counter = Counter(agent_names)
        return [name for name, count in counter.most_common(5)]

    def _identify_step_sequences(self, executions: List[AgentExecution]) -> List[str]:
        """Identify common step sequences."""
        sequences = []

        for execution in executions:
            if len(execution.steps) >= 2:
                step_names = [step.name for step in execution.steps]
                for i in range(len(step_names) - 1):
                    sequence = f"{step_names[i]} -> {step_names[i+1]}"
                    sequences.append(sequence)

        counter = Counter(sequences)
        return [sequence for sequence, count in counter.most_common(5)]

    def _identify_success_patterns(self, executions: List[AgentExecution]) -> List[str]:
        """Identify patterns in successful executions."""
        successful_executions = [
            e for e in executions if e.status == ExecutionStatus.SUCCESS
        ]
        patterns = []

        if successful_executions:
            avg_duration = sum(
                e.total_duration_ms or 0 for e in successful_executions
            ) / len(successful_executions)
            avg_steps = sum(len(e.steps) for e in successful_executions) / len(
                successful_executions
            )

            patterns.append(
                f"Successful executions average {avg_duration:.0f}ms duration"
            )
            patterns.append(f"Successful executions average {avg_steps:.1f} steps")

        return patterns

    def _identify_failure_patterns(self, executions: List[AgentExecution]) -> List[str]:
        """Identify patterns in failed executions."""
        failed_executions = [
            e for e in executions if e.status == ExecutionStatus.FAILED
        ]
        patterns = []

        if failed_executions:
            common_failure_points = []
            for execution in failed_executions:
                failed_steps = execution.get_failed_steps()
                for step in failed_steps:
                    common_failure_points.append(step.name)

            counter = Counter(common_failure_points)
            most_common_failure = counter.most_common(1)

            if most_common_failure:
                patterns.append(
                    f"Most common failure point: {most_common_failure[0][0]}"
                )

            avg_failure_duration = sum(
                e.total_duration_ms or 0 for e in failed_executions
            ) / len(failed_executions)
            patterns.append(
                f"Failed executions average {avg_failure_duration:.0f}ms before failure"
            )

        return patterns

    def _compare_performances(self, executions: List[AgentExecution]) -> Dict[str, Any]:
        """Compare performance across different agents."""
        agent_performance = {}

        for execution in executions:
            agent_name = execution.agent_name
            if agent_name not in agent_performance:
                agent_performance[agent_name] = {
                    "executions": 0,
                    "total_duration": 0,
                    "successful": 0,
                    "failed": 0,
                }

            agent_performance[agent_name]["executions"] += 1
            agent_performance[agent_name]["total_duration"] += (
                execution.total_duration_ms or 0
            )

            if execution.status == ExecutionStatus.SUCCESS:
                agent_performance[agent_name]["successful"] += 1
            elif execution.status == ExecutionStatus.FAILED:
                agent_performance[agent_name]["failed"] += 1

        # Calculate derived metrics
        for agent_name, metrics in agent_performance.items():
            metrics["success_rate"] = (
                metrics["successful"] / metrics["executions"]
                if metrics["executions"] > 0
                else 0
            )
            metrics["average_duration"] = (
                metrics["total_duration"] / metrics["executions"]
                if metrics["executions"] > 0
                else 0
            )

        return agent_performance

    def _identify_common_issues(self, executions: List[AgentExecution]) -> List[str]:
        """Identify common issues across executions."""
        issues = []

        # Collect all error messages
        error_messages = []
        for execution in executions:
            for step in execution.steps:
                if step.error_message:
                    error_messages.append(step.error_message.lower())

        # Simple keyword analysis
        issue_keywords = [
            "timeout",
            "memory",
            "api",
            "connection",
            "permission",
            "validation",
        ]
        for keyword in issue_keywords:
            count = sum(1 for msg in error_messages if keyword in msg)
            if count > 0:
                issues.append(f"{keyword.title()} issues ({count} occurrences)")

        return issues

    def _identify_best_practices(self, executions: List[AgentExecution]) -> List[str]:
        """Identify best practices from successful executions."""
        successful_executions = [
            e
            for e in executions
            if e.status == ExecutionStatus.SUCCESS and e.calculate_success_rate() > 0.9
        ]

        if not successful_executions:
            return []

        practices = []

        # Analyze patterns in highly successful executions
        avg_steps = sum(len(e.steps) for e in successful_executions) / len(
            successful_executions
        )
        avg_duration = sum(
            e.total_duration_ms or 0 for e in successful_executions
        ) / len(successful_executions)

        practices.append(f"Optimal step count: {avg_steps:.1f} steps")
        practices.append(f"Target execution time: {avg_duration:.0f}ms")

        return practices
