import type React from "react";

const Chat: React.FC = () => {
  return (
    <div className="chat">
      <div className="header">
        <h2 className="title">Customer Support</h2>
        <div className="status-icon"></div>
      </div>
      <div className="content">
        Content box
      </div>
    </div>
  );
}

export default Chat;
