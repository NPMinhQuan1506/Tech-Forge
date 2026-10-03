# Tech-Forge Learning Branch

Branch nay duoc dung de hoc va thuc hanh:

- TypeScript
- SCSS / CSS
- React co type ro rang
- Cach dua tung concept vao mot app nho that

## Muc tieu cua branch nay

Khong hoc TypeScript va SCSS theo kieu chi xem tutorial.

Huong hoc o day la:

1. hoc mot concept nho
2. ap dung ngay vao app
3. sai thi sua
4. doc lai code de hieu sau hon

## Project dang dung

Repo hien tai chi giu **mot huong hoc chinh**:

- [mini-task-dashboard](./mini-task-dashboard)

Day la app demo de hoc song song:

- React + Vite
- TypeScript
- SCSS

## App demo

`mini-task-dashboard` la app nho de luyen cac bai hoc that:

- hien thi task list
- task card typed sach
- layout dashboard
- sidebar
- section notes de giai thich concept dang nam o dau trong app

Day 1 hien da co:

- `type`
- `interface`
- `union type`
- `array type`
- typed props trong React
- SCSS variables
- SCSS nesting
- flex layout

## Cau truc repo

```txt
Tech-Forge/
|- README.md
|- .gitignore
`- mini-task-dashboard/
   |- src/
   |- docs/
   |- package.json
   `- ...
```

## Cach chay project

```bash
cd mini-task-dashboard
npm install
npm run dev
```

## Cach hoc de hieu nhanh hon

Nen doc theo thu tu:

1. `mini-task-dashboard/src/types/task.ts`
2. `mini-task-dashboard/src/data/tasks.ts`
3. `mini-task-dashboard/src/components/tasks/TaskCard.tsx`
4. `mini-task-dashboard/src/styles/components/_task-board.scss`
5. `mini-task-dashboard/docs/day-1-notes.md`

## Dinh huong tiep theo

Se tiep tuc phat trien cung mot app nay theo roadmap hoc:

- Week 1: typed model + layout
- Week 2: form tao, sua, xoa task
- Week 3: filter, search, theme, responsive
- Week 4: localStorage, state polish, reusable typing
