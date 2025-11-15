import { useMemo, useState } from "react";
import { LaunchRunForm } from "./components/LaunchRunForm";
import { RunDetailPanel } from "./components/RunDetailPanel";
import { RunTable } from "./components/RunTable";
import { useRunDetail, useRuns } from "./hooks/useRuns";
import type { AgentRunSummary } from "./types";

function SalesforceHeader() {
  return (
    <header style={{
      height: "50px",
      background: "var(--sf-white)",
      borderBottom: "1px solid var(--sf-border-color)",
      display: "flex",
      alignItems: "center",
      padding: "0 var(--sf-spacing-lg)",
      boxShadow: "var(--sf-shadow-sm)",
      position: "sticky",
      top: 0,
      zIndex: 1000
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: "var(--sf-spacing-md)" }}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="var(--sf-primary-blue)"/>
          <path d="M2 17L12 22L22 17V12L12 17L2 12V17Z" fill="var(--sf-primary-blue)"/>
        </svg>
        <h1 style={{
          margin: 0,
          fontSize: "16px",
          fontWeight: 600,
          color: "var(--sf-dark-navy)",
          fontFamily: "var(--sf-font-heading)"
        }}>
          Agentforce
        </h1>
      </div>
      <nav style={{
        marginLeft: "var(--sf-spacing-xxl)",
        display: "flex",
        gap: "var(--sf-spacing-xl)",
        flex: 1
      }}>
        <a href="#" style={{
          color: "var(--sf-primary-blue)",
          fontWeight: 600,
          borderBottom: "2px solid var(--sf-primary-blue)",
          paddingBottom: "14px"
        }}>
          Lost Opportunity Agent
        </a>
        <a href="#" style={{
          color: "var(--sf-text-gray)",
          paddingBottom: "14px"
        }}>
          Analytics
        </a>
        <a href="#" style={{
          color: "var(--sf-text-gray)",
          paddingBottom: "14px"
        }}>
          Settings
        </a>
      </nav>
      <div style={{ display: "flex", alignItems: "center", gap: "var(--sf-spacing-md)" }}>
        <span style={{
          color: "var(--sf-secondary-gray)",
          fontSize: "12px",
          padding: "4px 8px",
          background: "var(--sf-neutral-info)",
          borderRadius: "var(--sf-radius-sm)"
        }}>
          Local Emulator
        </span>
      </div>
    </header>
  );
}

function Dashboard() {
  const { data: runs = [], isLoading, isError, error } = useRuns();
  const [selected, setSelected] = useState<AgentRunSummary | null>(null);
  const { data: detail } = useRunDetail(selected?.id ?? null);

  const sortedRuns = useMemo(() => runs.slice().sort((a, b) => (a.started_at < b.started_at ? 1 : -1)), [runs]);

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh", background: "var(--sf-light-gray)" }}>
      <SalesforceHeader />

      <div style={{
        padding: "var(--sf-spacing-lg)",
        background: "var(--sf-white)",
        borderBottom: "1px solid var(--sf-border-color)"
      }}>
        <h2 style={{
          margin: "0 0 var(--sf-spacing-sm) 0",
          fontSize: "20px",
          fontWeight: 600,
          color: "var(--sf-dark-navy)"
        }}>
          Agent Runs
        </h2>
        <p style={{
          margin: 0,
          color: "var(--sf-secondary-gray)",
          fontSize: "13px"
        }}>
          Monitor and manage Lost Opportunity Agent executions
        </p>
      </div>

      <LaunchRunForm />

      <div style={{ display: "flex", flex: 1, overflow: "hidden", gap: "var(--sf-spacing-lg)", padding: "var(--sf-spacing-lg)" }}>
        <div style={{
          flex: 1,
          background: "var(--sf-white)",
          borderRadius: "var(--sf-radius-md)",
          boxShadow: "var(--sf-shadow-md)",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column"
        }}>
          <div style={{
            padding: "var(--sf-spacing-lg)",
            borderBottom: "1px solid var(--sf-border-color)",
            background: "var(--sf-white)"
          }}>
            <h3 style={{ margin: 0, fontSize: "14px", fontWeight: 600, color: "var(--sf-dark-navy)" }}>
              Recent Runs ({runs.length})
            </h3>
          </div>
          <div style={{ flex: 1, overflowY: "auto" }}>
            {isLoading && (
              <div style={{ padding: "var(--sf-spacing-xl)", textAlign: "center" }}>
                <p style={{ color: "var(--sf-secondary-gray)" }}>Loading runs…</p>
              </div>
            )}
            {isError && (
              <div style={{
                padding: "var(--sf-spacing-lg)",
                margin: "var(--sf-spacing-lg)",
                background: "var(--sf-error)",
                border: "1px solid var(--sf-error-dark)",
                borderRadius: "var(--sf-radius-sm)"
              }}>
                <p style={{ color: "var(--sf-error-dark)", margin: 0 }}>
                  {(error as Error).message}
                </p>
              </div>
            )}
            {!isLoading && !isError && (
              <RunTable runs={sortedRuns} onSelect={setSelected} selectedId={selected?.id} />
            )}
          </div>
        </div>

        {selected && (
          <div style={{
            width: "480px",
            background: "var(--sf-white)",
            borderRadius: "var(--sf-radius-md)",
            boxShadow: "var(--sf-shadow-md)",
            overflow: "hidden",
            display: "flex",
            flexDirection: "column"
          }}>
            <RunDetailPanel run={detail ?? null} />
          </div>
        )}
      </div>
    </div>
  );
}

export default function App() {
  return <Dashboard />;
}
