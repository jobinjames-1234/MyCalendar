import { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";

export default function PasswordField({
  label,
  name,
  value,
  onChange,
  placeholder = "",
  required = false,
}) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <label className="field">
      <span>{label}</span>
      <div className="password-wrapper">
        <input
          type={showPassword ? "text" : "password"}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
        />
        <button type="button" className="icon-button" onClick={() => setShowPassword((prev) => !prev)}>
          {showPassword ? <FiEyeOff /> : <FiEye />}
        </button>
      </div>
    </label>
  );
}
