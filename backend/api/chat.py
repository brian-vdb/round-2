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
    messages = []
    next_respondent = 'information_agent'

    while True:
      # Receive user message
      user_msg = await websocket.receive_text()
      responded = []

      while True:
        # Handle the chatbot
        last_respondent = next_respondent
        if next_respondent == 'information_agent':
          messages, agent_msg, next_respondent = info_agent.invoke(
            messages=messages, responded=', '.join(responded), user_prompt=user_msg
          )        
        else:
          messages, agent_msg, next_respondent = action_agent.invoke(
            messages=messages, responded=', '.join(responded), user_prompt=user_msg
          )
        responded.append(last_respondent)

        # Handle the result
        if next_respondent == last_respondent:
          await websocket.send_json({
            "identity": last_respondent,
            "message": agent_msg
          })
          break
        elif next_respondent in responded:
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
