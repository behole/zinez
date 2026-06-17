import { describe, expect, test } from "bun:test";
import { rowToResponse, safeParseArray } from "./zines";
import type { ZineRow, ZineResponse } from "../types";

describe("safeParseArray", () => {
  test("parses valid JSON array string", () => {
    expect(safeParseArray('["punk","hardcore"]')).toEqual(["punk", "hardcore"]);
  });

  test("returns empty array for empty string", () => {
    expect(safeParseArray("")).toEqual([]);
  });

  test("returns empty array for null/undefined string", () => {
    expect(safeParseArray(null as unknown as string)).toEqual([]);
  });

  test("returns empty array for non-array JSON", () => {
    expect(safeParseArray('"not an array"')).toEqual([]);
  });

  test("returns empty array for malformed JSON", () => {
    expect(safeParseArray("{broken")).toEqual([]);
  });

  test("handles single-element array", () => {
    expect(safeParseArray('["grindcore"]')).toEqual(["grindcore"]);
  });
});

describe("rowToResponse", () => {
  const baseRow: ZineRow = {
    id: "test-001",
    zine_name: "Maximum Rocknroll",
    issue_number: "42",
    year: "1987",
    year_primary: 1987,
    location: "San Francisco, CA",
    description: "Legendary punk zine",
    tags: '["punk","hardcore","interviews"]',
    bands_featured: '["Dead Kennedys","Black Flag"]',
    creators: "Tim Yohannan",
    circulation: "10000",
    source_type: "internet_archive",
    archive_source: "Internet Archive",
    image_url: "https://example.com/mrr042.jpg",
    ia_item_url: "https://archive.org/details/mrr042",
    ia_download_url: "",
    ia_thumb: "https://example.com/mrr042_thumb.jpg",
    attribution: "Courtesy of Internet Archive",
  };

  test("transforms row to response with parsed arrays", () => {
    const result = rowToResponse(baseRow);
    expect(result.tags).toEqual(["punk", "hardcore", "interviews"]);
    expect(result.bands_featured).toEqual(["Dead Kennedys", "Black Flag"]);
  });

  test("preserves all scalar fields", () => {
    const result = rowToResponse(baseRow);
    expect(result.id).toBe("test-001");
    expect(result.zine_name).toBe("Maximum Rocknroll");
    expect(result.year_primary).toBe(1987);
    expect(result.location).toBe("San Francisco, CA");
    expect(result.creators).toBe("Tim Yohannan");
    expect(result.circulation).toBe("10000");
    expect(result.attribution).toBe("Courtesy of Internet Archive");
  });

  test("handles empty tags and bands", () => {
    const row = { ...baseRow, tags: "", bands_featured: "" };
    const result = rowToResponse(row);
    expect(result.tags).toEqual([]);
    expect(result.bands_featured).toEqual([]);
  });

  test("response shape matches ZineResponse contract", () => {
    const result = rowToResponse(baseRow);
    const requiredKeys: (keyof ZineResponse)[] = [
      "id", "zine_name", "issue_number", "year", "year_primary",
      "location", "description", "tags", "bands_featured", "creators",
      "circulation", "source_type", "archive_source", "image_url",
      "ia_item_url", "ia_download_url", "ia_thumb", "attribution",
    ];
    for (const key of requiredKeys) {
      expect(result).toHaveProperty(key);
    }
  });
});
