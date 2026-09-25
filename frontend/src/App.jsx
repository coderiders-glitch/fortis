import { useState } from "react";
import { fetchDoctors } from "./services/api.js";
import SearchBox from "./components/SearchBox.jsx";
import SearchResults from "./components/SearchResults.jsx";
import NoResults from "./components/NoResults.jsx";
import * as apiModule from './services/api';
import * as api from './services/api';
export default function App() {
  const [searchState, setSearchState] = useState({
    status: "idle",
    data: null,
    error: ""
  });

  const handleSearch = async (keyword) => {
    setSearchState({ status: "loading", data: null, error: "" });
    try {
      const data = await fetchDoctors(keyword);
      setSearchState({ status: "success", data, error: "" });
    } catch (error) {
      setSearchState({
        status: "error",
        data: null,
        error: error instanceof Error ? error.message : "Unable to search right now. Please try again."
      });
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Care directory home">
          <span className="brand-mark" aria-hidden="true">+</span>
          <span>Care directory</span>
        </a>
        <span className="topbar-note">Find the right care for you</span>
      </header>

      <section className="search-page" aria-labelledby="page-title">
        <div className="page-heading">
          <p className="eyebrow">DOCTOR DIRECTORY</p>
          <h1 id="page-title" className="page-title">Doctor Search</h1>
          <p className="intro-copy">Search by doctor name, speciality, symptoms, or care details.</p>
        </div>

        <SearchBox onSearch={handleSearch} loading={searchState.status === "loading"} />

        <section className="results-section" aria-label="Doctor search results">
          {searchState.status === "idle" && (
            <p className="initial-prompt">Enter a keyword to see matching doctors.</p>
          )}
          {searchState.status === "loading" && (
            <p className="status-message" role="status">Searching doctor profiles…</p>
          )}
          {searchState.status === "error" && (
            <div className="error-message" role="alert">
              <strong>Search unavailable</strong>
              <p>{searchState.error}</p>
            </div>
          )}
          {searchState.status === "success" && searchState.data && (
            searchState.data.count === 0 ? (
              <NoResults message={searchState.data.message} />
            ) : (
              <SearchResults data={searchState.data} />
            )
          )}
        </section>
      </section>

      <footer className="site-footer">Doctor information provided for directory search.</footer>
    </main>
  );
}
