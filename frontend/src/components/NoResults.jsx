export default function NoResults({ message }) {
  return (
    <div className="empty-state" role="status">
      <span className="empty-icon" aria-hidden="true">⌕</span>
      <h2>No results found</h2>
      <p>{message}</p>
      <p className="empty-suggestion">Try another name, speciality, or symptom.</p>
    </div>
  );
}