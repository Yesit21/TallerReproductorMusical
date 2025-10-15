// src/tests/ColorPicker.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import ColorPicker from "../components/ColorPicker";

describe("ColorPicker", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("muestra el color inicial (blanco)", () => {
    render(<ColorPicker />);
    const box = screen.getByTestId("color-box");
    expect(box).toHaveStyle({ backgroundColor: "#ffffff" });
  });

  test("cambia el color al seleccionar uno nuevo", () => {
    render(<ColorPicker />);
  // Buscar el input de tipo color
  const input = screen.getByLabelText('Color');
    const box = screen.getByTestId("color-box");

  fireEvent.change(input, { target: { value: "#ff0000" } });
    expect(box).toHaveStyle({ backgroundColor: "#ff0000" });
  });

  test("guarda el color en localStorage", () => {
  const setItemSpy = jest.spyOn(window.localStorage, 'setItem');
    render(<ColorPicker />);
    const input = screen.getByLabelText('Color');

    fireEvent.change(input, { target: { value: "#00ff00" } });
    expect(setItemSpy).toHaveBeenCalledWith("selectedColor", "#00ff00");
    setItemSpy.mockRestore();
  });
});
