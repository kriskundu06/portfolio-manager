import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface PerformanceChartProps {
  dates: string[];
  values: number[];
}

function PerformanceChart({
  dates,
  values,
}: PerformanceChartProps) {
  const data = dates.map((date, index) => ({
    date,
    value: values[index],
  }));

  return (
    <div className="border-y border-slate-200 bg-white p-5">

      <div className="mb-6">
        <h3 className="text-base font-semibold text-slate-900">
          Portfolio value
        </h3>

        <p className="mt-1 text-xs text-slate-500">
          Cumulative value of the PPO portfolio during the 2023–2025 test period.
        </p>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{
              top: 5,
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
              dataKey="date"
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
              contentStyle={{
                border: "1px solid #e2e8f0",
                borderRadius: "2px",
                backgroundColor: "#ffffff",
                fontSize: "12px",
              }}
            />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#334155"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

export default PerformanceChart;