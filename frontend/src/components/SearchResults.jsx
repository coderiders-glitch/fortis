import DoctorCard from "./DoctorCard.jsx";

export default function SearchResults({ data }) {
  return (
    <div className="results-content" aria-live="polite">
      <div className="results-heading">
        <h2>Search results</h2>
        <p>{data.message}</p>
      </div>
      <div className="doctor-list">
        {data.results.map((doctor) => (
          <DoctorCard key={doctor.id} doctor={doctor} />
        ))}
      </div>
    </div>
  );
}