import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import App from "./App.jsx";
import { searchDoctors } from "./services/api.js";
import * as apiModule from './services/api';
import * as api from './services/api';
vi.mock("./services/api.js", () => ({
  searchDoctors: vi.fn(),
}));

beforeEach(async () => {
  vi.clearAllMocks();
});

async function submitSearch(keyword) {
  const input = await screen.findByRole("searchbox");
  fireEvent.change(input, { target: { value: keyword } });
  fireEvent.submit(input.closest("form"));
}

describe("doctor search", () => {
  it("renders matching doctor data returned by the search API", async () => {
    searchDoctors.mockResolvedValue({
      results: [
        {
          id: 1,
          name: "Dr. Sarah Johnson",
          speciality: "Cardiologist",
          details: "Heart disease prevention and care.",
          symptoms: "chest pain, shortness of breath",
          experience: 15,
          location: "123 Heart Center, Medical District",
        },
      ],
      count: 1,
      message: "Found 1 matching doctor",
    });

    render(<App />);
    expect(await screen.findByRole("heading", { name: "Find a doctor" })).toBeInTheDocument();
    await submitSearch("cardio");

    expect(await screen.findByText("Dr. Sarah Johnson")).toBeInTheDocument();
    expect(searchDoctors).toHaveBeenCalledWith("cardio");
  });

  it("shows the API no-results message when a search has no matches", async () => {
    searchDoctors.mockResolvedValue({
      results: [],
      count: 0,
      message: "No results found. Try a different search term.",
    });

    render(<App />);
    await submitSearch("unmatched term");

    expect(await screen.findByText("No results found. Try a different search term.")).toBeInTheDocument();
  });

  it("validates an empty search without calling the API", async () => {
    render(<App />);
    expect(await screen.findByRole("heading", { name: "Find a doctor" })).toBeInTheDocument();

    const input = await screen.findByRole("searchbox");
    fireEvent.submit(input.closest("form"));

    expect(await screen.findByText("Enter a keyword to search for doctors.")).toBeInTheDocument();
    expect(searchDoctors).not.toHaveBeenCalled();
  });
});
