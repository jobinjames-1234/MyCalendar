import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { forgotPasswordRequest } from "../api/authApi";
import { parseError } from "../utils/errorParser";

export default function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleGenerate = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const { data } = await forgotPasswordRequest({ email });
      setMessage("Password reset! Redirecting to login...");
      setTimeout(() => {
        navigate(`/login?username=${data.username}&password=${data.generated_password}`);
      }, 1500);
    } catch (err) {
      setError(parseError(err?.response?.data) || "Unable to generate reset token.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="card form-card">
        <h1>Forgot Password</h1>
        <p>Enter your email to reset your password to <strong>username@123456789</strong> and autofill the login form.</p>
        <form onSubmit={handleGenerate}>
          <label className="field">
            <span>Email</span>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <button type="submit" className="btn primary" disabled={loading}>
            {loading ? "Resetting..." : "Reset and Go to Login"}
          </button>
        </form>

        {message && <p className="success">{message}</p>}
        {error && <p className="error">{error}</p>}
        <Link to="/login">Back to login</Link>
      </div>
    </main>
  );
}
