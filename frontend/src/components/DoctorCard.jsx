export default function DoctorCard({ doctor }) {
  return (
    <article className="doctor-card" aria-labelledby={`doctor-${doctor.id}`}>
      <div className="doctor-card-header">
        <div>
          <h3 id={`doctor-${doctor.id}`} className="doctor-name">{doctor.name}</h3>
          <p className="doctor-speciality">{doctor.speciality}</p>
        </div>
        <span className="experience-badge">{doctor.experience} years’ experience</span>
      </div>
      <p className="doctor-details">{doctor.details}</p>
      <dl className="doctor-meta">
        <div>
          <dt>Symptoms treated</dt>
          <dd>{doctor.symptoms}</dd>
        </div>
        <div>
          <dt>Location</dt>
          <dd>{doctor.location}</dd>
        </div>
      </dl>
    </article>
  );
}