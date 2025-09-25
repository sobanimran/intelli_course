import { useState } from "react";
import axios from "axios";
import { MessageSquare, Settings, Plus } from "lucide-react";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "👋 Hi! Ask me anything about your courses." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Function to send query
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        query: input,
      });

      const botMessage = {
        sender: "bot",
        text: res.data.answer || "⚠️ No answer received.",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Error contacting server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Detect Enter key press
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Render AI text with formatting
  const renderBotText = (text) => {
    return text.split("\n").map((line, i) =>
      line.startsWith("-") ? (
        <li key={i} className="ml-6 list-disc">
          {line.slice(1).trim()}
        </li>
      ) : (
        <p key={i} className="mb-2">
          {line}
        </p>
      )
    );
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 p-4 border-r border-green-700 hidden md:flex flex-col">
        <h2 className="text-2xl font-extrabold text-green-500 mb-6">
          IntelliCourse
        </h2>

        <ul className="space-y-3 flex-1">
          <li className="flex items-center gap-2 p-2 rounded-lg cursor-pointer hover:bg-green-700/30 hover:text-green-400 transition">
            <Plus size={18} /> New Chat
          </li>
          <li className="flex items-center gap-2 p-2 rounded-lg cursor-pointer hover:bg-green-700/30 hover:text-green-400 transition">
            <MessageSquare size={18} /> Saved Notes
          </li>
          <li className="flex items-center gap-2 p-2 rounded-lg cursor-pointer hover:bg-green-700/30 hover:text-green-400 transition">
            <Settings size={18} /> Settings
          </li>
        </ul>

        <p className="text-xs text-gray-500 mt-auto">⚡ Powered by AI</p>
      </div>

      {/* Chat area */}
      <div className="flex flex-col flex-1">
        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-lg p-3 rounded-2xl shadow-md ${
                  msg.sender === "user"
                    ? "bg-green-600 text-white rounded-br-none"
                    : "bg-gray-800 text-gray-100 rounded-bl-none"
                }`}
              >
                {msg.sender === "bot" ? renderBotText(msg.text) : msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 p-3 rounded-2xl rounded-bl-none text-green-300 animate-pulse">
                🤖 Thinking...
              </div>
            </div>
          )}
        </div>

        {/* Input box */}
        <div className="p-4 border-t border-green-700 flex gap-2 bg-gray-900">
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your question..."
            className="flex-1 p-3 rounded-xl bg-gray-800 border border-green-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-green-600 hover:bg-green-500 px-5 py-2 rounded-xl font-medium disabled:opacity-50 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
