export const SECTION_CATEGORIES = [
  { label: "", ids: ["home"] },
  { label: "Testing", ids: ["test-scenarios", "configuration", "run-modes"] },
  { label: "CI/CD", ids: ["ci-cd"] },
] as const;

export const SECTION_ORDER = SECTION_CATEGORIES.flatMap(({ ids }) => ids);
