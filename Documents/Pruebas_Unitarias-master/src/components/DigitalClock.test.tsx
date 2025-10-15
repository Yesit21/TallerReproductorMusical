import { render, screen, act } from "@testing-library/react";
import DigitalClock from "./DigitalClock";
import { describe, test, expect, beforeAll, afterAll, jest } from "@jest/globals";
import '@testing-library/jest-dom';

describe("DigitalClock", () => {
  beforeAll(() => {
    jest.useFakeTimers();
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  test("muestra la hora en formato HH:MM:SS", () => {
    render(<DigitalClock />);
    const clockElement = screen.getByText(/\d{2}:\d{2}:\d{2}/);
    expect(clockElement).toBeInTheDocument();
  });

  test("avanza correctamente con el tiempo simulado", () => {
    render(<DigitalClock />);
    const initialTime = screen.getByText(/\d{2}:\d{2}:\d{2}/).textContent;
    act(() => {
      jest.advanceTimersByTime(1000);
    });
    const updatedTime = screen.getByText(/\d{2}:\d{2}:\d{2}/).textContent;
    expect(updatedTime).not.toBe(initialTime);
  });
});
