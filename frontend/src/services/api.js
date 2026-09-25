const API_BASE = "/api";

export async function fetchDoctors(keyword) {
  const query = typeof keyword === "string" ? keyword.trim() : "";

  if (!query) {
    throw new Error("Enter a keyword to search for doctors.");
  }
  if (query.length > 200) {
    throw new Error("Search terms must be 200 characters or fewer.");
  }

  const response = await fetch(
    `${API_BASE}/doctors/search?q=${encodeURIComponent(query)}`,
    {
      method: "GET",
      headers: { Accept: "application/json" },
    }
  );

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(
      payload && typeof payload.message === "string"
        ? payload.message
        : "Unable to search right now. Please try again."
    );
  }

  if (
    !payload ||
    !Array.isArray(payload.results) ||
    typeof payload.count !== "number" ||
    typeof payload.message !== "string"
  ) {
    throw new Error("The search response was invalid. Please try again.");
  }

  return payload;
}
