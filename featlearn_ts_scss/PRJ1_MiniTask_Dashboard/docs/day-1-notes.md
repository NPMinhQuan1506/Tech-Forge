# Day 1 Notes

## Muc tieu

- Hieu `type`, `interface`, `union`
- Hieu `SCSS variables`, `nesting`, `flex`
- Gan tung concept vao mot app that

## TypeScript dang nam o dau

File: `src/types/task.ts`

```ts
export type TaskStatus = "todo" | "doing" | "done";
```

Y nghia:
- `TaskStatus` la union type
- Status khong duoc gan linh tinh
- Editor se bao loi neu viet sai `"doign"`

```ts
export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  createdAt: Date;
}
```

Y nghia:
- `interface` mo ta hinh dang task
- `description?` la optional property
- `createdAt: Date` nhac ban day la ngay, khong phai string thuong

## SCSS dang nam o dau

File: `src/styles/abstracts/_variables.scss`

```scss
$color-accent: #2563eb;
$space-lg: 24px;
$radius-lg: 24px;
```

Y nghia:
- gom token de dung lai
- doi theme sau nay de hon

File: `src/styles/components/_task-board.scss`

```scss
.task-card {
  &__meta {
    display: flex;
    justify-content: space-between;
  }
}
```

Y nghia:
- dung nesting de giu code co ngu canh
- dung flex de canh status va ngay tao

## Tu hoc tiep sau khi doc xong

1. Them 1 task moi vao `src/data/tasks.ts`
2. Doi `status` cua task va xem card doi mau
3. Xoa `description` cua 1 task de thay optional property hoat dong
