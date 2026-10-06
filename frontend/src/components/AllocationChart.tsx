import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface AllocationChartProps {
  SP500: number;
  NASDAQ: number;
  GOLD: number;
  OIL: number;
  NIFTY: number;
}

function AllocationChart({
  SP500,
  NASDAQ,
  GOLD,
  OIL,
  NIFTY,
}: AllocationChartProps) {
  const data = [
    { name: "S&P 500", value: SP500 },
    { name: "NASDAQ", value: NASDAQ },
    { name: "Gold", value: GOLD },
    { name: "Oil", value: OIL },
    { name: "NIFTY", value: NIFTY },
  ];

  const colors = [
    "#0b69ec70",
    "#e80d85",
    "#94a3b8",
    "#6ca87a",
    "#01060f",
  ];

  return (
    <div className="border-y border-slate-200 bg-white p-5">

      <div className="mb-6">
        <h3 className="text-base font-semibold text-slate-900">
          Allocation
        </h3>

        <p className="mt-1 text-xs text-slate-500">
          Current portfolio weights produced by the PPO policy.
        </p>
      </div>

      <div className="grid min-w-0 grid-cols-1 items-center gap-5 sm:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">

        <div className="h-64 min-w-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>

              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={95}
                paddingAngle={1}
                stroke="#ffffff"
                strokeWidth={2}
              >
                {data.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={colors[index]}
                  />
                ))}
              </Pie>

              <Tooltip
              formatter={(value) =>`${Number(value ?? 0).toFixed(1)}%`}
              />

            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-3">

          {data.map((asset, index) => (
            <div
              key={asset.name}
              className="flex items-center justify-between text-sm"
            >
              <div className="flex items-center gap-2">

                <span
                  className="h-2.5 w-2.5"
                  style={{ backgroundColor: colors[index] }}
                />

                <span className="text-slate-600">
                  {asset.name}
                </span>

              </div>

              <span className="font-medium tabular-nums text-slate-900">
                {(asset.value * 100).toFixed(1)}%
              </span>
            </div>
          ))}

        </div>

      </div>
    </div>
  );
}

export default AllocationChart;