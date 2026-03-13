import YAML from "yaml";

export type ActionPlan = {
  id: string;
  title: string;
  steps: { run: string; note?: string }[];
};

export function compileActions(yamlText: string): ActionPlan[] {
  const doc = YAML.parse(yamlText);
  const out: ActionPlan[] = [];
  for (const item of doc?.actions ?? []) {
    out.push({
      id: item.id,
      title: item.title,
      steps: (item.steps || []).map((s: any) => (typeof s === "string" ? { run: s } : s))
    });
  }
  return out;
}
