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
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 1. Check for token on load
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) setToken(savedToken);
  }, []);

  // 2. Fetch Expenses Function
  const fetchExpenses = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/expenses`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Session expired. Please log in again.");
      const data = await response.json();
      setExpenses(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 3. Fetch on load
  useEffect(() => {
    fetchExpenses();
  }, [token]);

  // 4. Handle Login
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
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });
      if (!response.ok) throw new Error("Invalid username or password");
      
      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 5. Handle Add Expense
  const handleAddExpense = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description || !amount) return;

    try {
      const response = await fetch(`${API_URL}/expenses`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          description: description,
          amount: parseFloat(amount), // React inputs return strings, convert to float
        }),
      });

      if (!response.ok) throw new Error("Failed to add expense");

      // Clear form
      setDescription("");
      setAmount("");
      
      // Re-fetch to get the AI-generated category!
      fetchExpenses();
    } catch (err: any) {
      setError(err.message);
    }
  };

  // 6. Handle Delete Expense
  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`${API_URL}/expenses/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Failed to delete expense");
      
      // Filter the deleted item out of the local state instantly
      setExpenses(expenses.filter((exp) => exp.id !== id));
    } catch (err: any) {
      setError(err.message);
    }
  };

  // 7. Handle Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setExpenses([]);
  };

  // --- RENDER: LOGIN ---
  if (!token) {
    return (
      <main className="p-8 max-w-md mx-auto mt-20">
        <h1 className="text-3xl font-bold mb-6 text-center text-black">Login</h1>
        {error && <p className="text-red-500 mb-4 text-center">{error}</p>}
        <form onSubmit={handleLogin} className="space-y-4 bg-white p-6 rounded-lg shadow-md border text-black">
          <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full border p-2 rounded" required />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full border p-2 rounded" required />
          <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </main>
    );
  }

  // --- RENDER: DASHBOARD ---
  return (
    <main className="p-8 max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-black">My Expenses</h1>
        <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm">Logout</button>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {/* ADD EXPENSE FORM */}
      <form onSubmit={handleAddExpense} className="bg-white p-4 rounded-lg shadow-md border mb-6 flex gap-4 text-black">
        <input 
          type="text" 
          placeholder="Description (e.g. Uber)" 
          value={description} 
          onChange={(e) => setDescription(e.target.value)} 
          className="flex-1 border p-2 rounded" 
          required 
        />
        <input 
          type="number" 
          placeholder="Amount (₹)" 
          value={amount} 
          onChange={(e) => setAmount(e.target.value)} 
          className="w-32 border p-2 rounded" 
          required 
        />
        <button type="submit" className="bg-green-600 text-white px-6 rounded hover:bg-green-700 font-bold">
          Add
        </button>
      </form>

      {/* EXPENSE LIST */}
      {loading ? (
        <p className="text-gray-500">Loading expenses...</p>
      ) : expenses.length === 0 ? (
        <p className="text-gray-500">No expenses found. Add one above!</p>
      ) : (
        <ul className="space-y-4">
          {expenses.map((expense) => (
            <li key={expense.id} className="bg-white text-black border p-4 rounded shadow-sm flex justify-between items-center">
              <div>
                <span className="font-bold">{expense.description}</span>
                <span className="text-xs bg-gray-200 px-2 py-1 rounded ml-2">{expense.category}</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="font-bold">₹{expense.amount}</span>
                <button onClick={() => handleDelete(expense.id)} className="text-red-500 hover:text-red-700 font-bold">
                  ✕
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}