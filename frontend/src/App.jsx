import { useState } from "react";
import { searchDoctors } from "./services/api.js";
import SearchBox from "./components/SearchBox.jsx";
import SearchResults from "./components/SearchResults.jsx";
import NoResults from "./components/NoResults.jsx";
import * as apiModule from './services/api';
import * as api from './services/api';
export default function App() {
  const [query, setQuery] = useState("");
  const [searchState, setSearchState] = useState("idle");
  const [results, setResults] = useState([]);
  const [resultMessage, setResultMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [validationMessage, setValidationMessage] = useState("");

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    if (validationMessage) setValidationMessage("");
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();
    const keyword = query.trim();
    if (!keyword) {
      setValidationMessage("Enter a keyword to search for doctors.");
      setSearchState("idle");
      setResults([]);
      setResultMessage("");
      setErrorMessage("");
      return;
    }
    if (keyword.length > 200) {
      setValidationMessage("Search must be 200 characters or fewer.");
      return;
    }

    setValidationMessage("");
    setSearchState("loading");
    setErrorMessage("");
    setResults([]);
    setResultMessage("");

    try {
      const response = await searchDoctors(keyword);
      setResults(response.results);
      setResultMessage(response.message);
      setSearchState(response.count === 0 ? "empty" : "success");
    } catch (error) {
      setErrorMessage(error.message || "The search could not be completed. Please try again.");
      setSearchState("error");
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Care directory home">
          <span className="brand-mark" aria-hidden="true">+</span>
          <span>Care directory</span>
        </a>
        <span className="topbar-note">Doctor profiles</span>
      </header>

      <div className="content-wrap">
        <section className="search-panel" aria-labelledby="page-heading">
          <div className="eyebrow"><span className="eyebrow-dot" /> PROVIDER DIRECTORY</div>
          <h1 className="page-title" id="page-heading">Find a doctor</h1>
          <p className="page-description">Search doctor profiles by name, specialty, symptoms, or the care they provide.</p>
          <SearchBox
            value={query}
            onChange={handleInputChange}
            onSubmit={handleSubmit}
            loading={searchState === "loading"}
            validationMessage={validationMessage}
          />
        </section>

        <section className="results-area" aria-label="Doctor search output">
          {searchState === "idle" && (
            <p className="idle-message">Enter a search term to explore available doctor profiles.</p>
          )}
          {searchState === "loading" && (
            <p className="loading-message" role="status"><span className="loading-indicator" />Searching doctor profiles…</p>
          )}
          {searchState === "error" && (
            <div className="error-message" role="alert">
              <strong>Search unavailable</strong>
              <p>{errorMessage}</p>
              <button className="retry-button" type="button" onClick={handleSubmit}>Try again</button>
            </div>
          )}
          {searchState === "empty" && <NoResults message={resultMessage} />}
          {searchState === "success" && (
            <SearchResults results={results} count={results.length} message={resultMessage} />
          )}
        </section>
      </div>
      <footer className="site-footer">Search doctor profiles by the details that matter to you.</footer>
    </main>
  );
}
