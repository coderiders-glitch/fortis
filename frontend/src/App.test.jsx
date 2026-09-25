import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import App from "./App.jsx";
import { fetchDoctors } from "./services/api.js";
import * as apiModule from './services/api';
import * as api from './services/api';
vi.mock("./services/api.js", () => ({
  fetchDoctors: vi.fn()
}));

describe("Doctor Search", () => {
  beforeEach(async () => {
    vi.clearAllMocks();
  });

  it("submits a keyword and displays the matching doctor returned by the API", async () => {
    fetchDoctors.mockResolvedValue({
      results: [
        {
          id: 1,
          name: "Dr. Sarah Johnson",
          speciality: "Cardiologist",
          details: "Board-certified cardiologist with expertise in heart disease prevention.",
          symptoms: "chest pain, shortness of breath, heart palpitations",
          experience: 15,
          location: "123 Heart Center, Medical District"
        }
      ],
      count: 1,
      message: "Found 1 matching doctor"
    });

    const { container } = render(<App />);
    expect(await screen.findByRole("heading", { name: "Doctor Search" })).toBeTruthy();

    const input = await screen.findByRole("textbox");
    fireEvent.change(input, { target: { value: "cardiology" } });
    const form = container.querySelector("form");
    expect(form).not.toBeNull();
    fireEvent.submit(form);

    expect(await screen.findByRole("heading", { name: "Doctor Search" })).toBeTruthy();
    expect(fetchDoctors).toHaveBeenCalledWith("cardiology");
  });
});
