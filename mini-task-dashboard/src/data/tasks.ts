import type { Task } from "../types/task";

export const sampleTasks: Task[] = [
  {
    id: "task-01",
    title: "Dinh nghia Task type va interface",
    description: "Gan kieu ro rang cho title, status va createdAt.",
    status: "todo",
    createdAt: new Date("2026-06-03T09:00:00"),
  },
  {
    id: "task-02",
    title: "Render danh sach task bang React",
    description: "Dung array type Task[] va map de hien thi TaskCard.",
    status: "doing",
    createdAt: new Date("2026-06-03T10:30:00"),
  },
  {
    id: "task-03",
    title: "Dung SCSS variables va nesting cho card",
    description: "Tach token mau sac, radius, spacing thanh file rieng.",
    status: "done",
    createdAt: new Date("2026-06-02T14:15:00"),
  },
];
