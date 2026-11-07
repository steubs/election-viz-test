import * as d3 from "d3";
import { feature } from "topojson-client";
import type { Topology } from "topojson-specification";
import counties from "us-atlas/counties-10m.json";
import { fetchCounties } from "./api";

const stateSelect = document.querySelector<HTMLSelectElement>("#state")!;
const svg = d3.select<SVGSVGElement, unknown>("#map");

const topo = counties as unknown as Topology;
const states = (feature(topo, topo.objects.states as never) as unknown as GeoJSON.FeatureCollection)
  .features as GeoJSON.Feature[];
const allCounties = (feature(topo, topo.objects.counties as never) as unknown as GeoJSON.FeatureCollection)
  .features as GeoJSON.Feature[];

for (const s of states.sort((a, b) => String(a.properties?.name).localeCompare(String(b.properties?.name)))) {
  stateSelect.add(new Option(String(s.properties?.name), String(s.id)));
}

// Winner-margin colour: blue (D) <-> red (R), saturation scales with margin.
const margin = d3.scaleDiverging(d3.interpolateRdBu).domain([1, 0, -1]); // +1 = R, -1 = D

async function draw(stateFips: string) {
  const geo: GeoJSON.FeatureCollection = {
    type: "FeatureCollection",
    features: allCounties.filter((c) => String(c.id).startsWith(stateFips)),
  };
  const projection = d3.geoMercator().fitSize([960, 600], geo);
  const path = d3.geoPath(projection);
  svg.attr("viewBox", "0 0 960 600");

  let byFips = new Map<string, number>();
  try {
    const rows = await fetchCounties(2020, "senate", stateFips);
    byFips = new Map(
      rows.map((r) => {
        const v = (p: string) =>
          Object.values(r.candidates).filter((c) => c.party === p).reduce((a, c) => a + c.votes, 0);
        return [r.county_fips, (v("REPUBLICAN") - v("DEMOCRAT")) / (r.total_votes || 1)];
      }),
    );
  } catch {
    // No data yet (backend down or race missing): draw the bare map.
  }

  svg
    .selectAll("path")
    .data(geo.features)
    .join("path")
    .attr("d", path)
    .attr("fill", (d) => (byFips.has(String(d.id)) ? margin(byFips.get(String(d.id))!) : "#ddd"))
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.5)
    .selectAll("title")
    .data((d) => [d])
    .join("title")
    .text((d) => String(d.properties?.name));
}

stateSelect.addEventListener("change", () => draw(stateSelect.value));
stateSelect.value = states[0] ? String(states[0].id) : "";
draw(stateSelect.value);
