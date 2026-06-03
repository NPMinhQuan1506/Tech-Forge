const roadmapItems = [
  "Task type + interface",
  "TaskCard component",
  "Layout Header / Sidebar / List",
  "SCSS variables + nesting + flex",
];

export function Sidebar() {
  return (
    <div className="sidebar-panel">
      <p className="sidebar-panel__eyebrow">Learning roadmap</p>
      <h2>Build 1 app nho de hoc that</h2>
      <p className="sidebar-panel__description">
        Muc tieu khong phai hoc het ly thuyet. Muc tieu la thay ro moi concept
        dang nam o dau trong san pham.
      </p>

      <div className="sidebar-panel__section">
        <h3>Day 1 checklist</h3>
        <ul className="sidebar-panel__list">
          {roadmapItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>

      <div className="sidebar-panel__section sidebar-panel__section--highlight">
        <h3>Task model</h3>
        <pre>
          <code>{`type TaskStatus = "todo" | "doing" | "done"

interface Task {
  id: string
  title: string
  description?: string
  status: TaskStatus
  createdAt: Date
}`}</code>
        </pre>
      </div>
    </div>
  );
}
