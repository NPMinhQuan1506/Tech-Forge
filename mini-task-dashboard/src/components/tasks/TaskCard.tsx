import type { TaskStatus, Task } from "../../types/task";

interface TaskCardProps {
  task: Task;
}

const statusLabelMap: Record<TaskStatus, string> = {
  todo: "Todo",
  doing: "Doing",
  done: "Done",
};

export function TaskCard({ task }: TaskCardProps) {
  return (
    <article className="task-card">
      <div className="task-card__meta">
        <span className={`status-pill status-pill--${task.status}`}>
          {statusLabelMap[task.status]}
        </span>
        <time dateTime={task.createdAt.toISOString()}>
          {task.createdAt.toLocaleDateString("vi-VN")}
        </time>
      </div>

      <h3 className="task-card__title">{task.title}</h3>

      <p className="task-card__description">
        {task.description ?? "Task nay chua co mo ta."}
      </p>
    </article>
  );
}
