const API_BASE_PATH = "/api";

export async function searchDoctors(keyword) {
  const params = new URLSearchParams({ q: keyword });
  let response;

  try {
    response = await fetch(`${API_BASE_PATH}/doctors/search?${params.toString()}`, {
      method: "GET",
      headers: { Accept: "application/json" },
    });
  } catch {
    throw new Error("Unable to connect. Check your connection and try again.");
  }

  let body;
  try {
    body = await response.json();
  } catch {
    throw new Error("The search service returned an invalid response.");
  }

  if (!response.ok) {
    throw new Error(body.message || body.detail?.message || "The search could not be completed. Please try again.");
  }

  return body;
}
