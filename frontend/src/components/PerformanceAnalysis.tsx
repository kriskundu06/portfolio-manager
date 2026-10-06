import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface PerformanceAnalysisProps {
  dates: string[];
  portfolioValue: number[];
  returns: number[];
  drawdown: number[];
}

function PerformanceAnalysis({
  dates,
  portfolioValue,
  returns,
  drawdown,
}: PerformanceAnalysisProps) {
  const data = dates.map((date, index) => ({
    date,
    value: portfolioValue[index],
    return: returns[index] * 100,
    drawdown: drawdown[index] * 100,
  }));

  return (
    <div className="space-y-8">

      {/* Portfolio Growth */}
      <div className="border-y border-slate-200 bg-white p-5">

        <div className="mb-6">
          <h3 className="text-base font-semibold text-slate-900">
            Portfolio growth
          </h3>

          <p className="mt-1 text-xs text-slate-500">
            Cumulative portfolio value over the test period.
          </p>
        </div>

        <div className="h-80">

          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>

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

      {/* Monthly Returns */}
      <div className="border-y border-slate-200 bg-white p-5">

        <div className="mb-6">
          <h3 className="text-base font-semibold text-slate-900">
            Monthly returns
          </h3>

          <p className="mt-1 text-xs text-slate-500">
            Monthly portfolio returns during the test period.
          </p>
        </div>

        <div className="h-80">

          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>

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
                formatter={(value) => `${Number(value ?? 0).toFixed(2)}%`}
                contentStyle={{
                  border: "1px solid #e2e8f0",
                  borderRadius: "2px",
                  backgroundColor: "#ffffff",
                  fontSize: "12px",
                }}
              />

              <Bar
                dataKey="return"
                fill="#64748b"
              />

            </BarChart>
          </ResponsiveContainer>

        </div>
      </div>

      {/* Drawdown */}
      <div className="border-y border-slate-200 bg-white p-5">

        <div className="mb-6">
          <h3 className="text-base font-semibold text-slate-900">
            Drawdown
          </h3>

          <p className="mt-1 text-xs text-slate-500">
            Decline from the portfolio's previous peak.
          </p>
        </div>

        <div className="h-80">

          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>

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
                formatter={(value) => `${Number(value ?? 0).toFixed(2)}%`}
                contentStyle={{
                  border: "1px solid #e2e8f0",
                  borderRadius: "2px",
                  backgroundColor: "#ffffff",
                  fontSize: "12px",
                }}
              />

              <Line
                type="monotone"
                dataKey="drawdown"
                stroke="#b45309"
                strokeWidth={1.8}
                dot={false}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>
      </div>

    </div>
  );
}

export default PerformanceAnalysis;