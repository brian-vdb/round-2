import logging
from typing import Any, Optional

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, FunctionMessage, ToolMessage
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
def _create_system_message(additional_rules: str = '') -> SystemMessage:
  return SystemMessage(
    content=(
      "You are the Action Agent for Level-1 customer support for the website ran by Pace, which is the innovation hub of TCS (action_agent). "
      "This includes operations regarding accounts, and if there is a possibility that's the goal, ask clarifying questions."
      
      "Use the available tools to help the user with customer support. "
      "Notify the user about which tools you've used and why. "
      "You should always prioritize helping in any way you can before switching with another agent. "

      "When a prompt is confusing, ask clarifying questions rather than immidiatly using tools. "
      "Investigate the messages history. "
      
      "If the user requests information about the organization or content, call the '_switch_to_information_agent' tool, and explicitly notify the user by including a message in the response. "
      "Make it sound natural and as if you're getting the help of another agent and the reason why. "
      "ALWAYS ask permission from the '_switch_to_information_agent' tool, before you notify the user. "
      
      "The output is in the form of a chat message and you shouldn't use any line breaks. Act as if it's whatsapp and you're giving a quick response. "
      "Never attempt to answer on behalf of the other agents, even if you're not allowed to switch right now. "
      
      "If you're not allowed to switch to another agent for help, just perform your part of the user's question and await a response from the human. "
      "Never say you 'found information', you are the assistent that knows everything you found in tools inherently. "
      f"{additional_rules}"
    )
  )

# Placeholder tool implementations
def _reset_user_password(username: str) -> dict[str, Any]:
  logger.info("Tool call: reset_user_password(username=%s)", username)
  return {"status": "success", "username": username}

def _create_support_ticket(username: str, issue: str) -> dict[str, Any]:
  logger.info("Tool call: create_support_ticket(username=%s, issue=%s)", username, issue)
  return {"ticket_id": "TBD", "status": "created"}

def _check_order_status(username: str, order_id: str) -> dict[str, Any]:
  logger.info("Tool call: check_order_status(username=%s, order_id=%s)", username, order_id)
  return {"order_id": order_id, "status": "pending"}

def _update_user_profile(username: str, profile_updates: dict[str, Any]) -> dict[str, Any]:
  logger.info("Tool call: update_user_profile(username=%s, updates=%s)", username, profile_updates)
  return {"status": "success", "updated_fields": list(profile_updates.keys())}

def _send_followup_email(username: str, email_body: str) -> dict[str, Any]:
  logger.info("Tool call: send_followup_email(username=%s)", username)
  return {"status": "sent", "username": username}

# Switch to information agent tool
next_agent: dict[str, str] = {}
def _switch_to_information_agent(config: RunnableConfig) -> None:
  logger.info("Tool call: switch_to_information_agent()")

  global next_agent
  next_agent[config['metadata']['next_agent_id']] = "information_agent"

  return {"message": "Notify the user that you've succesfully switched to the information agent.", "status": "Success"}

# Wrap tools as StructuredTool
reset_password_tool = StructuredTool.from_function(_reset_user_password, description="Reset a customer's password given their username. This sends an email to the user with a link they can follow to change their password.")
create_ticket_tool = StructuredTool.from_function(_create_support_ticket, description="Create a new support ticket for a user issue.")
check_order_tool = StructuredTool.from_function(_check_order_status, description="Lookup an order status by order ID.")
update_profile_tool = StructuredTool.from_function(_update_user_profile, description="Update fields on a user's profile.")
send_email_tool = StructuredTool.from_function(_send_followup_email, description="Send a follow-up email to a when something important was changed for them in the system.")
switch_info_tool = StructuredTool.from_function(
  _switch_to_information_agent, 
  description="""Switches you with the information_agent. Only call when the situation follows your system message rules."""
)

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
  # Fetch the state information
  messages = state.get("messages", [])
  agents_invoked = config['metadata']['agents_invoked']
  additional_rules = f"You are currently NOT allowed to switch to {agents_invoked} at the moment. They already tried to help the user. Ask for clarifying questions instead."
  system_msg = _create_system_message(additional_rules) if agents_invoked != '' else _create_system_message()

  # Prepare the message history
  prepared: list[Any] = []
  for msg in messages:
    if isinstance(msg, ToolMessage):
      prepared.append(FunctionMessage(name=msg.name, content=msg.content))
    else:
      prepared.append(msg)

  # Invoke the llm
  llm = ChatOpenAI(model=COMPLETION_MODEL, temperature=0).bind_tools(_tools)
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

  def invoke(
    self, 
    messages: list[BaseMessage], 
    agents_invoked: list[str],
    user_prompt: Optional[str] = None
  ) -> tuple[list[BaseMessage], str, str]:
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

    # Invoke the graph
    init_state = {"messages": convo, "response": ""}
    final_state = self.app.invoke(
      init_state,
      config=RunnableConfig(
        configurable={
          "thread_id": "main", 
          "checkpoint_ns": "action", 
          "checkpoint_id": "0", 
          "next_agent_id": next_agent_id,
          "agents_invoked": f"[{', '.join(agents_invoked)}]" if len(agents_invoked) > 0 else ''
        },
        metadata={}
      )
    )

    # Return the results
    return {
      "messages": final_state["messages"],
      "response": final_state["response"],
      "next_agent": next_agent.pop(next_agent_id)
    }
