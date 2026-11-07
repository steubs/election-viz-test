// In dev, Vite proxies /api to FastAPI. In prod, set VITE_API_URL at build time.
const BASE = import.meta.env.VITE_API_URL ?? "";

export interface CountyResult {
  county_fips: string;
  county_name: string;
  candidates: Record<string, { party: string; votes: number }>;
  total_votes: number;
}

export async function fetchCounties(
  year: number,
  office: string,
  stateFips: string,
): Promise<CountyResult[]> {
  const res = await fetch(`${BASE}/api/races/${year}/${office}/${stateFips}/counties`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}
