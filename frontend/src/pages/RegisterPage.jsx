import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/authApi";
import PasswordField from "../components/PasswordField";
import { parseError } from "../utils/errorParser";

const initialState = {
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  password: "",
  confirm_password: "",
};

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onChange = (event) => setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      setError(parseError(err?.response?.data) || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <form className="card form-card" onSubmit={onSubmit}>
        <h1>Create account</h1>
        <label className="field">
          <span>First name</span>
          <input name="first_name" value={form.first_name} onChange={onChange} required />
        </label>
        <label className="field">
          <span>Last name</span>
          <input name="last_name" value={form.last_name} onChange={onChange} required />
        </label>
        <label className="field">
          <span>Email</span>
          <input type="email" name="email" value={form.email} onChange={onChange} required />
        </label>
        <label className="field">
          <span>Username</span>
          <input name="username" value={form.username} onChange={onChange} required />
        </label>
        <PasswordField label="Password" name="password" value={form.password} onChange={onChange} required />
        <PasswordField
          label="Confirm password"
          name="confirm_password"
          value={form.confirm_password}
          onChange={onChange}
          required
        />
        {error && <p className="error">{error}</p>}
        <button className="btn primary" disabled={loading} type="submit">
          {loading ? "Creating..." : "Register"}
        </button>
        <Link to="/login">Back to login</Link>
      </form>
    </main>
  );
}
