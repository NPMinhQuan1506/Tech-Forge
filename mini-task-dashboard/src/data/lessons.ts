interface LessonNote {
  title: string;
  description: string;
  code: string;
}

export const taskLessons: LessonNote[] = [
  {
    title: "Type co ban va union type",
    description:
      "Status chi duoc nam trong ba gia tri todo, doing, done. Day la union type rat thuc dung.",
    code: `export type TaskStatus = "todo" | "doing" | "done";`,
  },
  {
    title: "Interface mo ta model task",
    description:
      "Task la hop dong du lieu cua app. React component nao nhan task deu doc theo cung mot khuon dang.",
    code: `export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  createdAt: Date;
}`,
  },
  {
    title: "Array type va function typing",
    description:
      "TaskBoard nhan Task[] va TaskCard nhan Task. Ban se quen voi typed props rat som.",
    code: `interface TaskBoardProps {
  tasks: Task[];
}`,
  },
];

export const styleLessons: LessonNote[] = [
  {
    title: "SCSS variables",
    description:
      "Mau, spacing, radius duoc dat o abstracts de dung lai nhieu noi, giam hard-code.",
    code: `$color-accent: #2563eb;
$space-lg: 24px;
$radius-lg: 20px;`,
  },
  {
    title: "Nesting co kiem soat",
    description:
      "Class con cua card duoc viet trong context cua component, de doc ma van khong bi qua sau.",
    code: `.task-card {
  &__title {
    font-weight: 700;
  }
}`,
  },
  {
    title: "Flex layout",
    description:
      "Header, sidebar, card meta va status pill deu dang dung flex de canh hang va canh truc.",
    code: `.task-card__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}`,
  },
];

export type { LessonNote };
