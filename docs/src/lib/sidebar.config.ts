export const SECTION_CATEGORIES = [
  { label: "Start", ids: ["home"] },
  { label: "Test Profile", ids: ["test-scenarios", "configuration", "run-modes"] },
  { label: "Operations", ids: ["ci-cd"] },
] as const;

export const SECTION_ORDER = SECTION_CATEGORIES.flatMap(({ ids }) => ids);
