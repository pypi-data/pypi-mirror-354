# Databricks notebook source
# MAGIC %pip install --quiet uv
# MAGIC
# MAGIC import os
# MAGIC os.environ["UV_PROJECT_ENVIRONMENT"] = os.environ["VIRTUAL_ENV"]

# COMMAND ----------

# MAGIC %sh uv --project ../ sync

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

dbutils.widgets.text(name="config-path", defaultValue="../config/model_config.yaml")
config_path: str = dbutils.widgets.get("config-path")
print(config_path)

# COMMAND ----------

import sys
from typing import Sequence
from importlib.metadata import version
from pkg_resources import get_distribution

sys.path.insert(0, "..")

pip_requirements: Sequence[str] = [
    f"databricks-agents=={version('databricks-agents')}",
    f"databricks-connect=={get_distribution('databricks-connect').version}",
    f"databricks-langchain=={version('databricks-langchain')}",
    f"databricks-sdk=={version('databricks-sdk')}",
    f"duckduckgo-search=={version('duckduckgo-search')}",
    f"langchain=={version('langchain')}",
    f"langchain-mcp-adapters=={version('langchain-mcp-adapters')}",
    f"langgraph=={version('langgraph')}",
    f"langgraph-checkpoint-postgres=={version('langgraph-checkpoint-postgres')}",
    f"langgraph-reflection=={version('langgraph-reflection')}",
    f"langgraph-supervisor=={version('langgraph-supervisor')}",
    f"langgraph-swarm=={version('langgraph-swarm')}",
    f"langmem=={version('langmem')}",
    f"loguru=={version('loguru')}",
    f"mlflow=={version('mlflow')}",
    f"openevals=={version('openevals')}",
    f"psycopg[binary,pool]=={version('psycopg')}",
    f"pydantic=={version('pydantic')}",
    f"unitycatalog-ai[databricks]=={version('unitycatalog-ai')}",
    f"unitycatalog-langchain[databricks]=={version('unitycatalog-langchain')}",
]
print("\n".join(pip_requirements))

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

from mlflow.models import ModelConfig
from retail_ai.config import AppConfig

model_config_path: str = config_path
model_config: ModelConfig = ModelConfig(development_config=model_config_path)
config: AppConfig = AppConfig(**model_config.to_dict())

# COMMAND ----------

from langgraph.graph.state import CompiledStateGraph
from retail_ai.models import display_graph
from retail_ai.graph import create_retail_ai_graph

graph: CompiledStateGraph = create_retail_ai_graph(config=config)

display_graph(graph)

# COMMAND ----------

from pathlib import Path
from retail_ai.agent_as_code import app
from retail_ai.models import save_image

path: Path = Path.cwd().parent / Path("docs") / "architecture.png"
save_image(app, path)

# COMMAND ----------

config.create_agent()


# COMMAND ----------

config.deploy_agent()