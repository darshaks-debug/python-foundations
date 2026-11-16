"use client"; // This tells Next.js this is an interactive component

import { useState } from "react";

// 1. Define our data types (TypeScript)
type Expense = {
  id: number;
  description: string;
  amount: number;
};

export default function Home() {
  // 2. State: This is how React remembers things.
  const [expenses, setExpenses] = useState<Expense[]>([
    { id: 1, description: "Uber to airport", amount: 600 },
    { id: 2, description: "Starbucks Coffee", amount: 250 },
    { id: 3, description: "Dinner with friends", amount: 1200 },
  ]);

  // 3. A helper function to calculate the total
  const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);

  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-3xl font-bold mb-6">My Expenses (React)</h1>
      
      <div className="bg-gray-100 text-gray-100 p-4 rounded-lg mb-6">
        <p className="text-lg font-semibold">Total Spend: ₹{total}</p>
      </div>

      <ul className="space-y-4">
        {expenses.map((expense) => (
          <li key={expense.id} className="border p-4 rounded shadow-sm flex justify-between">
            <span>{expense.description}</span>
            <span className="font-bold">₹{expense.amount}</span>
          </li>
        ))}
      </ul>
    </main>
  );
}