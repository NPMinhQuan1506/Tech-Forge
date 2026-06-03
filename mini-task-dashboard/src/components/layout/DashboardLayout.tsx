import type { PropsWithChildren, ReactNode } from "react";

interface DashboardLayoutProps extends PropsWithChildren {
  sidebar: ReactNode;
  headerTitle: string;
  headerDescription: string;
}

export function DashboardLayout({
  sidebar,
  headerTitle,
  headerDescription,
  children,
}: DashboardLayoutProps) {
  return (
    <div className="dashboard-shell">
      <aside className="dashboard-shell__sidebar">{sidebar}</aside>

      <div className="dashboard-shell__main">
        <header className="topbar">
          <div>
            <p className="topbar__eyebrow">Week 1 / Day 1</p>
            <h1>{headerTitle}</h1>
            <p className="topbar__description">{headerDescription}</p>
          </div>

          <div className="topbar__summary">
            <div className="metric-card">
              <span>Typed Task Model</span>
              <strong>Ready</strong>
            </div>
            <div className="metric-card">
              <span>SCSS Layout</span>
              <strong>Ready</strong>
            </div>
          </div>
        </header>

        <main className="dashboard-shell__content">{children}</main>
      </div>
    </div>
  );
}
