import { useEffect, useState } from "react";

import {
  getPortfolio,
  getPerformance,
  getMetrics,
  type Portfolio,
  type Performance,
  type Metrics,
} from "./services/api";

import PerformanceChart from "./components/PerformanceChart";
import AllocationChart from "./components/AllocationChart";
import ModelComparison from "./components/ModelComparison";
import PerformanceAnalysis from "./components/PerformanceAnalysis";

type Page = "dashboard" | "performance" | "comparison" | "about";

function App() {
  const [page, setPage] = useState<Page>("dashboard");

  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [performance, setPerformance] = useState<Performance | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(false);

      const [portfolioData, performanceData, metricsData] =
        await Promise.all([
          getPortfolio(),
          getPerformance(),
          getMetrics(),
        ]);

      setPortfolio(portfolioData);
      setPerformance(performanceData);
      setMetrics(metricsData);
    } catch (err) {
      console.error("API error:", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f6f7f9] text-[#172033] flex items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-6 w-6 animate-spin rounded-full border-2 border-slate-200 border-t-slate-700" />

          <p className="text-sm font-medium">
            Loading portfolio data
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Connecting to the analysis service
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#f6f7f9] text-[#172033] flex items-center justify-center px-6">
        <div className="w-full max-w-md border border-slate-200 bg-white p-8 text-center shadow-sm">
          <p className="text-sm font-semibold text-red-600">
            Connection error
          </p>

          <h2 className="mt-2 text-xl font-semibold">
            Unable to load portfolio data
          </h2>

          <p className="mt-3 text-sm leading-6 text-slate-500">
            The FastAPI backend could not be reached. Check that the backend
            is running and try again.
          </p>

          <button
            onClick={loadData}
            className="mt-6 border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f6f7f9] text-[#172033]">

      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="flex min-h-[68px] items-center justify-between px-6 lg:px-8">

          <div>
            <h1 className="text-lg font-semibold tracking-tight">
              RL-based Portfolio Manager
            </h1>

            <p className="mt-0.5 text-xs text-slate-500">
              Reinforcement learning for multi-asset allocation
            </p>
          </div>

          <div className="hidden text-right sm:block">
            <p className="text-xs font-medium text-slate-700">
              PPO Market Strategy
            </p>

            <p className="text-xs text-slate-500">
              Test period · 2023–2025
            </p>
          </div>

        </div>
      </header>

      <div className="flex">

        {/* Sidebar */}
        <aside className="hidden min-h-[calc(100vh-68px)] w-56 shrink-0 border-r border-slate-200 bg-white md:block">

          <div className="p-5">

            <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">
              Overview
            </p>

            <nav className="space-y-0.5">

              <NavButton
                label="Dashboard"
                active={page === "dashboard"}
                onClick={() => setPage("dashboard")}
              />

              <NavButton
                label="Performance"
                active={page === "performance"}
                onClick={() => setPage("performance")}
              />

              <NavButton
                label="Model Comparison"
                active={page === "comparison"}
                onClick={() => setPage("comparison")}
              />

            </nav>

            <p className="mb-3 mt-8 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">
              Project
            </p>

            <nav>
              <NavButton
                label="About"
                active={page === "about"}
                onClick={() => setPage("about")}
              />
            </nav>

          </div>

          <div className="absolute bottom-0 w-56 border-t border-slate-200 px-5 py-4">
            <p className="text-[11px] text-slate-400">
              Research prototype
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Historical backtest analysis
            </p>
          </div>

        </aside>

        {/* Main content */}
        <main className="min-w-0 flex-1 px-5 py-7 lg:px-10 lg:py-9">

          {page === "dashboard" && (
            <Dashboard
              portfolio={portfolio}
              performance={performance}
              metrics={metrics}
            />
          )}

          {page === "performance" && performance && (
            <PerformancePage performance={performance} />
          )}

          {page === "comparison" && (
            <ComparisonPage />
          )}

          {page === "about" && (
            <AboutPage />
          )}

        </main>
      </div>
    </div>
  );
}

/* ---------------- Navigation ---------------- */

function NavButton({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full border-l-2 px-3 py-2 text-left text-sm transition ${
        active
          ? "border-slate-800 bg-slate-50 font-medium text-slate-900"
          : "border-transparent text-slate-500 hover:bg-slate-50 hover:text-slate-800"
      }`}
    >
      {label}
    </button>
  );
}

/* ---------------- Dashboard ---------------- */

function Dashboard({
  portfolio,
  performance,
  metrics,
}: {
  portfolio: Portfolio | null;
  performance: Performance | null;
  metrics: Metrics | null;
}) {
  return (
    <div className="mx-auto flex min-h-[calc(100vh-68px)] max-w-7xl flex-col">

      <PageHeading
        eyebrow="Overview"
        title="Portfolio overview"
        description="Current allocation and out-of-sample performance of the PPO strategy."
      />

      {metrics && (
        <section className="mb-10 grid grid-cols-2 border-y border-slate-200 bg-white lg:grid-cols-4">

          <MetricBlock
            label="CAGR"
            value={`${(metrics.cagr * 100).toFixed(2)}%`}
          />

          <MetricBlock
            label="Sharpe ratio"
            value={metrics.sharpe.toFixed(2)}
          />

          <MetricBlock
            label="Sortino ratio"
            value={metrics.sortino.toFixed(2)}
          />

          <MetricBlock
            label="Maximum drawdown"
            value={`${(metrics.max_drawdown * 100).toFixed(2)}%`}
          />

        </section>
      )}

      {portfolio && (
        <section className="mb-10">

          <SectionTitle
            title="Current allocation"
            description="Portfolio weights generated by PPO."
          />

          <div className="border-y border-slate-200 bg-white">
            <AllocationRow
              name="S&P 500"
              value={portfolio.SP500}
            />

            <AllocationRow
              name="NASDAQ"
              value={portfolio.NASDAQ}
            />

            <AllocationRow
              name="Gold"
              value={portfolio.GOLD}
            />

            <AllocationRow
              name="Oil"
              value={portfolio.OIL}
            />

            <AllocationRow
              name="NIFTY"
              value={portfolio.NIFTY}
            />
          </div>

        </section>
      )}

      {portfolio && performance && (
        <section className="grid grid-cols-1 gap-8 xl:grid-cols-[1fr_1.35fr]">

          <AllocationChart
            SP500={portfolio.SP500}
            NASDAQ={portfolio.NASDAQ}
            GOLD={portfolio.GOLD}
            OIL={portfolio.OIL}
            NIFTY={portfolio.NIFTY}
          />

          <PerformanceChart
            dates={performance.dates}
            values={performance.portfolio_value}
          />

        </section>
      )}
       <footer className="mt-auto pt-8 text-right text-xs text-slate-400">
        Made with <span className="text-red-500">♥</span> by Krishanu Kundu
      </footer>

    </div>
  );
}

/* ---------------- Performance ---------------- */

function PerformancePage({
  performance,
}: {
  performance: Performance;
}) {
  return (
    <div className="mx-auto max-w-7xl">

      <PageHeading
        eyebrow="Analysis"
        title="Performance"
        description="Detailed evaluation of the PPO portfolio on unseen 2023–2025 test data."
      />

      <PerformanceAnalysis
        dates={performance.dates}
        portfolioValue={performance.portfolio_value}
        returns={performance.returns}
        drawdown={performance.drawdown}
      />

    </div>
  );
}

/* ---------------- Comparison ---------------- */

function ComparisonPage() {
  return (
    <div className="mx-auto max-w-7xl">

      <PageHeading
        eyebrow="Research"
        title="Model comparison"
        description="Comparison of market-feature strategy and sentiment-enhanced PPO strategies on the same test period."
      />

      <ModelComparison />

    </div>
  );
}

/* ---------------- About ---------------- */

function AboutPage() {
  return (
    <div className="mx-auto max-w-5xl">

      <PageHeading
        eyebrow="Project"
        title="About this project"
        description="An end-to-end reinforcement learning system for multi-asset portfolio management."
      />

      <div className="space-y-10">

        <section>
          <SectionTitle title="Overview" />

          <p className="max-w-3xl text-[15px] leading-7 text-slate-600">
            This project explores whether reinforcement learning can learn
            useful portfolio allocation policies across multiple asset
            classes. A PPO agent interacts with a custom Gymnasium environment
            and learns portfolio weights from historical market features.
          </p>

          <p className="mt-4 max-w-3xl text-[15px] leading-7 text-slate-600">
            The final strategy is evaluated on data that was not used during
            training. Additional sentiment-based experiments were conducted
            using financial news features, but the market-feature PPO
            ultimately produced the strongest out-of-sample results.
          </p>
        </section>

        <section>
          <SectionTitle
            title="Pipeline"
            description="From historical data to the portfolio dashboard."
          />

          <div className="border-y border-slate-200 bg-white">

            <PipelineRow number="01" text="Market data" />
            <PipelineRow number="02" text="Feature engineering" />
            <PipelineRow number="03" text="Gymnasium portfolio environment" />
            <PipelineRow number="04" text="PPO training" />
            <PipelineRow number="05" text="Backtesting" />
            <PipelineRow number="06" text="Risk and performance analysis" />
            <PipelineRow number="07" text="FastAPI" />
            <PipelineRow number="08" text="React dashboard" />

          </div>
        </section>

        <section>
          <SectionTitle title="Experiment design" />

          <div className="grid grid-cols-1 border-y border-slate-200 bg-white sm:grid-cols-2 lg:grid-cols-4">

            <ExperimentBlock
              title="Training"
              value="2008–2020"
            />

            <ExperimentBlock
              title="Validation"
              value="2021–2022"
            />

            <ExperimentBlock
              title="Final test"
              value="2023–2025"
            />

            <ExperimentBlock
              title="2026"
              value="Untouched"
            />

          </div>
        </section>

        <section>
          <SectionTitle title="Asset universe" />

          <div className="grid grid-cols-1 gap-px border border-slate-200 bg-slate-200 sm:grid-cols-2 lg:grid-cols-5">

            <AssetBlock name="S&P 500" description="US equities" />
            <AssetBlock name="NASDAQ" description="US technology equities" />
            <AssetBlock name="Gold" description="Commodity" />
            <AssetBlock name="Oil" description="Energy commodity" />
            <AssetBlock name="NIFTY" description="Indian equities" />

          </div>
        </section>

        <section>
          <SectionTitle title="Sentiment experiment" />

          <p className="max-w-3xl text-[15px] leading-7 text-slate-600">
            Financial news sentiment was incorporated into two experimental
            PPO variants using FinBERT-derived features. Both variants
            underperformed the market-feature PPO during the final test
            period.
          </p>

          <div className="mt-5 border-y border-slate-200 bg-white">

            <ResultRow
              model="Market PPO"
              cagr="19.94%"
              sharpe="1.87"
              drawdown="−7.91%"
            />

            <ResultRow
              model="Sentiment PPO v1"
              cagr="14.80%"
              sharpe="1.25"
              drawdown="−12.53%"
            />

            <ResultRow
              model="Sentiment PPO v2"
              cagr="10.77%"
              sharpe="0.74"
              drawdown="−13.42%"
            />

          </div>
        </section>

        <section>
          <SectionTitle title="Technology" />

          <div className="flex flex-wrap gap-2">

            {[
              "Python",
              "Pandas",
              "NumPy",
              "Gymnasium",
              "Stable-Baselines3",
              "PPO",
              "FastAPI",
              "React",
              "TypeScript",
              "Tailwind CSS",
              "Recharts",
            ].map((item) => (
              <span
                key={item}
                className="border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-600"
              >
                {item}
              </span>
            ))}

          </div>
        </section>

        <section className="border-t border-slate-200 pt-7">

          <p className="text-xs leading-5 text-slate-500">
            This is a research and educational project. Historical backtest
            performance does not guarantee future results and the displayed
            allocations should not be interpreted as financial advice.
          </p>

        </section>

      </div>
    </div>
  );
}

/* ---------------- Reusable UI ---------------- */

function PageHeading({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <div className="mb-10">

      <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-slate-400">
        {eyebrow}
      </p>

      <h2 className="text-3xl font-semibold tracking-tight text-slate-900">
        {title}
      </h2>

      <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
        {description}
      </p>

    </div>
  );
}

function SectionTitle({
  title,
  description,
}: {
  title: string;
  description?: string;
}) {
  return (
    <div className="mb-4">

      <h3 className="text-base font-semibold text-slate-900">
        {title}
      </h3>

      {description && (
        <p className="mt-1 text-xs text-slate-500">
          {description}
        </p>
      )}

    </div>
  );
}

function MetricBlock({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="border-b border-slate-200 px-5 py-5 sm:border-r lg:border-b-0">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
        {value}
      </p>
    </div>
  );
}

function AllocationRow({
  name,
  value,
}: {
  name: string;
  value: number;
}) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 last:border-b-0">

      <span className="text-sm font-medium text-slate-700">
        {name}
      </span>

      <div className="flex items-center gap-4">

        <div className="hidden h-1.5 w-32 overflow-hidden bg-slate-100 sm:block">
          <div
            className="h-full bg-blue-700"
            style={{ width: `${value * 100}%` }}
          />
        </div>

        <span className="w-14 text-right text-sm font-medium tabular-nums text-slate-900">
          {(value * 100).toFixed(1)}%
        </span>

      </div>

    </div>
  );
}

function PipelineRow({
  number,
  text,
}: {
  number: string;
  text: string;
}) {
  return (
    <div className="flex items-center gap-5 border-b border-slate-100 px-5 py-4 last:border-b-0">

      <span className="w-6 font-mono text-xs text-slate-400">
        {number}
      </span>

      <span className="text-sm text-slate-700">
        {text}
      </span>

    </div>
  );
}

function ExperimentBlock({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="border-b border-slate-200 px-5 py-5 lg:border-b-0 lg:border-r last:border-r-0">
      <p className="text-xs text-slate-500">
        {title}
      </p>

      <p className="mt-2 font-medium text-slate-900">
        {value}
      </p>
    </div>
  );
}

function AssetBlock({
  name,
  description,
}: {
  name: string;
  description: string;
}) {
  return (
    <div className="bg-white p-5">
      <p className="text-sm font-semibold text-slate-900">
        {name}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {description}
      </p>
    </div>
  );
}

function ResultRow({
  model,
  cagr,
  sharpe,
  drawdown,
}: {
  model: string;
  cagr: string;
  sharpe: string;
  drawdown: string;
}) {
  return (
    <div className="grid grid-cols-4 border-b border-slate-100 px-5 py-4 text-sm last:border-b-0">

      <span className="font-medium text-slate-800">
        {model}
      </span>

      <span className="text-right tabular-nums text-slate-700">
        {cagr}
      </span>

      <span className="text-right tabular-nums text-slate-700">
        {sharpe}
      </span>

      <span className="text-right tabular-nums text-slate-700">
        {drawdown}
      </span>

    </div>
  );
}

export default App;