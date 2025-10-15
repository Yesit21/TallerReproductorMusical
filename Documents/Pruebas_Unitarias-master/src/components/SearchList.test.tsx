// src/tests/SearchList.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import SearchList from "../components/SearchList";

describe("SearchList", () => {
  beforeEach(() => {
    render(<SearchList />);
  });

  test("muestra todos los nombres al inicio", () => {
    const items = screen.getAllByRole("listitem");
    expect(items.length).toBeGreaterThan(1);
  });

  test("filtra nombres según el input", () => {
    const input = screen.getByPlaceholderText("Buscar...");
    fireEvent.change(input, { target: { value: "Ana" } });

    expect(screen.getByText("Ana")).toBeInTheDocument();
    expect(screen.queryByText("Carlos")).not.toBeInTheDocument();
  });

  test("no distingue entre mayúsculas y minúsculas", () => {
    const input = screen.getByPlaceholderText("Buscar...");
    fireEvent.change(input, { target: { value: "ana" } });

    expect(screen.getByText(/ana/i)).toBeInTheDocument();
  });

  test("muestra 'No encontrado' si no hay coincidencias", () => {
    const input = screen.getByPlaceholderText("Buscar...");
    fireEvent.change(input, { target: { value: "ZZZ" } });

    expect(screen.getByText("No encontrado")).toBeInTheDocument();
  });

  test("vuelve a mostrar la lista completa si el campo se vacía", () => {
    const input = screen.getByPlaceholderText("Buscar...");
    fireEvent.change(input, { target: { value: "Ana" } });
    fireEvent.change(input, { target: { value: "" } });

    const items = screen.getAllByRole("listitem");
    expect(items.length).toBeGreaterThan(0);
  });

  test("no falla si el usuario ingresa solo espacios", () => {
    const input = screen.getByPlaceholderText("Buscar...");
    fireEvent.change(input, { target: { value: "   " } });

    const items = screen.getAllByRole("listitem");
    expect(items.length).toBeGreaterThan(0);
  });
});
