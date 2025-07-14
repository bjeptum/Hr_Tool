import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AddEmployee() {
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState({ name: "", phone_number: "", department_id: "" });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/api/employees/", {
      credentials: "include"
    })
      .then(res => res.json())
      .then(data => {
        if (data && Array.isArray(data.departments) && data.departments.length > 0) {
          setDepartments(data.departments);
        } else {
          setDepartments([
            { id: 1, name: "Sales" },
            { id: 2, name: "HR" },
            { id: 3, name: "Tech" },
            { id: 4, name: "Marketing" }
          ]);
        }
      })
      .catch(() => {
        setDepartments([
          { id: 1, name: "Sales" },
          { id: 2, name: "HR" },
          { id: 3, name: "Tech" },
          { id: 4, name: "Marketing" }
        ]);
      });
  }, []);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    if (!form.name || !form.phone_number || !form.department_id) {
      setError("All fields are required.");
      setLoading(false);
      return;
    }
    try {
      const res = await fetch("/api/employees/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          name: form.name,
          phone_number: form.phone_number,
          department_id: form.department_id
        })
      });
      if (res.ok) {
        setSuccess("Employee added successfully!");
        setForm({ name: "", phone_number: "", department_id: "" });
        setTimeout(() => navigate("/dashboard"), 1200);
      } else {
        const data = await res.json();
        setError(data?.phone_number?.[0] || "Failed to add employee.");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-[#e6f0fa] to-[#f6fbff] p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-[#2e3c53] mb-6 text-center">Add Employee</h2>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-[#2e3c53] font-medium mb-1">Name</label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              className="w-full border border-[#c8d6e6] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#90acc6]"
              placeholder="Employee Name"
              required
            />
          </div>
          <div>
            <label className="block text-[#2e3c53] font-medium mb-1">Phone Number</label>
            <input
              type="tel"
              name="phone_number"
              value={form.phone_number}
              onChange={handleChange}
              className="w-full border border-[#c8d6e6] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#90acc6]"
              placeholder="e.g. +1234567890"
              required
            />
          </div>
          <div>
            <label className="block text-[#2e3c53] font-medium mb-1">Department</label>
            <select
              name="department_id"
              value={form.department_id}
              onChange={handleChange}
              className="w-full border border-[#c8d6e6] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#90acc6]"
              required
            >
              <option value="">Select Department</option>
              {departments.map((dept) => (
                <option key={dept.id} value={dept.id}>{dept.name}</option>
              ))}
            </select>
          </div>
          {error && <div className="text-red-600 text-sm font-medium">{error}</div>}
          {success && <div className="text-green-600 text-sm font-medium">{success}</div>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#90acc6] hover:bg-[#6d8db0] text-white font-semibold py-2 px-4 rounded-md transition-colors duration-150"
          >
            {loading ? "Adding..." : "Add Employee"}
          </button>
        </form>
      </div>
    </div>
  );
}
