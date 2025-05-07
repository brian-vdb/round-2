# models/information.py

import logging
import time
from typing import Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage, FunctionMessage, ToolMessage
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnableConfig
from langchain_core.tools.structured import StructuredTool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt.tool_node import ToolNode

from data.search.faq import search_faqs

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# direct system prompt
def _create_system_message() -> SystemMessage:
  return SystemMessage(
    content=(
      "Before responding, call 'faq_search' or 'switch_to_action_agent' tool as needed. "
      "Use exactly those results to give a concise, factual answer. "
      "When you call 'switch_to_action_agent', ALWAYS explicitly notify the user by including a message in the response. "
      "Make it sound natural and as if you're getting the help of another agent and the reason why. "
      "Also make the tool call when you intend to switch in, since it allows the backend to switch in the model. "
      "When you call 'faq_search' for the purpose of providing information, always mention your finding even when you intend to switch to another agent. "
      "The output is in the form of a chat message and you shouldn't use any line breaks. Act as if it's whatsapp and you're giving a quick response."
    )
  )

# OpenAI model
COMPLETION_MODEL = "gpt-4o-mini"

# FAQ search tool
def _faq_search_tool(query: str, k: int = 5) -> list[dict[str, Any]]:
  """Search the FAQ database for relevant entries based on a query and return up to k results."""
  logger.info("Tool call: faq_search(query=%s, k=%d)", query, k)

  items = search_faqs(query=query, k=k)
  results = [item.model_dump() for item in items]
  return results

# Switch to action agent tool
next_agent: dict[str, str] = {}
def _switch_to_action_agent(config: RunnableConfig) -> None:
  """Switch the current agent to the action_agent. Should be called when the user requests help with their account."""
  logger.info("Tool call: switch_to_action_agent()")

  global next_agent
  next_agent[config['metadata']['next_agent_id']] = "action_agent"

# wrap tools
faq_tool = StructuredTool.from_function(
  _faq_search_tool,
  description="Search the FAQ database for relevant entries based on a query and return up to k results."
)

switch_tool = StructuredTool.from_function(
  _switch_to_action_agent,
  description="Switch the current agent to the action_agent. Should be called when the user requests help with their account."
)

# tool node and binding
_tools = [faq_tool, switch_tool]
information_model_tools = ToolNode(_tools)

# LLM node
def information_model(state: dict[str, Any], config: RunnableConfig) -> dict[str, Any]:
  messages = state.get("messages", [])
  system_msg = _create_system_message()
  llm = ChatOpenAI(model=COMPLETION_MODEL, temperature=0).bind_tools(_tools)

  # Convert ToolMessage to FunctionMessage
  prepared: list[Any] = []
  for msg in messages:
    if isinstance(msg, ToolMessage):
      prepared.append(FunctionMessage(name=msg.name, content=msg.content))
    else:
      prepared.append(msg)

  # Generate a response
  response = llm.invoke([system_msg] + prepared)
  return {"messages": [response], "response": response.content}

# flow control
def information_model_should_continue(state: dict[str, Any]) -> str:
  last = state.get("messages", [])[-1]
  if getattr(last, "tool_calls", None):
    return "information_model_tools"
  return END

# orchestrator
class InformationAssistant:
  def __init__(self) -> None:
    self.workflow = StateGraph(input=dict[str, Any], output=dict[str, Any])
    self.workflow.add_node("information_model", information_model)
    self.workflow.add_node("information_model_tools", information_model_tools)

    self.workflow.add_edge(START, "information_model")
    self.workflow.add_conditional_edges("information_model", information_model_should_continue)
    self.workflow.add_edge("information_model_tools", "information_model")

    checkpointer = MemorySaver()
    self.app = self.workflow.compile(checkpointer=checkpointer)

  def invoke(self, messages: list[HumanMessage], user_prompt: Optional[str] = None) -> dict[str, Any]:
    global next_agent

    # Set up the next agent state
    next_agent_id = round(time.time())
    while next_agent.get(next_agent_id, None) != None:
      next_agent_id += 1
    next_agent_id = str(next_agent_id)
    next_agent[next_agent_id] = "information_agent"

    # Prepare the conversation up to now
    convo = list(messages)
    if user_prompt:
      convo.append(HumanMessage(content=user_prompt))

    # Invoke the chatbot
    init_state = {"messages": convo, "response": ""}
    final_state = self.app.invoke(
      init_state,
      config=RunnableConfig(
        configurable={"thread_id": "main", "checkpoint_ns": "info", "checkpoint_id": "0", "next_agent_id": next_agent_id},
        metadata={}
      )
    )

    # Return the state and next agent to call
    return {
      "messages": final_state["messages"],
      "response": final_state["response"],
      "next_agent": next_agent.pop(next_agent_id)
    }
