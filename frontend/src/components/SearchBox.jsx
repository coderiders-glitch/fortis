import { useState } from "react";

export default function SearchBox({ onSearch, loading }) {
  const [formData, setFormData] = useState({ query: "" });
  const [validationMessage, setValidationMessage] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    if (validationMessage) {
      setValidationMessage("");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const keyword = formData.query.trim();
    if (!keyword) {
      setValidationMessage("Enter a keyword to search.");
      return;
    }
    if (keyword.length > 200) {
      setValidationMessage("Search terms must be 200 characters or fewer.");
      return;
    }
    setValidationMessage("");
    onSearch(keyword);
  };

  return (
    <form className="search-form" onSubmit={handleSubmit} noValidate>
      <label className="search-label" htmlFor="doctor-query">Search doctors</label>
      <div className="search-controls">
        <div className="search-input-wrap">
          <span className="search-icon" aria-hidden="true">⌕</span>
          <input
            id="doctor-query"
            name="query"
            type="search"
            value={formData.query}
            onChange={handleChange}
            maxLength={200}
            placeholder="Try “cardiologist” or “headaches”"
            aria-describedby={validationMessage ? "search-validation" : "search-hint"}
            aria-invalid={Boolean(validationMessage)}
            disabled={loading}
          />
        </div>
        <button className="search-button" type="submit" disabled={loading}>
          {loading ? "Searching…" : "Search"}
        </button>
      </div>
      {validationMessage ? (
        <p className="validation-message" id="search-validation" role="alert">{validationMessage}</p>
      ) : (
        <p className="search-hint" id="search-hint">Search across names, specialities, symptoms, and care details.</p>
      )}
    </form>
  );
}