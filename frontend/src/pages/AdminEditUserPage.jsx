import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { adminGetUser, adminUpdateUser } from "../api/authApi";
import PasswordField from "../components/PasswordField";
import { parseError } from "../utils/errorParser";

export default function AdminEditUserPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirm_password: "",
    role: "user",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      setLoading(true);
      try {
        const { data } = await adminGetUser(id);
        setForm({
          first_name: data.first_name,
          last_name: data.last_name,
          email: data.email,
          password: "",
          confirm_password: "",
          role: data.role,
        });
      } catch {
        setError("Unable to load user.");
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, [id]);

  const onChange = (event) => {
    const { name, type, checked, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const payload = { ...form };
      if (!payload.password) {
        delete payload.password;
        delete payload.confirm_password;
      }
      const { data } = await adminUpdateUser(id, payload);
      setMessage(data.message);
      setForm((prev) => ({ ...prev, password: "", confirm_password: "" }));
    } catch (err) {
      setError(parseError(err?.response?.data) || "Unable to update user.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <form className="card form-card" onSubmit={onSubmit}>
        <h1>Admin Edit User</h1>
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
        {/* <label className="field">
          <span>Role</span>
          <select name="role" value={form.role} onChange={onChange}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </label> */}
        {error && <p className="error">{error}</p>}
        {message && <p className="success">{message}</p>}
        <button className="btn primary" disabled={loading} type="submit">
          {loading ? "Saving..." : "Save"}
        </button>
        <button className="btn" type="button" onClick={() => navigate("/admin/users")}>
          Back
        </button>
      </form>
    </main>
  );
}
