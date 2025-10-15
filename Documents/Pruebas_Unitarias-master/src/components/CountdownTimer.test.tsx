import { render, screen, fireEvent, act } from "@testing-library/react";
import '@testing-library/jest-dom';
import CountdownTimer from "./CountdownTimer";
import { describe, it, expect, beforeEach, jest } from "@jest/globals";

describe("CountdownTimer", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  it("muestra el tiempo inicial correctamente", () => {
    render(<CountdownTimer />);
    const input = screen.getByPlaceholderText("Segundos") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "5" } });
    fireEvent.click(screen.getByText("Iniciar"));

    expect(screen.getByText("5")).toBeInTheDocument();
  });

  it("disminuye en intervalos de un segundo", () => {
    render(<CountdownTimer />);
    const input = screen.getByPlaceholderText("Segundos") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "3" } });
    fireEvent.click(screen.getByText("Iniciar"));

    expect(screen.getByText("3")).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(1000);
    });
    expect(screen.getByText("2")).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(1000);
    });
    expect(screen.getByText("1")).toBeInTheDocument();
  });

  it("se detiene en 0", () => {
    render(<CountdownTimer />);
    const input = screen.getByPlaceholderText("Segundos") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "2" } });
    fireEvent.click(screen.getByText("Iniciar"));

    act(() => {
      jest.advanceTimersByTime(3000);
    });

    expect(screen.getByText("0")).toBeInTheDocument();
  });
});
