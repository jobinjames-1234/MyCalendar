import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { updateCurrentUser } from "../api/authApi";
import PasswordField from "../components/PasswordField";
import { useAuth } from "../context/AuthContext";
import { parseError } from "../utils/errorParser";

export default function EditProfilePage() {
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();
  const [form, setForm] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    email: user?.email || "",
    password: "",
    confirm_password: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const onChange = (event) => setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = { ...form };
      if (!payload.password) delete payload.password;
      const { data } = await updateCurrentUser(payload);
      setMessage(data.message);
      await refreshUser();
      setForm((prev) => ({ ...prev, password: "", confirm_password: "" }));
    } catch (err) {
      setError(parseError(err?.response?.data) || "Unable to update profile.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <form className="card form-card" onSubmit={onSubmit}>
        <h1>Edit Profile</h1>
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
        <PasswordField label="New Password" name="password" value={form.password} onChange={onChange} />
        <PasswordField
          label="Confirm New Password"
          name="confirm_password"
          value={form.confirm_password}
          onChange={onChange}
        />
        {message && <p className="success">{message}</p>}
        {error && <p className="error">{error}</p>}
        <button className="btn primary" disabled={loading} type="submit">
          {loading ? "Saving..." : "Save profile"}
        </button>
        <button type="button" className="btn" onClick={() => navigate(-1)}>
          Back
        </button>
      </form>
    </main>
  );
}
