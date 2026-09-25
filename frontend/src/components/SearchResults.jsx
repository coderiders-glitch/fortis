import DoctorCard from "./DoctorCard.jsx";

export default function SearchResults({ results, count, message }) {
  return (
    <section className="results-section" aria-labelledby="results-heading" aria-live="polite">
      <div className="results-heading-row">
        <h2 id="results-heading">Search results</h2>
        <span className="result-count">{count} {count === 1 ? "doctor" : "doctors"}</span>
      </div>
      <p className="results-message">{message}</p>
      <div className="doctor-list">
        {results.map((doctor) => <DoctorCard key={doctor.id} doctor={doctor} />)}
      </div>
    </section>
  );
}
