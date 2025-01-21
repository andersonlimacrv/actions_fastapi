from fastapi import WebSocket, HTTPException, status
import json
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        logger.info("WebSocketManager initialized with no active connections.")

    async def connect(self, websocket: WebSocket, endpoint: str):
        """
        Accepts a WebSocket connection and registers it under the specified endpoint.
        """
        await websocket.accept()
        if endpoint not in self.active_connections:
            self.active_connections[endpoint] = []
            logger.info(f"Created a new endpoint group: '{endpoint}'.")

        self.active_connections[endpoint].append(websocket)
        logger.info(
            f"New WebSocket connection added to '{endpoint}'. Total connections: {len(self.active_connections[endpoint])}."
        )

    def disconnect(self, websocket: WebSocket, endpoint: str):
        """
        Removes a WebSocket connection from the specified endpoint.
        """
        if endpoint in self.active_connections:
            self.active_connections[endpoint].remove(websocket)
            logger.info(
                f"WebSocket connection removed from '{endpoint}'. Remaining connections: {len(self.active_connections[endpoint])}."
            )

            if not self.active_connections[endpoint]:
                del self.active_connections[endpoint]
                logger.info(f"No more connections under '{endpoint}'. Endpoint group deleted.")

    async def broadcast(self, endpoint: str, message: str):
        """
        Sends a message to all active WebSocket connections for the specified endpoint.
        """
        if endpoint in self.active_connections:
            connections = self.active_connections[endpoint]
            logger.info(f"Broadcasting message to {len(connections)} connection(s) under '{endpoint}'.")
            for connection in connections:
                try:
                    await connection.send_text(message)
                    logger.info(f"Message sent to WebSocket under '{endpoint}'.")
                except Exception as e:
                    logger.error(f"Failed to send message to a WebSocket under '{endpoint}'. Error: {e}")
        else:
            logger.warning(f"No active connections under '{endpoint}' to broadcast the message.")

    async def get_token_from_first_message(self, websocket: WebSocket):
        """
        Receives the first message from the WebSocket connection, validates it,
        and returns the token if valid.
        """
        first_message = await websocket.receive_text()

        if not first_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mensagem vazia recebida"
            )

        logger.info(f"Mensagem recebida: {first_message}")

        try:
            token_data = json.loads(first_message)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao analisar JSON: {str(e)}"
            )
        
        token = token_data.get("token")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token não fornecido"
            )

        return token
