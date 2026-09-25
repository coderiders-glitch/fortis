export default function DoctorCard({ doctor }) {
  return (
    <article className="doctor-card" aria-label={`${doctor.name}, ${doctor.speciality}`}>
      <div className="doctor-card-heading">
        <div>
          <h3>{doctor.name}</h3>
          <p className="doctor-speciality">{doctor.speciality}</p>
        </div>
        <span className="experience-tag">{doctor.experience} years’ experience</span>
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
