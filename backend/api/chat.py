from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Optional

from api.auth import User, get_current_user

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
    token = websocket.query_params.get("token")
    if token:
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
        while True:
            # Receive user message
            message = await websocket.receive_text()
            
            # Send the message back
            await websocket.send_text(message)

    except WebSocketDisconnect:
        # Handle client disconnection
        print(f"{username} disconnected from chat")

    except Exception as e:
        # Unexpected error: notify client and close connection
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
