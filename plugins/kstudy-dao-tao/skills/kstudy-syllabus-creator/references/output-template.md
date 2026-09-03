# (Đã thay thế)

Định dạng output cũ (markdown copy-block) đã được thay bằng **3 file** sinh tự động từ `course.json`:
`<mã> - kstudy import - <tên>.xlsx` · `<mã> - Kstudy template - <tên>.html` · `<mã> - Kstudy Syllabus - <tên>.docx`.

Cấu trúc `course.json` + cách map sang form/sheet: xem **`course-schema.md`**.
Sinh file: `python scripts/build_kstudy_outputs.py course.json <outdir>`.
