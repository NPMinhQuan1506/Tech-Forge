import type { Task } from "../../types/task";

interface TaskSummaryProps {
  tasks: Task[];
}

export function TaskSummary({ tasks }: TaskSummaryProps) {
  const totalTasks = tasks.length;
  const totalCompleted = tasks.filter((task) => task.status === "done").length;
  const totalInProgress = tasks.filter((task) => task.status === "doing").length;

  return (
    <div className="summary-grid">
      <article className="metric-card">
        <span>Total tasks</span>
        <strong>{totalTasks}</strong>
      </article>
      <article className="metric-card">
        <span>In progress</span>
        <strong>{totalInProgress}</strong>
      </article>
      <article className="metric-card">
        <span>Completed</span>
        <strong>{totalCompleted}</strong>
      </article>
    </div>
  );
}
