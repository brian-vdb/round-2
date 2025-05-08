# api/chat.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Optional

from api.auth import User, get_current_user
from models.action import ActionAssistant
from models.information import InformationAssistant

router = APIRouter()

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
  """
  WebSocket endpoint for real-time chat with the AI agent.
  """
  # Accept the WebSocket connection
  await websocket.accept()

  # Attempt optional authentication
  user: Optional[User] = None
  raw_token = websocket.query_params.get("token")
  if raw_token:
    # Expect format "<AuthType> <Token>"
    parts = raw_token.split(" ", 1)
    token = parts[1] if len(parts) == 2 else parts[0]
    try:
      user = get_current_user(token)
    except HTTPException:
      # Invalid token, proceed as anonymous
      user = None

  # Log connection
  username = user.username if user else "anonymous"
  print(f"{username} connected to chat")

  # Main chat loop
  try:
    # Set up the two agents
    info_agent = InformationAssistant()
    action_agent = ActionAssistant()
    messages: list = []
    next_agent = 'information_agent'

    while True:
      # Receive user message
      prompt = await websocket.receive_text()
      agents_invoked: list[str] = []

      while True:
        # Invoke the agent
        current_agent = next_agent
        agent = info_agent if current_agent == 'information_agent' else action_agent
        result = agent.invoke(
          messages=messages,
          agents_invoked=agents_invoked,
          user_prompt=prompt
        )
        agents_invoked.append(current_agent)

        # Parse the result
        messages = result['messages']
        response = result['response']
        next_agent = result['next_agent']

        # Handle the result
        if current_agent == next_agent:
          await websocket.send_json({
            "identity": current_agent,
            "message": response
          })
          break
        elif next_agent in agents_invoked:
          break
        else:
          messages.pop()

  except WebSocketDisconnect:
    # Handle client disconnection
    print(f"{username} disconnected from chat")

  except Exception as e:
    # Unexpected error: notify client and close connection
    await websocket.send_text(f"Error: {str(e)}")
    await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
