export default function NoResults({ message }) {
  return (
    <section className="no-results" role="status" aria-live="polite">
      <span className="no-results-mark" aria-hidden="true">⌕</span>
      <h2>No results found</h2>
      <p>{message}</p>
      <p className="no-results-tip">Try another name, specialty, symptom, or keyword.</p>
    </section>
  );
}
