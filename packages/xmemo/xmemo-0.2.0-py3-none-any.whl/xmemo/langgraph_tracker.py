"""
LangGraph Integration for Xmemo.

This module provides integration with LangGraph to automatically track
and analyze LangGraph agent executions, providing insights into graph
performance, node efficiency, and execution patterns.
"""

from contextlib import contextmanager
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

try:
    from langgraph.graph import StateGraph
    from langgraph.graph.graph import CompiledGraph

    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    CompiledGraph = None

from .analyzer import ExecutionAnalyzer
from .models import (
    ExecutionStatus,
    LangGraphExecution,
    LangGraphNode,
    LangGraphNodeType,
    LangGraphState,
)
from .reflection import ExecutionReflectionEngine


class LangGraphTracker:
    """
    Tracks and analyzes LangGraph agent executions.

    This class provides hooks and instrumentation for LangGraph
    to automatically capture execution data and generate insights.
    """

    def __init__(
        self,
        analyzer: Optional[ExecutionAnalyzer] = None,
        reflection_engine: Optional[ExecutionReflectionEngine] = None,
    ):
        """
        Initialize the LangGraph tracker.

        Args:
            analyzer: Optional ExecutionAnalyzer instance
            reflection_engine: Optional ExecutionReflectionEngine instance
        """
        if not LANGGRAPH_AVAILABLE:
            raise ImportError(
                "LangGraph is not installed. Please install it with: "
                "pip install langgraph"
            )

        self.analyzer = analyzer or ExecutionAnalyzer()
        self.reflection_engine = reflection_engine or ExecutionReflectionEngine()
        self.active_executions: Dict[str, LangGraphExecution] = {}
        self.execution_history: List[LangGraphExecution] = []

    def track_execution(
        self,
        graph: CompiledGraph,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
        execution_id: Optional[str] = None,
    ) -> LangGraphExecution:
        """
        Track a LangGraph execution.

        Args:
            graph: The compiled LangGraph to execute
            input_data: Input data for the graph
            config: Optional configuration
            execution_id: Optional custom execution ID

        Returns:
            LangGraphExecution record
        """
        execution_id = (
            execution_id or f"lg_exec_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        )

        # Create initial state
        initial_state = LangGraphState(data=input_data.copy())

        # Create execution record
        execution = LangGraphExecution(
            execution_id=execution_id,
            graph_name=getattr(graph, "name", "unknown_graph"),
            initial_state=initial_state,
            start_time=datetime.now(),
            config=config or {},
        )

        self.active_executions[execution_id] = execution
        return execution

    def track_node_execution(
        self,
        execution_id: str,
        node_id: str,
        node_name: str,
        node_type: LangGraphNodeType,
        input_state: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start tracking a node execution.

        Args:
            execution_id: ID of the parent execution
            node_id: Unique identifier for the node
            node_name: Human-readable name of the node
            node_type: Type of the node
            input_state: Input state for the node

        Returns:
            Node execution ID
        """
        execution = self.active_executions.get(execution_id)
        if not execution:
            raise ValueError(f"No active execution found with ID: {execution_id}")

        node = LangGraphNode(
            node_id=node_id,
            node_name=node_name,
            node_type=node_type,
            execution_start=datetime.now(),
            status=ExecutionStatus.RUNNING,
        )

        if input_state:
            node.input_state = LangGraphState(data=input_state)

        execution.add_node_execution(node)
        return node_id

    def complete_node_execution(
        self,
        execution_id: str,
        node_id: str,
        output_state: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Complete a node execution.

        Args:
            execution_id: ID of the parent execution
            node_id: ID of the node
            output_state: Output state from the node
            error: Error message if the node failed
            tool_calls: List of tool calls made by the node
        """
        execution = self.active_executions.get(execution_id)
        if not execution:
            return

        # Find the node
        node = None
        for n in execution.executed_nodes:
            if n.node_id == node_id:
                node = n
                break

        if not node:
            return

        node.execution_end = datetime.now()
        node.duration_ms = int(
            (node.execution_end - node.execution_start).total_seconds() * 1000
        )

        if error:
            node.status = ExecutionStatus.FAILED
            node.error_message = error
        else:
            node.status = ExecutionStatus.SUCCESS

        if output_state:
            node.output_state = LangGraphState(data=output_state)

        if tool_calls:
            node.tool_calls = tool_calls

    def complete_execution(
        self,
        execution_id: str,
        final_state: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> LangGraphExecution:
        """
        Complete a LangGraph execution.

        Args:
            execution_id: ID of the execution
            final_state: Final state of the execution
            error: Error message if execution failed

        Returns:
            Completed LangGraphExecution record
        """
        execution = self.active_executions.pop(execution_id, None)
        if not execution:
            raise ValueError(f"No active execution found with ID: {execution_id}")

        execution.end_time = datetime.now()
        execution.total_duration_ms = int(
            (execution.end_time - execution.start_time).total_seconds() * 1000
        )

        if error:
            execution.status = ExecutionStatus.FAILED
        else:
            execution.status = ExecutionStatus.SUCCESS

        if final_state:
            execution.final_state = LangGraphState(data=final_state)

        self.execution_history.append(execution)
        return execution

    def analyze_execution(self, execution: LangGraphExecution) -> Dict[str, Any]:
        """
        Analyze a LangGraph execution.

        Args:
            execution: LangGraph execution to analyze

        Returns:
            Analysis results
        """
        # Convert to standard format for analyzer
        converted_execution = self._convert_to_agent_execution(execution)
        analysis = self.analyzer.analyze_execution(converted_execution)

        # Add LangGraph-specific analysis
        langgraph_analysis = {
            "graph_structure": self._analyze_graph_structure(execution),
            "node_performance": self._analyze_node_performance(execution),
            "execution_path": self._analyze_execution_path(execution),
            "state_evolution": self._analyze_state_evolution(execution),
            "tool_usage": self._analyze_tool_usage(execution),
        }

        analysis["langgraph_analysis"] = langgraph_analysis
        return analysis

    def generate_insights(self, executions: List[LangGraphExecution]) -> Dict[str, Any]:
        """
        Generate insights from multiple LangGraph executions.

        Args:
            executions: List of LangGraph executions

        Returns:
            Insight analysis
        """
        if not executions:
            return {"insights": [], "patterns": []}

        # Convert to standard format
        converted_executions = [
            self._convert_to_agent_execution(ex) for ex in executions
        ]

        # Use reflection engine
        reflection_result = self.reflection_engine.reflect_on_multiple_executions(
            converted_executions
        )

        # Add LangGraph-specific insights
        langgraph_insights = {
            "common_graph_patterns": self._identify_graph_patterns(executions),
            "node_efficiency_insights": self._analyze_node_efficiency(executions),
            "path_optimization_opportunities": self._identify_path_optimizations(
                executions
            ),
            "state_management_insights": self._analyze_state_management(executions),
        }

        return {
            "standard_reflection": reflection_result,
            "langgraph_insights": langgraph_insights,
        }

    @contextmanager
    def track_graph_execution(
        self,
        graph: CompiledGraph,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager for tracking a complete graph execution.

        Args:
            graph: The compiled LangGraph
            input_data: Input data
            config: Optional configuration

        Yields:
            LangGraphExecution record
        """
        execution = self.track_execution(graph, input_data, config)
        try:
            yield execution
        except Exception as e:
            self.complete_execution(execution.execution_id, error=str(e))
            raise
        else:
            self.complete_execution(execution.execution_id)

    def _convert_to_agent_execution(self, langgraph_execution: LangGraphExecution):
        """Convert LangGraphExecution to AgentExecution for analysis."""
        from .models import AgentExecution, ExecutionStep

        steps = []
        for node in langgraph_execution.executed_nodes:
            step = ExecutionStep(
                step_id=node.node_id,
                name=node.node_name,
                description=f"{node.node_type.value} node",
                status=node.status,
                start_time=node.execution_start,
                end_time=node.execution_end,
                duration_ms=node.duration_ms,
                input_data=node.input_state.data if node.input_state else {},
                output_data=node.output_state.data if node.output_state else {},
                error_message=node.error_message,
                metadata={
                    "node_type": node.node_type.value,
                    "tool_calls": node.tool_calls,
                    **node.metadata,
                },
            )
            steps.append(step)

        agent_execution = AgentExecution(
            execution_id=langgraph_execution.execution_id,
            agent_name=langgraph_execution.graph_name,
            agent_version=langgraph_execution.graph_version,
            task_description=f"LangGraph execution: {langgraph_execution.graph_name}",
            status=langgraph_execution.status,
            start_time=langgraph_execution.start_time,
            end_time=langgraph_execution.end_time,
            total_duration_ms=langgraph_execution.total_duration_ms,
            steps=steps,
            final_output=(
                langgraph_execution.final_state.data
                if langgraph_execution.final_state
                else {}
            ),
            metadata={
                "execution_path": langgraph_execution.execution_path,
                "interruptions": langgraph_execution.interruptions,
                "graph_config": langgraph_execution.config,
                **langgraph_execution.metadata,
            },
        )

        return agent_execution

    def _analyze_graph_structure(self, execution: LangGraphExecution) -> Dict[str, Any]:
        """Analyze the structure of the executed graph."""
        nodes_by_type = {}
        for node in execution.executed_nodes:
            node_type = node.node_type.value
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = 0
            nodes_by_type[node_type] += 1

        return {
            "total_nodes": len(execution.executed_nodes),
            "nodes_by_type": nodes_by_type,
            "execution_path_length": len(execution.execution_path),
            "unique_nodes_executed": len(set(execution.execution_path)),
            "repeated_nodes": len(execution.execution_path)
            - len(set(execution.execution_path)),
        }

    def _analyze_node_performance(
        self, execution: LangGraphExecution
    ) -> Dict[str, Any]:
        """Analyze performance of individual nodes."""
        node_stats = {}

        for node in execution.executed_nodes:
            if node.node_type.value not in node_stats:
                node_stats[node.node_type.value] = {
                    "count": 0,
                    "total_duration": 0,
                    "successes": 0,
                    "failures": 0,
                }

            stats = node_stats[node.node_type.value]
            stats["count"] += 1
            if node.duration_ms:
                stats["total_duration"] += node.duration_ms

            if node.status == ExecutionStatus.SUCCESS:
                stats["successes"] += 1
            elif node.status == ExecutionStatus.FAILED:
                stats["failures"] += 1

        # Calculate averages
        for node_type, stats in node_stats.items():
            if stats["count"] > 0:
                stats["average_duration"] = stats["total_duration"] / stats["count"]
                stats["success_rate"] = stats["successes"] / stats["count"]

        return node_stats

    def _analyze_execution_path(self, execution: LangGraphExecution) -> Dict[str, Any]:
        """Analyze the execution path through the graph."""
        return {
            "path": execution.execution_path,
            "path_length": len(execution.execution_path),
            "unique_nodes": list(set(execution.execution_path)),
            "most_frequent_node": (
                max(set(execution.execution_path), key=execution.execution_path.count)
                if execution.execution_path
                else None
            ),
            "cycles_detected": len(execution.execution_path)
            != len(set(execution.execution_path)),
        }

    def _analyze_state_evolution(self, execution: LangGraphExecution) -> Dict[str, Any]:
        """Analyze how the state evolved through execution."""
        state_changes = []

        if execution.initial_state and execution.final_state:
            initial_keys = set(execution.initial_state.data.keys())
            final_keys = set(execution.final_state.data.keys())

            added_keys = final_keys - initial_keys
            removed_keys = initial_keys - final_keys
            common_keys = initial_keys & final_keys

            state_changes.append(
                {
                    "added_keys": list(added_keys),
                    "removed_keys": list(removed_keys),
                    "modified_keys": [
                        key
                        for key in common_keys
                        if execution.initial_state.data.get(key)
                        != execution.final_state.data.get(key)
                    ],
                }
            )

        return {
            "state_changes": state_changes,
            "initial_state_size": (
                len(execution.initial_state.data) if execution.initial_state else 0
            ),
            "final_state_size": (
                len(execution.final_state.data) if execution.final_state else 0
            ),
        }

    def _analyze_tool_usage(self, execution: LangGraphExecution) -> Dict[str, Any]:
        """Analyze tool usage patterns."""
        all_tool_calls = []
        for node in execution.executed_nodes:
            all_tool_calls.extend(node.tool_calls)

        tool_stats = {}
        for tool_call in all_tool_calls:
            tool_name = tool_call.get("tool", "unknown")
            if tool_name not in tool_stats:
                tool_stats[tool_name] = 0
            tool_stats[tool_name] += 1

        return {
            "total_tool_calls": len(all_tool_calls),
            "unique_tools": len(tool_stats),
            "tool_usage": tool_stats,
        }

    def _identify_graph_patterns(
        self, executions: List[LangGraphExecution]
    ) -> List[str]:
        """Identify common patterns across graph executions."""
        patterns = []

        # Analyze execution paths
        paths = [ex.execution_path for ex in executions]
        if paths:
            # Find most common path
            from collections import Counter

            path_strings = [" -> ".join(path) for path in paths]
            most_common_path = Counter(path_strings).most_common(1)
            if most_common_path:
                patterns.append(f"Most common execution path: {most_common_path[0][0]}")

        return patterns

    def _analyze_node_efficiency(
        self, executions: List[LangGraphExecution]
    ) -> Dict[str, Any]:
        """Analyze node efficiency across executions."""
        node_performance = {}

        for execution in executions:
            for node in execution.executed_nodes:
                node_type = node.node_type.value
                if node_type not in node_performance:
                    node_performance[node_type] = {
                        "durations": [],
                        "success_count": 0,
                        "total_count": 0,
                    }

                perf = node_performance[node_type]
                perf["total_count"] += 1

                if node.duration_ms:
                    perf["durations"].append(node.duration_ms)

                if node.status == ExecutionStatus.SUCCESS:
                    perf["success_count"] += 1

        # Calculate statistics
        for node_type, perf in node_performance.items():
            if perf["durations"]:
                perf["avg_duration"] = sum(perf["durations"]) / len(perf["durations"])
                perf["min_duration"] = min(perf["durations"])
                perf["max_duration"] = max(perf["durations"])

            perf["success_rate"] = (
                perf["success_count"] / perf["total_count"]
                if perf["total_count"] > 0
                else 0
            )

        return node_performance

    def _identify_path_optimizations(
        self, executions: List[LangGraphExecution]
    ) -> List[str]:
        """Identify opportunities for path optimization."""
        optimizations = []

        # Find nodes that are frequently repeated
        all_paths = [ex.execution_path for ex in executions]
        repeated_sequences = []

        for path in all_paths:
            # Simple check for immediate repetitions
            for i in range(len(path) - 1):
                if path[i] == path[i + 1]:
                    repeated_sequences.append(path[i])

        if repeated_sequences:
            from collections import Counter

            most_repeated = Counter(repeated_sequences).most_common(3)
            for node, count in most_repeated:
                optimizations.append(
                    f"Node '{node}' frequently repeats - consider optimization"
                )

        return optimizations

    def _analyze_state_management(
        self, executions: List[LangGraphExecution]
    ) -> Dict[str, Any]:
        """Analyze state management patterns."""
        state_insights = {
            "average_initial_state_size": 0,
            "average_final_state_size": 0,
            "common_state_keys": [],
        }

        if executions:
            initial_sizes = [
                len(ex.initial_state.data) for ex in executions if ex.initial_state
            ]
            final_sizes = [
                len(ex.final_state.data) for ex in executions if ex.final_state
            ]

            if initial_sizes:
                state_insights["average_initial_state_size"] = sum(initial_sizes) / len(
                    initial_sizes
                )
            if final_sizes:
                state_insights["average_final_state_size"] = sum(final_sizes) / len(
                    final_sizes
                )

            # Find common state keys
            all_keys = []
            for ex in executions:
                if ex.initial_state:
                    all_keys.extend(ex.initial_state.data.keys())
                if ex.final_state:
                    all_keys.extend(ex.final_state.data.keys())

            if all_keys:
                from collections import Counter

                common_keys = Counter(all_keys).most_common(5)
                state_insights["common_state_keys"] = [
                    key for key, count in common_keys
                ]

        return state_insights


# Utility functions for easy integration
def create_instrumented_graph(
    graph_builder_func: Callable, tracker: LangGraphTracker
) -> CompiledGraph:
    """
    Create an instrumented LangGraph that automatically tracks execution.

    Args:
        graph_builder_func: Function that builds and returns a compiled graph
        tracker: LangGraphTracker instance

    Returns:
        Instrumented compiled graph
    """
    if not LANGGRAPH_AVAILABLE:
        raise ImportError("LangGraph is not installed")

    # Build the original graph
    original_graph = graph_builder_func()

    # TODO: Add instrumentation hooks
    # This would require deeper integration with LangGraph's execution model
    # For now, return the original graph and rely on manual tracking

    return original_graph


def auto_track_execution(func):
    """
    Decorator to automatically track LangGraph execution.

    Usage:
        @auto_track_execution
        def run_my_graph(input_data):
            # LangGraph execution code
            return result
    """

    def wrapper(*args, **kwargs):
        # This would need access to a global tracker instance
        # Implementation depends on specific use case
        return func(*args, **kwargs)

    return wrapper
