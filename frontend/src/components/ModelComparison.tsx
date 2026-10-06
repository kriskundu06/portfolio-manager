import { useEffect, useState } from "react";

import {
  getComparison,
  type ModelResult,
} from "../services/api";

import ComparisonChart from "./ComparisonChart";

function ModelComparison() {
  const [models, setModels] = useState<ModelResult[]>([]);

  useEffect(() => {
    getComparison()
      .then(setModels)
      .catch((error) =>
        console.error("Comparison error:", error)
      );
  }, []);

  return (
    <div>

      {models.length > 0 && (
        <ComparisonChart models={models} />
      )}

      <div className="border-y border-slate-200 bg-white">

        <div className="border-b border-slate-200 px-5 py-5">
          <h3 className="text-base font-semibold text-slate-900">
            Detailed comparison
          </h3>

          <p className="mt-1 text-xs text-slate-500">
            Performance and risk statistics calculated from the same
            2023–2025 test period.
          </p>
        </div>

        <div className="overflow-x-auto">

          <table className="w-full min-w-[850px] text-left text-sm">

            <thead className="border-b border-slate-200 bg-slate-50">
              <tr className="text-xs text-slate-500">

                <th className="px-5 py-3 font-medium">
                  Model
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Return
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  CAGR
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Volatility
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Sharpe
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Sortino
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Max drawdown
                </th>

                <th className="px-4 py-3 text-right font-medium">
                  Calmar
                </th>

              </tr>
            </thead>

            <tbody>

              {models.map((model, index) => (
                <tr
                  key={model.name}
                  className={`border-b border-slate-100 last:border-b-0 ${
                    index === 0
                      ? "bg-slate-50/70"
                      : "bg-white"
                  }`}
                >

                  <td className="px-5 py-4 font-medium text-slate-800">
                    {model.name}

                    {index === 0 && (
                      <span className="ml-2 text-[10px] font-medium uppercase tracking-wide text-slate-400">
                        selected
                      </span>
                    )}
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {(model.total_return * 100).toFixed(2)}%
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {(model.cagr * 100).toFixed(2)}%
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {(model.volatility * 100).toFixed(2)}%
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {model.sharpe.toFixed(2)}
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {model.sortino.toFixed(2)}
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {(model.max_drawdown * 100).toFixed(2)}%
                  </td>

                  <td className="px-4 py-4 text-right tabular-nums text-slate-700">
                    {model.calmar.toFixed(2)}
                  </td>

                </tr>
              ))}

            </tbody>

          </table>

        </div>
      </div>

    </div>
  );
}

export default ModelComparison;