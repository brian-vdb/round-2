import logging
from typing import Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage, FunctionMessage, ToolMessage
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnableConfig
from langchain_core.tools.structured import StructuredTool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt.tool_node import ToolNode

import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# System prompt for the Action Agent
def _create_system_message() -> SystemMessage:
  return SystemMessage(
    content=(
      "You are the Action Agent for Level-1 customer support. "
      "Respond by invoking the appropriate tools for user-facing support tasks. "
      "Use the available tools to help the user with customer support. "
      "If the user needs general informational help, call 'switch_to_information_agent', ALWAYS explicitly notify the user by including a message in the response. "
      "Make it sound natural and as if you're getting the help of another agent and the reason why. "
      "Also make the tool call when you intend to switch in, since it allows the backend to switch in the model. "
    )
  )

# Placeholder tool implementations
def _reset_user_password(user_id: str) -> dict[str, Any]:
  logger.info("Tool call: reset_user_password(user_id=%s)", user_id)
  return {"status": "success", "user_id": user_id}

def _create_support_ticket(user_id: str, issue: str) -> dict[str, Any]:
  logger.info("Tool call: create_support_ticket(user_id=%s, issue=%s)", user_id, issue)
  return {"ticket_id": "TBD", "status": "created"}

def _check_order_status(order_id: str) -> dict[str, Any]:
  logger.info("Tool call: check_order_status(order_id=%s)", order_id)
  return {"order_id": order_id, "status": "pending"}

def _update_user_profile(user_id: str, profile_updates: dict[str, Any]) -> dict[str, Any]:
  logger.info("Tool call: update_user_profile(user_id=%s, updates=%s)", user_id, profile_updates)
  return {"status": "success", "updated_fields": list(profile_updates.keys())}

def _send_followup_email(user_id: str, email_body: str) -> dict[str, Any]:
  logger.info("Tool call: send_followup_email(user_id=%s)", user_id)
  return {"status": "sent", "user_id": user_id}

# Switch to information agent tool
next_agent: dict[str, str] = {}
def _switch_to_information_agent(config: RunnableConfig) -> None:
  logger.info("Tool call: switch_to_information_agent()")

  global next_agent
  next_agent[config['metadata']['next_agent_id']] = "action_agent"

# Wrap tools as StructuredTool
reset_password_tool = StructuredTool.from_function(_reset_user_password, description="Reset a customer's password given their user ID.")
create_ticket_tool = StructuredTool.from_function(_create_support_ticket, description="Create a new support ticket for a user issue.")
check_order_tool = StructuredTool.from_function(_check_order_status, description="Lookup an order status by order ID.")
update_profile_tool = StructuredTool.from_function(_update_user_profile, description="Update fields on a user's profile.")
send_email_tool = StructuredTool.from_function(_send_followup_email, description="Send a follow-up email to a user.")
switch_info_tool = StructuredTool.from_function(_switch_to_information_agent, description="Switch the conversation back to the information agent. Should be called when the user requests information.")

# Tool node binding
_tools = [
  reset_password_tool,
  create_ticket_tool,
  check_order_tool,
  update_profile_tool,
  send_email_tool,
  switch_info_tool,
]
action_model_tools = ToolNode(_tools)

# LLM node
COMPLETION_MODEL = "gpt-4o-mini"

def action_model(state: dict[str, Any], config: RunnableConfig) -> dict[str, Any]:
  messages = state.get("messages", [])
  system_msg = _create_system_message()
  llm = ChatOpenAI(model=COMPLETION_MODEL, temperature=0).bind_tools(_tools)

  prepared: list[Any] = []
  for msg in messages:
    if isinstance(msg, ToolMessage):
      prepared.append(FunctionMessage(name=msg.name, content=msg.content))
    else:
      prepared.append(msg)

  response = llm.invoke([system_msg] + prepared)
  return {"messages": [response], "response": response.content}

# flow control
def action_model_should_continue(state: dict[str, Any]) -> str:
  last = state.get("messages", [])[-1]
  if getattr(last, "tool_calls", None):
    return "action_model_tools"
  return END

# Orchestrator
class ActionAssistant:
  def __init__(self) -> None:
    self.workflow = StateGraph(input=dict[str, Any], output=dict[str, Any])
    self.workflow.add_node("action_model", action_model)
    self.workflow.add_node("action_model_tools", action_model_tools)

    self.workflow.add_edge(START, "action_model")
    self.workflow.add_conditional_edges("action_model", action_model_should_continue)
    self.workflow.add_edge("action_model_tools", "action_model")

    checkpointer = MemorySaver()
    self.app = self.workflow.compile(checkpointer=checkpointer)

  def invoke(self, messages: list[HumanMessage], user_prompt: Optional[str] = None) -> dict[str, Any]:
    global next_agent

    # Set up the next agent state
    next_agent_id = round(time.time())
    while next_agent.get(next_agent_id, None) != None:
      next_agent_id += 1
    next_agent_id = str(next_agent_id)
    next_agent[next_agent_id] = "action_agent"

    # Prepare the conversation up to now
    convo = list(messages)
    if user_prompt:
      convo.append(HumanMessage(content=user_prompt))

    # Invoke the chatbot
    init_state = {"messages": convo, "response": ""}
    final_state = self.app.invoke(
      init_state,
      config=RunnableConfig(
        configurable={"thread_id": "main", "checkpoint_ns": "action", "checkpoint_id": "0", "next_agent_id": next_agent_id},
        metadata={}
      )
    )

    # Return the state and next agent to call
    return {
      "messages": final_state["messages"],
      "response": final_state["response"],
      "next_agent": next_agent.pop(next_agent_id)
    }
