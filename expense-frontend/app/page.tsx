"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Expense = {
  id: number;
  description: string;
  amount: number;
  category: string;
};

export default function Home() {
  // Auth State
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  // App State
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 1. On page load, check if we have a token saved
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  // 2. Fetch expenses whenever the token changes
  useEffect(() => {
    if (!token) return; // Don't fetch if not logged in

    const fetchExpenses = async () => {
      setLoading(true);
      setError("");
      try {
        const response = await fetch(`${API_URL}/expenses`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch expenses. Session may have expired.");
        }

        const data = await response.json();
        setExpenses(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, [token]);

  // 3. Handle Login (FastAPI requires form-data, not JSON)
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch(`${API_URL}/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Invalid username or password");
      }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 4. Handle Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setExpenses([]);
  };

  // --- RENDER: LOGIN SCREEN ---
  if (!token) {
    return (
      <main className="p-8 max-w-md mx-auto mt-20">
        <h1 className="text-3xl font-bold mb-6 text-center text-black">Login to Expense Tracker</h1>
        {error && <p className="text-red-500 mb-4 text-center">{error}</p>}
        
        <form onSubmit={handleLogin} className="space-y-4 bg-white p-6 rounded-lg shadow-md border text-black">
          <div>
            <label className="block text-sm font-medium mb-1">Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)}
              className="w-full border p-2 rounded" required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border p-2 rounded" required 
            />
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </main>
    );
  }

  // --- RENDER: MAIN APP (Logged In) ---
  return (
    <main className="p-8 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-black">My Expenses</h1>
        <button 
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm"
        >
          Logout
        </button>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}
      
      {loading ? (
        <p className="text-gray-500">Loading expenses from Railway...</p>
      ) : expenses.length === 0 ? (
        <p className="text-gray-500">No expenses found. Add some in the Streamlit app!</p>
      ) : (
        <ul className="space-y-4">
          {expenses.map((expense) => (
            <li key={expense.id} className="bg-white text-black border p-4 rounded shadow-sm flex justify-between items-center">
              <div>
                <span className="font-bold">{expense.description}</span>
                <span className="text-sm text-gray-500 ml-2">({expense.category})</span>
              </div>
              <span className="font-bold">₹{expense.amount}</span>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}