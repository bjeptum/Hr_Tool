import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    const csrftoken = getCookie('csrftoken');
    try {
      const response = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username,
          password: password
        }),
        credentials: "include"
      });
      const result = await response.json();
      console.log('Login API response:', result);
      if (result.success) {
        navigate("/dashboard");
      } else {
        setError(result.message || "Invalid credentials. Please try again.");
      }
    } catch (err) {
      setError("Login failed. Please check your connection.");
    }
  };

  return (
    <div className="login-bg min-h-screen w-full flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-lg animate-float">
        <div className="text-center mb-6">
          <img
            src="/logo.png"
            alt="PulseTracker Logo"
            className="w-24 mx-auto rounded-xl animate-logo-pulse"
          />
        </div>
        <form className="space-y-4" onSubmit={handleLogin}>
          {error && <div className="text-red-500 text-center mb-2">{error}</div>}
          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Username</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-md"
              placeholder="Enter your username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 border border-gray-300 rounded-md"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-[#90acc6] text-white py-2 rounded-md hover:bg-[#a3bcd9]"
          >
            Log In
          </button>
        </form>
        <p className="mt-4 text-center text-xs text-[#90acc6]">
          Don’t have access? <a href="#" className="hover:underline">Contact your admin</a>
        </p>
      </div>
    </div>
  );
}

