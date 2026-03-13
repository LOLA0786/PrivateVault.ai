import React, { useEffect, useMemo, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

type Rec = { id:string; title:string; impact_monthly:number; rationale:string; actions:string[]; effort:string };
type ApiRes = { provider: string; lei: number; recommendations: Rec[] };

const api = (path:string) => fetch(`http://127.0.0.1:8787${path}`).then(r=>r.json());

export default function App() {
  const [provider, setProvider] = useState<"aws"|"azure"|"gcp">("aws");
  const [data, setData] = useState<ApiRes|null>(null);

  useEffect(() => { api(`/recommendations?provider=${provider}`).then(setData); }, [provider]);

  const pie = useMemo(() => (data?.recommendations ?? []).slice(0,5).map(r => ({ name: r.title, value: r.impact_monthly })), [data]);
  return (
    <div className="wrap">
      <div className="row">
        <div className="card">
          <h2>Overview</h2>
          <p>Provider:&nbsp;
            <select value={provider} onChange={e=>setProvider(e.target.value as any)}>
              <option value="aws">AWS</option>
              <option value="azure">Azure</option>
              <option value="gcp">GCP</option>
            </select>
            &nbsp; LEI: <span className="pill">{data?.lei ?? "…"}</span>
          </p>

          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie dataKey="value" data={pie} outerRadius={110} label>
                  {pie.map((entry, index) => <Cell key={`c-${index}`} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <h2>Top Savings</h2>
          <table>
            <thead><tr><th>Recommendation</th><th>Impact / mo</th></tr></thead>
            <tbody>
              {(data?.recommendations ?? []).map(r => (
                <tr key={r.id}><td>{r.title}</td><td className="green">₹ {(r.impact_monthly*83).toFixed(0)}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card" style={{marginTop:16}}>
        <h2>Actions DSL (simulate plan)</h2>
        <textarea id="yaml" style={{width:'100%', height:140, background:'#0b1220', color:'#cfe2ff', border:'1px solid #223059', borderRadius:12, padding:8}} defaultValue={`actions:
  - id: cosmos-to-supabase
    title: "Migrate Azure CosmosDB → Supabase"
    steps:
      - run: "pg_dump ..."
      - run: "pg_restore ..."`} />
        <br />
        <button onClick={async () => {
          const yaml = (document.getElementById("yaml") as HTMLTextAreaElement).value;
          const res = await fetch("http://127.0.0.1:8787/actions/plan", { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify({ yaml }) });
          const json = await res.json();
          alert("Plan steps: " + json.plan[0]?.steps.length);
        }}>Compile Plan</button>
      </div>
    </div>
  );
}
