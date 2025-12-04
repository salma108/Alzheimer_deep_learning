import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from "recharts";

function ProbabilityBar({ probabilities, highlight }) {
  if (!probabilities) return null;

  const data = Object.entries(probabilities).map(([label, value]) => ({
    label,
    value: +(value * 100).toFixed(2)
  }));

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
          <XAxis type="number" domain={[0, 100]} hide />
          <YAxis type="category" dataKey="label" />
          <Tooltip formatter={(v) => `${v.toFixed(2)} %`} />
          <Bar dataKey="value" radius={[4, 4, 4, 4]}>
            {data.map((entry) => (
              <Cell
                key={entry.label}
                fill={entry.label === highlight ? "#4f46e5" : "#94a3b8"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ProbabilityBar;
