import React, { useState } from "react";

export default function SendBotMessageButton({ onSent }) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleSend = async () => {
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      const res = await fetch("/api/send-bot-message/", {
        method: "POST",
        credentials: "include"
      });
      if (res.ok) {
        setSuccess("Bot message sent to all employees!");
        onSent && onSent();
      } else {
        setError("Failed to send message.");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="my-4 flex flex-col items-center">
      <button
        onClick={handleSend}
        disabled={loading}
        className="bg-[#90acc6] hover:bg-[#6d8db0] text-white font-semibold py-2 px-6 rounded-md shadow transition-colors duration-150"
      >
        {loading ? "Sending..." : "Send Test Bot Message"}
      </button>
      {success && <div className="text-green-600 text-sm font-medium mt-2">{success}</div>}
      {error && <div className="text-red-600 text-sm font-medium mt-2">{error}</div>}
    </div>
  );
}
