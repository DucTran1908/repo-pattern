# Implement plan: <Tiêu đề>

- Trạng thái: draft | approved | in-progress | done | blocked
- Mức độ: vừa | lớn — <lý do ngắn>
- Branch: <git branch>
- Ngày tạo: YYYY-MM-DD
- Spec liên quan: <SPEC-XXX hoặc không có>

## 1. Nguyên nhân
> Tóm tắt: <một câu: vì sao cần thay đổi>

- <Vấn đề / yêu cầu dẫn tới plan này>

## 2. Phương án
> Tóm tắt: <một câu: làm thế nào>

- <Cách tiếp cận được chọn, các thành phần chính>

## 3. Phạm vi
> Tóm tắt: <một câu: làm gì và không làm gì>

- Trong phạm vi: ...
- Ngoài phạm vi: ...

## 4. Tác động
> Tóm tắt: <một câu: ảnh hưởng tới ai / cái gì>

- <Người dùng, module, dữ liệu, hiệu năng, tương thích>

## 5. Lưu ý
> Tóm tắt: <một câu: rủi ro hoặc điều cần chú ý>

- <Rủi ro, giả định, phụ thuộc>

## 6. Bảng file sẽ thay đổi
> Tóm tắt: <số file thêm / sửa / xoá>

| File | Hành động | Mô tả |
|---|---|---|
| `path/to/file` | Thêm / Sửa / Xoá | ... |

## 7. Checklist to do
> Tóm tắt: <thứ tự thực hiện>

- [ ] T1. <chuẩn bị kiểm chứng cho ...: test / script đo / output mẫu / checklist> (đỏ nếu chạy được)
- [ ] T2. <thực hiện ...> (kiểm chứng đạt)
- [ ] T3. <refactor / cập nhật tài liệu>
- [ ] T4. Chạy toàn bộ kiểm chứng, đối chiếu tiêu chí nghiệm thu
- [ ] T5. Ghi session log

## 8. Tiêu chí nghiệm thu
> Tóm tắt: <một câu: khi nào coi là xong>

Phương pháp: `test` | `metric` | `output-diff` | `manual` | `review`

| ID | Tiêu chí | Phương pháp | Cách kiểm chứng |
|---|---|---|---|
| AC-1 | <tiêu chí kiểm chứng được> | test | <tên test / lệnh chạy> |
| AC-2 | ... | metric | <script, dữ liệu, ngưỡng> |
