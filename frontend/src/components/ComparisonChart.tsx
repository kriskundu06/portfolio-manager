import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface ComparisonChartProps {
  models: {
    name: string;
    cagr: number;
  }[];
}

function ComparisonChart({
  models,
}: ComparisonChartProps) {
  const data = models.map((model) => ({
    name: model.name,
    CAGR: model.cagr * 100,
  }));

  return (
    <div className="mb-8 border-y border-slate-200 bg-white p-5">

      <div className="mb-6">
        <h3 className="text-base font-semibold text-slate-900">
          CAGR comparison
        </h3>

        <p className="mt-1 text-xs text-slate-500">
          Annualized return on the 2023–2025 test period.
        </p>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{
              top: 10,
              right: 10,
              left: 0,
              bottom: 5,
            }}
          >

            <CartesianGrid
              stroke="#e5e7eb"
              strokeDasharray="2 4"
            />

            <XAxis
              dataKey="name"
              stroke="#94a3b8"
              tick={{ fontSize: 11 }}
              tickLine={false}
              axisLine={false}
            />

            <YAxis
              stroke="#94a3b8"
              tick={{ fontSize: 11 }}
              tickLine={false}
              axisLine={false}
            />

            <Tooltip
              formatter={(value) => `${Number(value ?? 0).toFixed(2)}%`}
              contentStyle={{
                border: "1px solid #e2e8f0",
                borderRadius: "2px",
                backgroundColor: "#ffffff",
                fontSize: "12px",
              }}
            />

            <Bar
              dataKey="CAGR"
              fill="#475569"
              radius={[2, 2, 0, 0]}
              barSize={48}
            />

          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

export default ComparisonChart;