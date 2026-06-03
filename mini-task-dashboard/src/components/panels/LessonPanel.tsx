import type { LessonNote } from "../../data/lessons";

interface LessonPanelProps {
  title: string;
  description: string;
  lessons: LessonNote[];
}

export function LessonPanel({
  title,
  description,
  lessons,
}: LessonPanelProps) {
  return (
    <section className="lesson-panel">
      <div className="section-heading">
        <div>
          <p className="section-heading__eyebrow">Applied learning</p>
          <h2>{title}</h2>
        </div>
        <p className="section-heading__description">{description}</p>
      </div>

      <div className="lesson-panel__grid">
        {lessons.map((lesson) => (
          <article key={lesson.title} className="lesson-card">
            <h3>{lesson.title}</h3>
            <p>{lesson.description}</p>
            <pre>
              <code>{lesson.code}</code>
            </pre>
          </article>
        ))}
      </div>
    </section>
  );
}
