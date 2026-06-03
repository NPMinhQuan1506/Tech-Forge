import type { Task } from "../../types/task";
import { TaskCard } from "./TaskCard";
import { TaskSummary } from "./TaskSummary";

interface TaskBoardProps {
  tasks: Task[];
}

export function TaskBoard({ tasks }: TaskBoardProps) {
  return (
    <section className="task-board">
      <div className="section-heading">
        <div>
          <p className="section-heading__eyebrow">Mini app</p>
          <h2>Task list typed sach ngay tu dau</h2>
        </div>
        <p className="section-heading__description">
          Tuan 1 chi can hien thi task dung kieu, layout de doc, card ro rang.
          Day la nen mong cho form, filter, search o cac buoi sau.
        </p>
      </div>

      <TaskSummary tasks={tasks} />

      <div className="task-board__list">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </section>
  );
}
