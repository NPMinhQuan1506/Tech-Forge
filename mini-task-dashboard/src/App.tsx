import { DashboardLayout } from "./components/layout/DashboardLayout";
import { LessonPanel } from "./components/panels/LessonPanel";
import { Sidebar } from "./components/panels/Sidebar";
import { TaskBoard } from "./components/tasks/TaskBoard";
import { taskLessons, styleLessons } from "./data/lessons";
import { sampleTasks } from "./data/tasks";

function App() {
  return (
    <DashboardLayout
      sidebar={<Sidebar />}
      headerTitle="Mini Task Dashboard"
      headerDescription="Day 1: type, interface, union, SCSS variables, nesting, flex"
    >
      <TaskBoard tasks={sampleTasks} />
      <LessonPanel
        title="TypeScript dang ap dung o dau?"
        description="Day 1 khong hoc rieng ly thuyet. Moi concept deu dang song trong app nay."
        lessons={taskLessons}
      />
      <LessonPanel
        title="SCSS dang ap dung o dau?"
        description="Ban doc style source se thay variables, nesting va flex dang phuc vu layout that."
        lessons={styleLessons}
      />
    </DashboardLayout>
  );
}

export default App;
