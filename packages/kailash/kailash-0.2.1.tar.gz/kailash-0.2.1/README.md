# Kailash Python SDK

<p align="center">
  <a href="https://pypi.org/project/kailash/"><img src="https://img.shields.io/pypi/v/kailash.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/kailash/"><img src="https://img.shields.io/pypi/pyversions/kailash.svg" alt="Python versions"></a>
  <a href="https://pepy.tech/project/kailash"><img src="https://static.pepy.tech/badge/kailash" alt="Downloads"></a>
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  <img src="https://img.shields.io/badge/tests-734%20passing-brightgreen.svg" alt="Tests: 734 passing">
  <img src="https://img.shields.io/badge/coverage-100%25-brightgreen.svg" alt="Coverage: 100%">
</p>

<p align="center">
  <strong>A Pythonic SDK for the Kailash container-node architecture</strong>
</p>

<p align="center">
  Build workflows that seamlessly integrate with Kailash's production environment while maintaining the flexibility to prototype quickly and iterate locally.
</p>

---

## ✨ Highlights

- 🚀 **Rapid Prototyping**: Create and test workflows locally without containerization
- 🏗️ **Architecture-Aligned**: Automatically ensures compliance with Kailash standards
- 🔄 **Seamless Handoff**: Export prototypes directly to production-ready formats
- 📊 **Real-time Monitoring**: Live dashboards with WebSocket streaming and performance metrics
- 🧩 **Extensible**: Easy to create custom nodes for domain-specific operations
- ⚡ **Fast Installation**: Uses `uv` for lightning-fast Python package management
- 🤖 **AI-Powered**: Complete LLM agents, embeddings, and hierarchical RAG architecture
- 🧠 **Retrieval-Augmented Generation**: Full RAG pipeline with intelligent document processing
- 🌐 **REST API Wrapper**: Expose any workflow as a production-ready API in 3 lines
- 🚪 **Multi-Workflow Gateway**: Manage multiple workflows through unified API with MCP integration
- 🤖 **Self-Organizing Agents**: Autonomous agent pools with intelligent team formation and convergence detection
- 🧠 **Agent-to-Agent Communication**: Shared memory pools and intelligent caching for coordinated multi-agent systems
- 🔒 **Production Security**: Comprehensive security framework with path traversal prevention, code sandboxing, and audit logging
- 🎨 **Visual Workflow Builder**: Kailash Workflow Studio - drag-and-drop interface for creating and managing workflows (coming soon)
- 🔁 **Cyclic Workflows (v0.2.0)**: Universal Hybrid Cyclic Graph Architecture with 30,000+ iterations/second performance
- 🛠️ **Developer Tools**: CycleAnalyzer, CycleDebugger, CycleProfiler for production-ready cyclic workflows
- 📈 **High Performance**: Optimized execution engine supporting 100,000+ iteration workflows

## 🎯 Who Is This For?

The Kailash Python SDK is designed for:

- **AI Business Coaches (ABCs)** who need to prototype workflows quickly
- **Data Scientists** building ML pipelines compatible with production infrastructure
- **Engineers** who want to test Kailash workflows locally before deployment
- **Teams** looking to standardize their workflow development process

## 🚀 Quick Start

### Installation

**Requirements:** Python 3.11 or higher

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# For users: Install from PyPI
pip install kailash

# For developers: Clone and sync
git clone https://github.com/integrum/kailash-python-sdk.git
cd kailash-python-sdk
uv sync
```

### Your First Workflow

```python
from kailash.workflow import Workflow
from kailash.nodes.data import CSVReaderNode
from kailash.nodes.code import PythonCodeNode
from kailash.runtime.local import LocalRuntime
import pandas as pd

# Create a workflow
workflow = Workflow("customer_analysis", name="customer_analysis")

# Add data reader
reader = CSVReaderNode(file_path="customers.csv")
workflow.add_node("read_customers", reader)

# Add custom processing using Python code
def analyze_customers(data):
    """Analyze customer data and compute metrics."""
    df = pd.DataFrame(data)
    # Convert total_spent to numeric
    df['total_spent'] = pd.to_numeric(df['total_spent'])
    return {
        "result": {
            "total_customers": len(df),
            "avg_spend": df["total_spent"].mean(),
            "top_customers": df.nlargest(10, "total_spent").to_dict("records")
        }
    }

analyzer = PythonCodeNode.from_function(analyze_customers, name="analyzer")
workflow.add_node("analyze", analyzer)

# Connect nodes
workflow.connect("read_customers", "analyze", {"data": "data"})

# Run locally
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow)
print(f"Analysis complete! Results: {results}")

# Export for production
from kailash.utils.export import WorkflowExporter
exporter = WorkflowExporter()
workflow.save("customer_analysis.yaml", format="yaml")
```

### SharePoint Integration Example

```python
from kailash.workflow import Workflow
from kailash.nodes.data import SharePointGraphReader, CSVWriterNode
import os

# Create workflow for SharePoint file processing
workflow = Workflow("sharepoint_processor", name="sharepoint_processor")

# Configure SharePoint reader (using environment variables)
sharepoint = SharePointGraphReader()
workflow.add_node("read_sharepoint", sharepoint)

# Process downloaded files
csv_writer = CSVWriterNode(file_path="sharepoint_output.csv")
workflow.add_node("save_locally", csv_writer)

# Connect nodes
workflow.connect("read_sharepoint", "save_locally")

# Execute with credentials
from kailash.runtime.local import LocalRuntime

inputs = {
    "read_sharepoint": {
        "tenant_id": os.getenv("SHAREPOINT_TENANT_ID"),
        "client_id": os.getenv("SHAREPOINT_CLIENT_ID"),
        "client_secret": os.getenv("SHAREPOINT_CLIENT_SECRET"),
        "site_url": "https://yourcompany.sharepoint.com/sites/YourSite",
        "operation": "list_files",
        "library_name": "Documents"
    }
}

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow, inputs=inputs)
```

### Hierarchical RAG Example

```python
from kailash.workflow import Workflow
from kailash.nodes.ai.embedding_generator import EmbeddingGeneratorNode
from kailash.nodes.ai.llm_agent import LLMAgentNode
from kailash.nodes.data.sources import DocumentSourceNode, QuerySourceNode
from kailash.nodes.data.retrieval import RelevanceScorerNode
from kailash.nodes.transform.chunkers import HierarchicalChunkerNode
from kailash.nodes.transform.formatters import (
    ChunkTextExtractorNode, QueryTextWrapperNode, ContextFormatterNode
)

# Create hierarchical RAG workflow
workflow = Workflow("hierarchical_rag", name="Hierarchical RAG Workflow")

# Data sources (autonomous - no external files needed)
doc_source = DocumentSourceNode()
query_source = QuerySourceNode()

# Document processing pipeline
chunker = HierarchicalChunkerNode()
chunk_text_extractor = ChunkTextExtractorNode()
query_text_wrapper = QueryTextWrapperNode()

# AI processing with Ollama
chunk_embedder = EmbeddingGeneratorNode(
    provider="ollama", model="nomic-embed-text", operation="embed_batch"
)
query_embedder = EmbeddingGeneratorNode(
    provider="ollama", model="nomic-embed-text", operation="embed_batch"
)

# Retrieval and response generation
relevance_scorer = RelevanceScorerNode()
context_formatter = ContextFormatterNode()
llm_agent = LLMAgentNode(provider="ollama", model="llama3.2", temperature=0.7)

# Add all nodes to workflow
for name, node in {
    "doc_source": doc_source, "query_source": query_source,
    "chunker": chunker, "chunk_text_extractor": chunk_text_extractor,
    "query_text_wrapper": query_text_wrapper, "chunk_embedder": chunk_embedder,
    "query_embedder": query_embedder, "relevance_scorer": relevance_scorer,
    "context_formatter": context_formatter, "llm_agent": llm_agent
}.items():
    workflow.add_node(name, node)

# Connect the RAG pipeline
workflow.connect("doc_source", "chunker", {"documents": "documents"})
workflow.connect("chunker", "chunk_text_extractor", {"chunks": "chunks"})
workflow.connect("chunk_text_extractor", "chunk_embedder", {"input_texts": "input_texts"})
workflow.connect("query_source", "query_text_wrapper", {"query": "query"})
workflow.connect("query_text_wrapper", "query_embedder", {"input_texts": "input_texts"})
workflow.connect("chunker", "relevance_scorer", {"chunks": "chunks"})
workflow.connect("query_embedder", "relevance_scorer", {"embeddings": "query_embedding"})
workflow.connect("chunk_embedder", "relevance_scorer", {"embeddings": "chunk_embeddings"})
workflow.connect("relevance_scorer", "context_formatter", {"relevant_chunks": "relevant_chunks"})
workflow.connect("query_source", "context_formatter", {"query": "query"})
workflow.connect("context_formatter", "llm_agent", {"messages": "messages"})

# Execute the RAG workflow
from kailash.runtime.local import LocalRuntime
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow)

print("RAG Response:", results["llm_agent"]["response"])
```

### Cyclic Workflows - Iterative Processing with Convergence

Build workflows that iterate until a condition is met, perfect for optimization, retries, and ML training:

```python
from kailash.workflow import Workflow
from kailash.nodes.base_cycle_aware import CycleAwareNode
from kailash.nodes.base import NodeParameter
from kailash.runtime.local import LocalRuntime
from typing import Any, Dict

# Create a custom cycle-aware node for data quality improvement
class DataQualityImproverNode(CycleAwareNode):
    def get_parameters(self) -> Dict[str, NodeParameter]:
        return {
            "data": NodeParameter(name="data", type=list, required=True),
            "target_quality": NodeParameter(name="target_quality", type=float, required=False, default=0.95)
        }

    def run(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Iteratively improve data quality."""
        data = kwargs["data"]
        target_quality = kwargs.get("target_quality", 0.95)

        # Get current iteration and previous state
        iteration = self.get_iteration(context)
        prev_state = self.get_previous_state(context)

        # Calculate current quality
        quality = prev_state.get("quality", 0.5) + 0.1  # Improve by 10% each iteration
        quality = min(quality, 1.0)

        # Process data (simplified)
        processed_data = [item for item in data if item is not None]

        # Track quality history
        quality_history = self.accumulate_values(context, "quality_history", quality, max_history=10)

        # Detect convergence trend
        trend = self.detect_convergence_trend(context, "quality_history", window_size=5)
        converged = quality >= target_quality or (trend and trend["slope"] < 0.01)

        # Log progress
        self.log_cycle_info(context, f"Iteration {iteration}: Quality={quality:.2%}")

        # Save state for next iteration
        self.set_cycle_state({"quality": quality, "processed_count": len(processed_data)})

        return {
            "data": processed_data,
            "quality": quality,
            "converged": converged,
            "iteration": iteration,
            "history": quality_history
        }

# Build cyclic workflow
workflow = Workflow("quality_improvement", "Iterative Data Quality")
workflow.add_node("improver", DataQualityImproverNode())

# Create a cycle - node connects to itself!
workflow.connect("improver", "improver",
                 mapping={"data": "data"},  # Pass data to next iteration
                 cycle=True,  # This is a cycle
                 max_iterations=20,  # Safety limit
                 convergence_check="converged == True")  # Stop condition

# Execute with automatic iteration management
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow, parameters={
    "improver": {
        "data": [1, None, 3, None, 5, 6, None, 8, 9, 10],
        "target_quality": 0.9
    }
})

print(f"Converged after {results['improver']['iteration']} iterations")
print(f"Final quality: {results['improver']['quality']:.2%}")
print(f"Quality history: {results['improver']['history']}")
```

### NEW in v0.2.0: CycleBuilder API

The new CycleBuilder API provides a fluent interface for creating cyclic workflows:

```python
# Modern approach with CycleBuilder
workflow.create_cycle("optimization_loop")
    .connect("gradient", "optimizer")
    .connect("optimizer", "evaluator")
    .connect("evaluator", "gradient")
    .max_iterations(100)
    .converge_when("loss < 0.01")
    .early_stop_when("gradient_norm < 1e-6")
    .checkpoint_every(10)
    .build()

# Developer tools for production workflows
from kailash.workflow import CycleAnalyzer, CycleDebugger, CycleProfiler

# Analyze cycle patterns
analyzer = CycleAnalyzer(workflow)
report = analyzer.analyze()
print(f"Found {len(report.cycles)} cycles")
print(f"Max depth: {report.max_cycle_depth}")

# Debug with breakpoints
debugger = CycleDebugger(workflow)
debugger.set_breakpoint("optimizer", iteration=50)
debugger.set_trace("gradient_norm", lambda x: x < 0.001)

# Profile performance
profiler = CycleProfiler(workflow)
profile_data = profiler.profile(runtime, parameters)
print(f"Bottleneck: {profile_data.bottleneck_node}")
print(f"Iterations/sec: {profile_data.iterations_per_second}")
```

#### Cyclic Workflow Features

- **Built-in Iteration Management**: No manual loops or recursion needed
- **State Persistence**: Maintain state across iterations with `get_previous_state()` and `set_cycle_state()`
- **Convergence Detection**: Automatic trend analysis with `detect_convergence_trend()`
- **Value Accumulation**: Track metrics over time with `accumulate_values()`
- **Safety Limits**: Max iterations prevent infinite loops
- **Performance**: Optimized execution with ~30,000 iterations/second
- **Developer Tools**: CycleAnalyzer, CycleDebugger, CycleProfiler for production workflows

Common cyclic patterns include:
- **Retry with Backoff**: ETL pipelines with automatic retry
- **Optimization Loops**: Iterative parameter tuning
- **ML Training**: Training until accuracy threshold
- **Polling**: API polling with rate limiting
- **Stream Processing**: Windowed data processing

### Workflow API Wrapper - Expose Workflows as REST APIs

Transform any Kailash workflow into a production-ready REST API in just 3 lines of code:

```python
from kailash.api.workflow_api import WorkflowAPI

# Take any workflow and expose it as an API
api = WorkflowAPI(workflow)
api.run(port=8000)  # That's it! Your workflow is now a REST API
```

#### Features

- **Automatic REST Endpoints**:
  - `POST /execute` - Execute workflow with inputs
  - `GET /workflow/info` - Get workflow metadata
  - `GET /health` - Health check endpoint
  - Automatic OpenAPI docs at `/docs`

- **Multiple Execution Modes**:
  ```python
  # Synchronous execution (wait for results)
  curl -X POST http://localhost:8000/execute \
    -d '{"inputs": {...}, "mode": "sync"}'

  # Asynchronous execution (get execution ID)
  curl -X POST http://localhost:8000/execute \
    -d '{"inputs": {...}, "mode": "async"}'

  # Check async status
  curl http://localhost:8000/status/{execution_id}
  ```

- **Specialized APIs** for specific domains:
  ```python
  from kailash.api.workflow_api import create_workflow_api

  # Create a RAG-specific API with custom endpoints
  api = create_workflow_api(rag_workflow, api_type="rag")
  # Adds /documents and /query endpoints
  ```

- **Production Ready**:
  ```python
  # Development
  api.run(reload=True, log_level="debug")

  # Production with SSL
  api.run(
      host="0.0.0.0",
      port=443,
      ssl_keyfile="key.pem",
      ssl_certfile="cert.pem",
      workers=4
  )
  ```

See the [API demo example](examples/integration_examples/integration_api_demo.py) for complete usage patterns.

### Multi-Workflow API Gateway - Manage Multiple Workflows

Run multiple workflows through a single unified API gateway with dynamic routing and MCP integration:

```python
from kailash.api.gateway import WorkflowAPIGateway
from kailash.api.mcp_integration import MCPIntegration

# Create gateway
gateway = WorkflowAPIGateway(
    title="Enterprise Platform",
    description="Unified API for all workflows"
)

# Register multiple workflows
gateway.register_workflow("sales", sales_workflow)
gateway.register_workflow("analytics", analytics_workflow)
gateway.register_workflow("reports", reporting_workflow)

# Add AI-powered tools via MCP
mcp = MCPIntegration("ai_tools")
mcp.add_tool("analyze", analyze_function)
mcp.add_tool("predict", predict_function)
gateway.register_mcp_server("ai", mcp)

# Run unified server
gateway.run(port=8000)
```

#### Gateway Features

- **Unified Access Point**: All workflows accessible through one server
  - `/sales/execute` - Execute sales workflow
  - `/analytics/execute` - Execute analytics workflow
  - `/workflows` - List all available workflows
  - `/health` - Check health of all services

- **MCP Integration**: AI-powered tools available to all workflows
  ```python
  # Use MCP tools in workflows
  from kailash.api.mcp_integration import MCPToolNode

  tool_node = MCPToolNode(
      mcp_server="ai_tools",
      tool_name="analyze"
  )
  workflow.add_node("ai_analysis", tool_node)
  ```

- **Flexible Deployment Patterns**:
  ```python
  # Pattern 1: Single Gateway (most cases)
  gateway.register_workflow("workflow1", wf1)
  gateway.register_workflow("workflow2", wf2)

  # Pattern 2: Hybrid (heavy workflows separate)
  gateway.register_workflow("light", light_wf)
  gateway.proxy_workflow("heavy", "http://gpu-service:8080")

  # Pattern 3: High Availability
  # Run multiple gateway instances behind load balancer

  # Pattern 4: Kubernetes
  # Deploy with horizontal pod autoscaling
  ```

- **Production Features**:
  - WebSocket support for real-time updates
  - Health monitoring across all workflows
  - Dynamic workflow registration/unregistration
  - Built-in CORS and authentication support

See the [Gateway examples](examples/integration_examples/gateway_comprehensive_demo.py) for complete implementation patterns.

### Self-Organizing Agent Pools - Autonomous Multi-Agent Systems

Build intelligent agent systems that can autonomously form teams, share information, and solve complex problems collaboratively:

```python
from kailash import Workflow
from kailash.runtime import LocalRuntime
from kailash.nodes.ai.intelligent_agent_orchestrator import (
    OrchestrationManagerNode,
    IntelligentCacheNode,
    ConvergenceDetectorNode
)
from kailash.nodes.ai.self_organizing import (
    AgentPoolManagerNode,
    TeamFormationNode,
    ProblemAnalyzerNode
)
from kailash.nodes.ai.a2a import SharedMemoryPoolNode, A2AAgentNode

# Create self-organizing agent workflow
workflow = Workflow("self_organizing_research")

# Shared infrastructure
memory_pool = SharedMemoryPoolNode(
    memory_size_limit=1000,
    attention_window=50
)
workflow.add_node("memory", memory_pool)

# Intelligent caching to prevent redundant operations
cache = IntelligentCacheNode(
    ttl=3600,  # 1 hour cache
    similarity_threshold=0.8,
    max_entries=1000
)
workflow.add_node("cache", cache)

# Problem analysis and team formation
problem_analyzer = ProblemAnalyzerNode()
team_former = TeamFormationNode(
    formation_strategy="capability_matching",
    optimization_rounds=3
)
workflow.add_node("analyzer", problem_analyzer)
workflow.add_node("team_former", team_former)

# Self-organizing agent pool
pool_manager = AgentPoolManagerNode(
    max_active_agents=20,
    agent_timeout=120
)
workflow.add_node("pool", pool_manager)

# Convergence detection for stopping criteria
convergence = ConvergenceDetectorNode(
    quality_threshold=0.85,
    improvement_threshold=0.02,
    max_iterations=10
)
workflow.add_node("convergence", convergence)

# Orchestration manager coordinates the entire system
orchestrator = OrchestrationManagerNode(
    max_iterations=10,
    quality_threshold=0.85,
    parallel_execution=True
)
workflow.add_node("orchestrator", orchestrator)

# Execute with complex business problem
runtime = LocalRuntime()
result, _ = runtime.execute(workflow, parameters={
    "orchestrator": {
        "query": "Analyze market trends and develop growth strategy for fintech",
        "agent_pool_size": 12,
        "mcp_servers": [
            {"name": "market_data", "command": "python", "args": ["-m", "market_mcp"]},
            {"name": "financial", "command": "python", "args": ["-m", "finance_mcp"]},
            {"name": "research", "command": "python", "args": ["-m", "research_mcp"]}
        ],
        "context": {
            "domain": "fintech",
            "depth": "comprehensive",
            "output_format": "strategic_report"
        }
    }
})

print(f"Solution Quality: {result['orchestrator']['quality_score']:.2%}")
print(f"Agents Used: {result['orchestrator']['agents_deployed']}")
print(f"Iterations: {result['orchestrator']['iterations_completed']}")
print(f"Final Strategy: {result['orchestrator']['final_solution']['strategy']}")
```

#### Key Self-Organizing Features

- **Autonomous Team Formation**: Agents automatically form optimal teams based on:
  - Capability matching for skill-specific tasks
  - Swarm-based formation for exploration
  - Market-based allocation for resource constraints
  - Hierarchical organization for complex problems

- **Intelligent Information Sharing**:
  - **SharedMemoryPoolNode**: Selective attention mechanisms for relevant information
  - **IntelligentCacheNode**: Semantic similarity detection prevents redundant operations
  - **A2AAgentNode**: Direct agent-to-agent communication with context awareness

- **Convergence Detection**: Automatic termination when:
  - Solution quality exceeds threshold (e.g., 85% confidence)
  - Improvement rate drops below minimum (e.g., <2% per iteration)
  - Maximum iterations reached
  - Time limits exceeded

- **MCP Integration**: Agents can access external tools and data sources:
  - File systems, databases, APIs
  - Web scraping and research tools
  - Specialized domain knowledge bases
  - Real-time data streams

- **Performance Optimization**:
  - Multi-level caching strategies
  - Parallel agent execution
  - Resource management and monitoring
  - Cost tracking for API usage

See the [Self-Organizing Agents examples](examples/integration_examples/) for complete implementation patterns and the [Agent Systems Guide](docs/guides/self_organizing_agents.rst) for detailed documentation.

### Zero-Code MCP Ecosystem - Visual Workflow Builder

Build and deploy workflows through an interactive web interface without writing any code:

```python
from kailash.api.gateway import WorkflowAPIGateway
from kailash.api.mcp_integration import MCPServerRegistry

# Run the MCP ecosystem demo
# cd examples/integration_examples
# ./run_ecosystem.sh

# Or run programmatically:
python examples/integration_examples/mcp_ecosystem_demo.py
```

#### Features

- **Drag-and-Drop Builder**: Visual interface for creating workflows
  - Drag nodes from palette (CSV Reader, Python Code, JSON Writer, etc.)
  - Drop onto canvas to build workflows
  - Deploy with one click

- **Live Dashboard**: Real-time monitoring and statistics
  - Connected MCP server status
  - Running workflow count
  - Execution logs with timestamps

- **Pre-built Templates**: One-click deployment
  - GitHub → Slack Notifier
  - Data Processing Pipeline (CSV → Transform → JSON)
  - AI Research Assistant

- **Technology Stack**: Lightweight and fast
  - Backend: FastAPI + Kailash SDK
  - Frontend: Vanilla HTML/CSS/JavaScript (no frameworks)
  - Zero build process required

See the [MCP Ecosystem example](examples/integration_examples/) for the complete zero-code workflow deployment platform.

## 📚 Documentation

| Resource | Description |
|----------|-------------|
| 📖 [User Guide](docs/user-guide.md) | Comprehensive guide for using the SDK |
| 📋 [API Reference](docs/) | Detailed API documentation |
| 🌐 [API Integration Guide](examples/API_INTEGRATION_README.md) | Complete API integration documentation |
| 🎓 [Examples](examples/) | Working examples and tutorials |
| 🤝 [Contributing](CONTRIBUTING.md) | Contribution guidelines |

## 🛠️ Features

### 📦 Pre-built Nodes

The SDK includes a rich set of pre-built nodes for common operations:

<table>
<tr>
<td width="50%">

**Data Operations**
- `CSVReaderNode` - Read CSV files
- `JSONReaderNode` - Read JSON files
- `DocumentSourceNode` - Sample document provider
- `QuerySourceNode` - Sample query provider
- `RelevanceScorerNode` - Multi-method similarity
- `SQLDatabaseNode` - Query databases
- `CSVWriterNode` - Write CSV files
- `JSONWriterNode` - Write JSON files

</td>
<td width="50%">

**Transform Nodes**
- `PythonCodeNode` - Custom Python logic
- `DataTransformer` - Transform data
- `HierarchicalChunkerNode` - Document chunking
- `ChunkTextExtractorNode` - Extract chunk text
- `QueryTextWrapperNode` - Wrap queries for processing
- `ContextFormatterNode` - Format LLM context
- `Filter` - Filter records
- `Aggregator` - Aggregate data

**Logic Nodes**
- `SwitchNode` - Conditional routing
- `MergeNode` - Combine multiple inputs
- `WorkflowNode` - Wrap workflows as reusable nodes

</td>
</tr>
<tr>
<td width="50%">

**AI/ML Nodes**
- `LLMAgentNode` - Multi-provider LLM with memory & tools
- `EmbeddingGeneratorNode` - Vector embeddings with caching
- `MCPClient/MCPServer` - Model Context Protocol
- `TextClassifier` - Text classification
- `SentimentAnalyzer` - Sentiment analysis
- `NamedEntityRecognizer` - NER extraction

**Self-Organizing Agent Nodes**
- `SharedMemoryPoolNode` - Agent memory sharing
- `A2AAgentNode` - Agent-to-agent communication
- `A2ACoordinatorNode` - Multi-agent coordination
- `IntelligentCacheNode` - Semantic caching system
- `MCPAgentNode` - MCP-enabled agents
- `QueryAnalysisNode` - Query complexity analysis
- `OrchestrationManagerNode` - System orchestration
- `ConvergenceDetectorNode` - Solution convergence
- `AgentPoolManagerNode` - Agent pool management
- `ProblemAnalyzerNode` - Problem decomposition
- `TeamFormationNode` - Optimal team creation
- `SolutionEvaluatorNode` - Multi-criteria evaluation
- `SelfOrganizingAgentNode` - Adaptive individual agents

</td>
<td width="50%">

**API Integration Nodes**
- `HTTPRequestNode` - HTTP requests
- `RESTAPINode` - REST API client
- `GraphQLClientNode` - GraphQL queries
- `OAuth2AuthNode` - OAuth 2.0 authentication
- `RateLimitedAPINode` - Rate-limited API calls

**Other Integration Nodes**
- `KafkaConsumerNode` - Kafka streaming
- `WebSocketNode` - WebSocket connections
- `EmailNode` - Send emails

**SharePoint Integration**
- `SharePointGraphReader` - Read SharePoint files
- `SharePointGraphWriter` - Upload to SharePoint

**Real-time Monitoring**
- `RealTimeDashboard` - Live workflow monitoring
- `WorkflowPerformanceReporter` - Comprehensive reports
- `SimpleDashboardAPI` - REST API for metrics
- `DashboardAPIServer` - WebSocket streaming server

</td>
</tr>
</table>

### 🔧 Core Capabilities

#### Workflow Management
```python
from kailash.workflow import Workflow
from kailash.nodes.logic import SwitchNode
from kailash.nodes.transform import DataTransformer

# Create complex workflows with branching logic
workflow = Workflow("data_pipeline", name="data_pipeline")

# Add conditional branching with SwitchNode
switch = SwitchNode()
workflow.add_node("route", switch)

# Different paths based on validation
processor_a = DataTransformer(transformations=["lambda x: x"])
error_handler = DataTransformer(transformations=["lambda x: {'error': str(x)}"])
workflow.add_node("process_valid", processor_a)
workflow.add_node("handle_errors", error_handler)

# Connect with switch routing
workflow.connect("route", "process_valid")
workflow.connect("route", "handle_errors")
```

#### Hierarchical Workflow Composition
```python
from kailash.workflow import Workflow
from kailash.nodes.logic import WorkflowNode
from kailash.runtime.local import LocalRuntime

# Create a reusable data processing workflow
inner_workflow = Workflow("data_processor", name="Data Processor")
# ... add nodes to inner workflow ...

# Wrap the workflow as a node
processor_node = WorkflowNode(
    workflow=inner_workflow,
    name="data_processor"
)

# Use in a larger workflow
main_workflow = Workflow("main", name="Main Pipeline")
main_workflow.add_node("process", processor_node)
main_workflow.add_node("analyze", analyzer_node)

# Connect workflows
main_workflow.connect("process", "analyze")

# Execute - parameters automatically mapped to inner workflow
runtime = LocalRuntime()
results, _ = runtime.execute(main_workflow)
```

#### Immutable State Management
```python
from kailash.workflow import Workflow
from kailash.workflow.state import WorkflowStateWrapper
from pydantic import BaseModel

# Define state model
class MyStateModel(BaseModel):
    counter: int = 0
    status: str = "pending"
    nested: dict = {}

# Create workflow
workflow = Workflow("state_workflow", name="state_workflow")

# Create and wrap state object
state = MyStateModel()
state_wrapper = workflow.create_state_wrapper(state)

# Single path-based update
updated_wrapper = state_wrapper.update_in(
    ["counter"],
    42
)

# Batch update multiple fields atomically
updated_wrapper = state_wrapper.batch_update([
    (["counter"], 10),
    (["status"], "processing")
])

# Access the updated state
print(f"Updated counter: {updated_wrapper._state.counter}")
print(f"Updated status: {updated_wrapper._state.status}")
```

#### Task Tracking
```python
from kailash.tracking import TaskManager

# Initialize task manager
task_manager = TaskManager()

# Create a sample workflow
from kailash.workflow import Workflow
workflow = Workflow("sample_workflow", name="Sample Workflow")

# Run workflow with tracking
from kailash.runtime.local import LocalRuntime
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow)

# Query execution history
# Note: list_runs() may fail with timezone comparison errors in some cases
try:
    # List all runs
    all_runs = task_manager.list_runs()

    # Filter by status
    completed_runs = task_manager.list_runs(status="completed")
    failed_runs = task_manager.list_runs(status="failed")

    # Filter by workflow name
    workflow_runs = task_manager.list_runs(workflow_name="sample_workflow")

    # Process run information
    for run in completed_runs[:5]:  # First 5 runs
        print(f"Run {run.run_id[:8]}: {run.workflow_name} - {run.status}")

except Exception as e:
    print(f"Error listing runs: {e}")
    # Fallback: Access run details directly if available
    if hasattr(task_manager, 'storage'):
        run = task_manager.get_run(run_id)
```

#### Local Testing
```python
from kailash.runtime.local import LocalRuntime
from kailash.workflow import Workflow

# Create a test workflow
workflow = Workflow("test_workflow", name="test_workflow")

# Create test runtime with debugging enabled
runtime = LocalRuntime(debug=True)

# Execute with test data
results, run_id = runtime.execute(workflow)

# Validate results
assert isinstance(results, dict)
```

#### Performance Monitoring & Real-time Dashboards
```python
from kailash.visualization.performance import PerformanceVisualizer
from kailash.visualization.dashboard import RealTimeDashboard, DashboardConfig
from kailash.visualization.reports import WorkflowPerformanceReporter, ReportFormat
from kailash.tracking import TaskManager
from kailash.runtime.local import LocalRuntime
from kailash.workflow import Workflow
from kailash.nodes.transform import DataTransformer

# Create a workflow to monitor
workflow = Workflow("monitored_workflow", name="monitored_workflow")
node = DataTransformer(transformations=["lambda x: x"])
workflow.add_node("transform", node)

# Run workflow with task tracking
# Note: Pass task_manager to execute() to enable performance tracking
task_manager = TaskManager()
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow, task_manager=task_manager)

# Static performance analysis
from pathlib import Path
perf_viz = PerformanceVisualizer(task_manager)
outputs = perf_viz.create_run_performance_summary(run_id, output_dir=Path("performance_report"))

# Real-time monitoring dashboard
config = DashboardConfig(
    update_interval=1.0,
    max_history_points=100,
    auto_refresh=True,
    theme="light"
)

dashboard = RealTimeDashboard(task_manager, config)
dashboard.start_monitoring(run_id)

# Add real-time callbacks
def on_metrics_update(metrics):
    print(f"Tasks: {metrics.completed_tasks} completed, {metrics.active_tasks} active")

dashboard.add_metrics_callback(on_metrics_update)

# Generate live HTML dashboard
dashboard.generate_live_report("live_dashboard.html", include_charts=True)
dashboard.stop_monitoring()

# Comprehensive performance reports
reporter = WorkflowPerformanceReporter(task_manager)
report_path = reporter.generate_report(
    run_id,
    output_path="workflow_report.html",
    format=ReportFormat.HTML
)
```

**Real-time Dashboard Features**:
- ⚡ **Live Metrics Streaming**: Real-time task progress and resource monitoring
- 📊 **Interactive Charts**: CPU, memory, and throughput visualizations with Chart.js
- 🔌 **API Endpoints**: REST and WebSocket APIs for custom integrations
- 📈 **Performance Reports**: Multi-format reports (HTML, Markdown, JSON) with insights
- 🎯 **Bottleneck Detection**: Automatic identification of performance issues
- 📱 **Responsive Design**: Mobile-friendly dashboards with auto-refresh

**Performance Metrics Collected**:
- **Execution Timeline**: Gantt charts showing node execution order and duration
- **Resource Usage**: Real-time CPU and memory consumption
- **I/O Analysis**: Read/write operations and data transfer volumes
- **Performance Heatmaps**: Identify bottlenecks across workflow runs
- **Throughput Metrics**: Tasks per minute and completion rates
- **Error Tracking**: Failed task analysis and error patterns

#### API Integration
```python
from kailash.nodes.api import (
    HTTPRequestNode as RESTAPINode,
    # OAuth2AuthNode,
    # RateLimitedAPINode,
    # RateLimitConfig
)

# OAuth 2.0 authentication
# # auth_node = OAuth2AuthNode(
#     client_id="your_client_id",
#     client_secret="your_client_secret",
#     token_url="https://api.example.com/oauth/token"
# )

# Rate-limited API client
rate_config = None  # RateLimitConfig(
#     max_requests=100,
#     time_window=60.0,
#     strategy="token_bucket"
# )

api_client = RESTAPINode(
    base_url="https://api.example.com"
    # auth_node=auth_node
)

# rate_limited_client = RateLimitedAPINode(
#     wrapped_node=api_client,
#     rate_limit_config=rate_config
# )
```

#### Export Formats
```python
from kailash.utils.export import WorkflowExporter, ExportConfig
from kailash.workflow import Workflow
from kailash.nodes.transform import DataTransformer

# Create a workflow to export
workflow = Workflow("export_example", name="export_example")
node = DataTransformer(transformations=["lambda x: x"])
workflow.add_node("transform", node)

exporter = WorkflowExporter()

# Export to different formats
workflow.save("workflow.yaml", format="yaml")  # Kailash YAML format
workflow.save("workflow.json", format="json")  # JSON representation

# Export with custom configuration
config = ExportConfig(
    include_metadata=True,
    container_tag="latest"
)
workflow.save("deployment.yaml")
```

### 🎨 Visualization

```python
from kailash.workflow import Workflow
from kailash.workflow.visualization import WorkflowVisualizer
from kailash.nodes.transform import DataTransformer

# Create a workflow to visualize
workflow = Workflow("viz_example", name="viz_example")
node = DataTransformer(transformations=["lambda x: x"])
workflow.add_node("transform", node)

# Generate Mermaid diagram (recommended for documentation)
mermaid_code = workflow.to_mermaid()
print(mermaid_code)

# Save as Mermaid markdown file
with open("workflow.md", "w") as f:
    f.write(workflow.to_mermaid_markdown(title="My Workflow"))

# Or use matplotlib visualization
visualizer = WorkflowVisualizer(workflow)
visualizer.visualize()
visualizer.save("workflow.png", dpi=300)  # Save as PNG
```

#### Hierarchical RAG (Retrieval-Augmented Generation)
```python
from kailash.workflow import Workflow
from kailash.nodes.data.sources import DocumentSourceNode, QuerySourceNode
from kailash.nodes.data.retrieval import RelevanceScorerNode
from kailash.nodes.transform.chunkers import HierarchicalChunkerNode
from kailash.nodes.transform.formatters import (
    ChunkTextExtractorNode,
    QueryTextWrapperNode,
    ContextFormatterNode,
)
from kailash.nodes.ai.llm_agent import LLMAgent
from kailash.nodes.ai.embedding_generator import EmbeddingGenerator

# Create hierarchical RAG workflow
workflow = Workflow(
    workflow_id="hierarchical_rag_example",
    name="Hierarchical RAG Workflow",
    description="Complete RAG pipeline with embedding-based retrieval",
    version="1.0.0"
)

# Create data source nodes
doc_source = DocumentSourceNode()
query_source = QuerySourceNode()

# Create document processing pipeline
chunker = HierarchicalChunkerNode()
chunk_text_extractor = ChunkTextExtractorNode()
query_text_wrapper = QueryTextWrapperNode()

# Create embedding generators
chunk_embedder = EmbeddingGeneratorNode(
    provider="ollama",
    model="nomic-embed-text",
    operation="embed_batch"
)

query_embedder = EmbeddingGeneratorNode(
    provider="ollama",
    model="nomic-embed-text",
    operation="embed_batch"
)

# Create retrieval and formatting nodes
relevance_scorer = RelevanceScorerNode(similarity_method="cosine")
context_formatter = ContextFormatterNode()

# Create LLM agent for final answer generation
llm_agent = LLMAgentNode(
    provider="ollama",
    model="llama3.2",
    temperature=0.7,
    max_tokens=500
)

# Add all nodes to workflow
for node_id, node in [
    ("doc_source", doc_source),
    ("chunker", chunker),
    ("query_source", query_source),
    ("chunk_text_extractor", chunk_text_extractor),
    ("query_text_wrapper", query_text_wrapper),
    ("chunk_embedder", chunk_embedder),
    ("query_embedder", query_embedder),
    ("relevance_scorer", relevance_scorer),
    ("context_formatter", context_formatter),
    ("llm_agent", llm_agent)
]:
    workflow.add_node(node_id, node)

# Connect the workflow pipeline
# Document processing: docs → chunks → text → embeddings
workflow.connect("doc_source", "chunker", {"documents": "documents"})
workflow.connect("chunker", "chunk_text_extractor", {"chunks": "chunks"})
workflow.connect("chunk_text_extractor", "chunk_embedder", {"input_texts": "input_texts"})

# Query processing: query → text wrapper → embeddings
workflow.connect("query_source", "query_text_wrapper", {"query": "query"})
workflow.connect("query_text_wrapper", "query_embedder", {"input_texts": "input_texts"})

# Relevance scoring: chunks + embeddings → scored chunks
workflow.connect("chunker", "relevance_scorer", {"chunks": "chunks"})
workflow.connect("query_embedder", "relevance_scorer", {"embeddings": "query_embedding"})
workflow.connect("chunk_embedder", "relevance_scorer", {"embeddings": "chunk_embeddings"})

# Context formatting: relevant chunks + query → formatted context
workflow.connect("relevance_scorer", "context_formatter", {"relevant_chunks": "relevant_chunks"})
workflow.connect("query_source", "context_formatter", {"query": "query"})

# Final answer generation: formatted context → LLM response
workflow.connect("context_formatter", "llm_agent", {"messages": "messages"})

# Execute workflow
results, run_id = workflow.run()

# Access results
print("🎯 Top Relevant Chunks:")
for chunk in results["relevance_scorer"]["relevant_chunks"]:
    print(f"  - {chunk['document_title']}: {chunk['relevance_score']:.3f}")

print("\n🤖 Final Answer:")
print(results["llm_agent"]["response"]["content"])
```

This example demonstrates:
- **Document chunking** with hierarchical structure
- **Vector embeddings** using Ollama's nomic-embed-text model
- **Semantic similarity** scoring with cosine similarity
- **Context formatting** for LLM input
- **Answer generation** using Ollama's llama3.2 model

### 🔒 Access Control and Security

Kailash SDK provides comprehensive access control and security features for enterprise deployments:

#### Role-Based Access Control (RBAC)
```python
from kailash.access_control import UserContext, PermissionRule, NodePermission
from kailash.runtime.access_controlled import AccessControlledRuntime

# Define user with roles
user = UserContext(
    user_id="analyst_001",
    tenant_id="company_abc",
    email="analyst@company.com",
    roles=["analyst", "viewer"]
)

# Create secure runtime
runtime = AccessControlledRuntime(user_context=user)

# Execute workflow with automatic permission checks
results, run_id = runtime.execute(workflow, parameters={})
```

#### Multi-Tenant Isolation
```python
from kailash.access_control import get_access_control_manager, PermissionEffect, WorkflowPermission

# Configure tenant-based access rules
acm = get_access_control_manager()
acm.enabled = True

# Tenant isolation rule
acm.add_rule(PermissionRule(
    id="tenant_isolation",
    resource_type="workflow",
    resource_id="customer_analytics",
    permission=WorkflowPermission.EXECUTE,
    effect=PermissionEffect.ALLOW,
    tenant_id="company_abc"  # Only this tenant can access
))
```

#### Data Masking and Field Protection
```python
from kailash.nodes.base_with_acl import add_access_control

# Add access control to sensitive data nodes
secure_reader = add_access_control(
    CSVReaderNode(file_path="customers.csv"),
    enable_access_control=True,
    required_permission=NodePermission.READ_OUTPUT,
    mask_output_fields=["ssn", "phone"]  # Mask for non-admin users
)

workflow.add_node("secure_data", secure_reader)
```

#### Permission-Based Routing
```python
# Different execution paths based on user permissions
from kailash.access_control import NodePermission

# Admin users get full processing
admin_processor = PythonCodeNode.from_function(
    lambda data: {"result": process_all_data(data)},
    name="admin_processor"
)

# Analyst users get limited processing
analyst_processor = PythonCodeNode.from_function(
    lambda data: {"result": process_limited_data(data)},
    name="analyst_processor"
)

# Runtime automatically routes based on user permissions
workflow.add_node("admin_path", admin_processor)
workflow.add_node("analyst_path", analyst_processor)
```

**Security Features:**
- 🔐 **JWT Authentication**: Token-based authentication with refresh support
- 👥 **Multi-Tenant Isolation**: Complete data separation between tenants
- 🛡️ **Field-Level Security**: Mask sensitive data based on user roles
- 📊 **Audit Logging**: Complete access attempt logging for compliance
- 🚫 **Path Traversal Prevention**: Built-in protection against directory attacks
- 🏗️ **Backward Compatibility**: Existing workflows work unchanged
- ⚡ **Performance Optimized**: Minimal overhead with caching

## 💻 CLI Commands

The SDK includes a comprehensive CLI for workflow management:

```bash
# Project initialization
kailash init my-project --template data-pipeline

# Workflow operations
kailash validate workflow.yaml
kailash run workflow.yaml --inputs data.json
kailash export workflow.py --format kubernetes

# Task management
kailash tasks list --status running
kailash tasks show run-123
kailash tasks cancel run-123

# Development tools
kailash test workflow.yaml --data test_data.json
kailash debug workflow.yaml --breakpoint node-id
```

## 🏗️ Architecture

The SDK follows a clean, modular architecture:

```
kailash/
├── nodes/           # Node implementations and base classes
│   ├── base.py      # Abstract Node class
│   ├── data/        # Data I/O nodes
│   ├── transform/   # Transformation nodes
│   ├── logic/       # Business logic nodes
│   └── ai/          # AI/ML nodes
├── workflow/        # Workflow management
│   ├── graph.py     # DAG representation
│   └── visualization.py  # Visualization tools
├── visualization/   # Performance visualization
│   └── performance.py    # Performance metrics charts
├── runtime/         # Execution engines
│   ├── local.py     # Local execution
│   └── docker.py    # Docker execution (planned)
├── tracking/        # Monitoring and tracking
│   ├── manager.py   # Task management
│   └── metrics_collector.py  # Performance metrics
│   └── storage/     # Storage backends
├── cli/             # Command-line interface
└── utils/           # Utilities and helpers
```

### 🤖 Unified AI Provider Architecture

The SDK features a unified provider architecture for AI capabilities:

```python
from kailash.nodes.ai import LLMAgentNode, EmbeddingGeneratorNode

# Multi-provider LLM support
agent = LLMAgentNode()
result = agent.run(
    provider="ollama",  # or "openai", "anthropic", "mock"
    model="llama3.1:8b-instruct-q8_0",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    generation_config={"temperature": 0.7, "max_tokens": 500}
)

# Vector embeddings with the same providers
embedder = EmbeddingGeneratorNode()
embedding = embedder.run(
    provider="ollama",  # Same providers support embeddings
    model="snowflake-arctic-embed2",
    operation="embed_text",
    input_text="Quantum computing uses quantum mechanics principles"
)

# Check available providers and capabilities
from kailash.nodes.ai.ai_providers import get_available_providers
providers = get_available_providers()
# Returns: {"ollama": {"available": True, "chat": True, "embeddings": True}, ...}
```

**Supported AI Providers:**
- **Ollama**: Local LLMs with both chat and embeddings (llama3.1, mistral, etc.)
- **OpenAI**: GPT models and text-embedding-3 series
- **Anthropic**: Claude models (chat only)
- **Cohere**: Embedding models (embed-english-v3.0)
- **HuggingFace**: Sentence transformers and local models
- **Mock**: Testing provider with consistent outputs

## 🧪 Testing

The SDK is thoroughly tested with comprehensive test suites:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=kailash --cov-report=html

# Run specific test categories
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/integrum/kailash-python-sdk.git
cd kailash-python-sdk

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates venv automatically and installs everything)
uv sync

# Run commands using uv (no need to activate venv)
uv run pytest
uv run kailash --help

# Or activate the venv if you prefer
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv add --dev pre-commit detect-secrets doc8

# Install Trivy (macOS with Homebrew)
brew install trivy

# Set up pre-commit hooks
pre-commit install
pre-commit install --hook-type pre-push

# Run initial setup (formats code and fixes issues)
pre-commit run --all-files
```

### Code Quality & Pre-commit Hooks

We use automated pre-commit hooks to ensure code quality:

**Hooks Include:**
- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linting
- **pytest**: Unit tests
- **Trivy**: Security vulnerability scanning
- **detect-secrets**: Secret detection
- **doc8**: Documentation linting
- **mypy**: Type checking

**Manual Quality Checks:**
```bash
# Format code
black src/ tests/
isort src/ tests/

# Linting and fixes
ruff check src/ tests/ --fix

# Type checking
mypy src/

# Run all pre-commit hooks manually
pre-commit run --all-files

# Run specific hooks
pre-commit run black
pre-commit run pytest-check
```

## 📈 Project Status

<table>
<tr>
<td width="40%">

### ✅ Completed
- Core node system with 66+ node types
- Workflow builder with DAG validation
- Local & async execution engines
- Task tracking with metrics
- Multiple storage backends
- Export functionality (YAML/JSON)
- CLI interface
- Immutable state management
- API integration with rate limiting
- OAuth 2.0 authentication
- Production security framework
- Path traversal prevention
- Code execution sandboxing
- Comprehensive security testing
- SharePoint Graph API integration
- **Self-organizing agent pools with 13 specialized nodes**
- **Agent-to-agent communication and shared memory**
- **Intelligent caching and convergence detection**
- **MCP integration for external tool access**
- **Multi-strategy team formation algorithms**
- **Real-time performance metrics collection**
- **Performance visualization dashboards**
- **Real-time monitoring dashboard with WebSocket streaming**
- **Comprehensive performance reports (HTML, Markdown, JSON)**
- **100% test coverage (591 tests)**
- **All test categories passing**
- 68 working examples

</td>
<td width="30%">

### 🚧 In Progress
- **Kailash Workflow Studio** - Visual workflow builder UI
  - React-based drag-and-drop interface
  - Multi-tenant architecture with Docker
  - WorkflowStudioAPI backend
  - Real-time execution monitoring
- Performance optimizations
- Docker runtime finalization

</td>
<td width="30%">

### 📋 Planned
- Cloud deployment templates
- Visual workflow editor
- Plugin system
- Additional integrations

</td>
</tr>
</table>

### 🎯 Test Suite Status
- **Total Tests**: 591 passing (100%)
- **Test Categories**: All passing
- **Integration Tests**: All passing
- **Security Tests**: 10 consolidated comprehensive tests
- **Examples**: 68/68 working
- **Code Coverage**: 100%

## ⚠️ Known Issues

1. **DateTime Comparison in `list_runs()`**: The `TaskManager.list_runs()` method may encounter timezone comparison errors between timezone-aware and timezone-naive datetime objects. Workaround: Use try-catch blocks when calling `list_runs()` or access run details directly via `get_run(run_id)`.

2. **Performance Tracking**: To enable performance metrics collection, you must pass the `task_manager` parameter to the `runtime.execute()` method: `runtime.execute(workflow, task_manager=task_manager)`.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The Integrum team for the Kailash architecture
- All contributors who have helped shape this SDK
- The Python community for excellent tools and libraries

## 📞 Support

- 📋 [GitHub Issues](https://github.com/integrum/kailash-python-sdk/issues)
- 📧 Email: support@integrum.com
- 💬 Slack: [Join our community](https://integrum.slack.com/kailash-sdk)

---

<p align="center">
  Made with ❤️ by the Integrum Team
</p>
