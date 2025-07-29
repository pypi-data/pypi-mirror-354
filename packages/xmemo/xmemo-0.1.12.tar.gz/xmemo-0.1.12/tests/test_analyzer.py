"""
Tests for the ExecutionAnalyzer class.
"""

from datetime import datetime, timedelta
from typing import List

import pytest

from xmemo import (
    AgentExecution,
    ExecutionAnalyzer,
    ExecutionStatus,
    ExecutionStep,
)


class TestExecutionAnalyzer:
    """Test cases for ExecutionAnalyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ExecutionAnalyzer()

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer is not None

    def test_analyze_single_execution_success(self):
        """Test analyzing a single successful execution."""
        execution = AgentExecution(
            execution_id="exec-123",
            agent_name="test-agent",
            task_description="Data processing task",
            start_time=datetime.now() - timedelta(minutes=5),
            end_time=datetime.now(),
            status=ExecutionStatus.SUCCESS,
            steps=[
                ExecutionStep(
                    step_id="step-1",
                    name="Data Validation",
                    start_time=datetime.now() - timedelta(minutes=4),
                    end_time=datetime.now() - timedelta(minutes=3),
                    status=ExecutionStatus.SUCCESS,
                    output_data={"validated_records": 100},
                ),
                ExecutionStep(
                    step_id="step-2",
                    name="Data Processing",
                    start_time=datetime.now() - timedelta(minutes=3),
                    end_time=datetime.now(),
                    status=ExecutionStatus.SUCCESS,
                    output_data={"processed_records": 100},
                ),
            ],
        )

        result = self.analyzer.analyze_execution(execution)

        assert result["agent_name"] == "test-agent"
        assert result["execution_id"] == "exec-123"
        assert result["performance_metrics"]["success_rate"] == 1.0
        assert result["performance_metrics"]["successful_steps"] == 2
        assert result["performance_metrics"]["failed_steps"] == 0

    def test_analyze_single_execution_with_failures(self):
        """Test analyzing an execution with step failures."""
        execution = AgentExecution(
            execution_id="exec-456",
            agent_name="test-agent",
            task_description="API integration task",
            start_time=datetime.now() - timedelta(minutes=10),
            end_time=datetime.now(),
            status=ExecutionStatus.FAILED,
            steps=[
                ExecutionStep(
                    step_id="step-1",
                    name="Authentication",
                    start_time=datetime.now() - timedelta(minutes=9),
                    end_time=datetime.now() - timedelta(minutes=8),
                    status=ExecutionStatus.SUCCESS,
                ),
                ExecutionStep(
                    step_id="step-2",
                    name="API Call",
                    start_time=datetime.now() - timedelta(minutes=8),
                    end_time=datetime.now() - timedelta(minutes=5),
                    status=ExecutionStatus.FAILED,
                    error_message="Connection timeout",
                ),
                ExecutionStep(
                    step_id="step-3",
                    name="Retry Logic",
                    start_time=datetime.now() - timedelta(minutes=5),
                    end_time=datetime.now(),
                    status=ExecutionStatus.SUCCESS,
                ),
            ],
        )

        result = self.analyzer.analyze_execution(execution)

        assert (
            result["performance_metrics"]["success_rate"] == 2 / 3
        )  # 2 successful steps out of 3
        assert result["performance_metrics"]["successful_steps"] == 2
        assert result["performance_metrics"]["failed_steps"] == 1

    def test_batch_analysis(self):
        """Test batch analysis of multiple executions."""
        executions = [
            AgentExecution(
                execution_id=f"exec-{i}",
                agent_name="agent-1",
                task_description="Test task",
                start_time=datetime.now() - timedelta(minutes=i * 5),
                end_time=datetime.now() - timedelta(minutes=i * 5 - 2),
                status=(
                    ExecutionStatus.SUCCESS if i % 2 == 0 else ExecutionStatus.FAILED
                ),
                steps=[
                    ExecutionStep(
                        step_id=f"step-{i}-1",
                        name="Test Step",
                        start_time=datetime.now() - timedelta(minutes=i * 5),
                        end_time=datetime.now() - timedelta(minutes=i * 5 - 2),
                        status=(
                            ExecutionStatus.SUCCESS
                            if i % 2 == 0
                            else ExecutionStatus.FAILED
                        ),
                    )
                ],
            )
            for i in range(5)
        ]

        result = self.analyzer.analyze_execution_batch(executions)

        assert result["execution_count"] == 5
        assert result["aggregate_metrics"]["total_executions"] == 5
        assert result["aggregate_metrics"]["success_rate"] == 0.6  # 3/5

    def test_trend_analysis(self):
        """Test trend analysis over time."""
        executions = []
        base_time = datetime.now() - timedelta(days=10)

        for i in range(10):
            execution = AgentExecution(
                execution_id=f"trend-exec-{i}",
                agent_name="trend-agent",
                task_description="Trend test task",
                start_time=base_time + timedelta(days=i),
                end_time=base_time + timedelta(days=i, minutes=2),
                status=(
                    ExecutionStatus.SUCCESS if i < 7 else ExecutionStatus.FAILED
                ),  # Performance degrades
                steps=[
                    ExecutionStep(
                        step_id=f"trend-step-{i}",
                        name="Trend Step",
                        start_time=base_time + timedelta(days=i),
                        end_time=base_time + timedelta(days=i, minutes=2),
                        status=(
                            ExecutionStatus.SUCCESS if i < 7 else ExecutionStatus.FAILED
                        ),
                    )
                ],
            )
            executions.append(execution)

        result = self.analyzer.analyze_execution_batch(executions)

        assert result["execution_count"] == 10
        assert result["trend_analysis"]["performance_trend"] in [
            "improving",
            "declining",
            "stable",
        ]

    def test_performance_comparison(self):
        """Test performance comparison between agents."""
        agents_data = {
            "fast-agent": [
                AgentExecution(
                    execution_id="fast-1",
                    agent_name="fast-agent",
                    task_description="Comparison task",
                    start_time=datetime.now() - timedelta(minutes=2),
                    end_time=datetime.now() - timedelta(minutes=1),
                    status=ExecutionStatus.SUCCESS,
                    total_duration_ms=60000,  # 1 minute
                    steps=[],
                )
            ],
            "slow-agent": [
                AgentExecution(
                    execution_id="slow-1",
                    agent_name="slow-agent",
                    task_description="Comparison task",
                    start_time=datetime.now() - timedelta(minutes=10),
                    end_time=datetime.now() - timedelta(minutes=5),
                    status=ExecutionStatus.SUCCESS,
                    total_duration_ms=300000,  # 5 minutes
                    steps=[],
                )
            ],
        }

        all_executions = agents_data["fast-agent"] + agents_data["slow-agent"]
        result = self.analyzer.analyze_execution_batch(all_executions)

        assert result["execution_count"] == 2
        comparison = result["performance_comparison"]
        assert "fast-agent" in comparison
        assert "slow-agent" in comparison

        fast_metrics = comparison["fast-agent"]
        slow_metrics = comparison["slow-agent"]

        assert fast_metrics["average_duration"] < slow_metrics["average_duration"]

    def test_progress_tracking(self):
        """Test progress tracking for ongoing executions."""
        ongoing_execution = AgentExecution(
            execution_id="progress-exec",
            agent_name="progress-agent",
            task_description="Long running task",
            start_time=datetime.now() - timedelta(minutes=5),
            end_time=None,  # Still running
            status=ExecutionStatus.RUNNING,
            steps=[
                ExecutionStep(
                    step_id="step-1",
                    name="Completed Step",
                    start_time=datetime.now() - timedelta(minutes=4),
                    end_time=datetime.now() - timedelta(minutes=3),
                    status=ExecutionStatus.SUCCESS,
                ),
                ExecutionStep(
                    step_id="step-2",
                    name="Running Step",
                    start_time=datetime.now() - timedelta(minutes=3),
                    end_time=None,
                    status=ExecutionStatus.RUNNING,
                ),
            ],
        )

        result = self.analyzer.track_execution_progress(ongoing_execution)

        assert result["execution_id"] == "progress-exec"
        assert result["progress_percentage"] > 0
        assert result["progress_percentage"] < 100  # Not complete yet
        assert result["completed_steps"] == 1
        assert result["running_steps"] == 1
        assert result["estimated_remaining_time"] is not None
