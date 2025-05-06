// components/Chat.tsx

import React, { useState } from "react";
import './Chat.css'

const Chat: React.FC = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className={`chat ${open ? 'open' : 'closed'}`}>
      <div className="header" onClick={() => setOpen(o => !o)}>
        <h2 className="title">Customer Support</h2>
        <div className="status-icon" />
      </div>
      <div className="content">
        {/* your chat messages or form go here */}
        Content box
      </div>
    </div>
  );
}

export default Chat;
