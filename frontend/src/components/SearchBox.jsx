export default function SearchBox({ value, onChange, onSubmit, loading, validationMessage }) {
  return (
    <form className="search-form" onSubmit={onSubmit} noValidate>
      <div className="search-field-wrap">
        <label className="search-label" htmlFor="doctor-query">Search doctors</label>
        <div className="search-field-row">
          <input
            id="doctor-query"
            name="query"
            type="search"
            value={value}
            onChange={onChange}
            placeholder="Try a name, specialty, or symptom"
            maxLength={200}
            aria-describedby={validationMessage ? "query-error" : "search-hint"}
            aria-invalid={Boolean(validationMessage)}
            disabled={loading}
          />
          <button className="search-button" type="submit" disabled={loading}>
            {loading ? "Searching…" : "Search"}
          </button>
        </div>
        {validationMessage ? (
          <p className="field-error" id="query-error" role="alert">{validationMessage}</p>
        ) : (
          <p className="field-hint" id="search-hint">Search by doctor name, specialty, symptoms, or care details.</p>
        )}
      </div>
    </form>
  );
}
