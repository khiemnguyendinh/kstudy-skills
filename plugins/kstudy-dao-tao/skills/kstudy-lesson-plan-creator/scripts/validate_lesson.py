#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA tu dong cho lesson plan Kstudy.

Cach dung:
  python validate_lesson.py --fingerprint course.json
      -> in 12 ky tu dau SHA-256 cua course.json (ghi vao lesson.json.course_fingerprint)
  python validate_lesson.py lesson.json course.json [--slide Slide-outline.md] [--video Video-outline.md]
      -> kiem tra, in PASS/WARN/FAIL; exit 1 neu co FAIL.
"""
import argparse, hashlib, json, os, re, sys, unicodedata

FAILS, WARNS, PASSES = [], [], []
def fail(m): FAILS.append(m)
def warn(m): WARNS.append(m)
def ok(m): PASSES.append(m)

def fingerprint(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:12]

def norm(s):
    s = unicodedata.normalize('NFC', str(s)).lower()
    return re.sub(r'[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]', ' ', s)

STOPWORDS = set('''va và của cho các một những trong với được là có không này đó khi để từ trên theo sau
như bằng bài buổi phút học viên người dùng cách thực hành nội dung phần video slide the and for with'''.split())

def tokens(s):
    return {w for w in norm(s).split() if len(w) >= 4 and w not in STOPWORDS}

def walk_strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f'{path}[{i}]')
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f'{path}.{k}' if path else k)

def parse_minutes(cell):
    if isinstance(cell, (int, float)):
        return int(cell)
    nums = [int(n) for n in re.findall(r'\d+', str(cell))]
    if not nums:
        return 0
    if len(nums) >= 2 and re.search(r'\d\s*[–\-—]\s*\d', str(cell)):
        return nums[1] - nums[0]   # dang khoang "0-10"
    return nums[0]

BANNED_COLLOQUIAL = ['chốt']
BANNED_ENGLISH = ['deadline', 'feedback', 'mindset', 'teamwork', 'workflow', 'checklist']
VAGUE_VERBS = ['nắm vững', 'nắm được', 'hiểu được', 'hiểu rõ', 'biết được']

def lint_text(text, label):
    low = norm(text)
    hits = []
    for w in BANNED_COLLOQUIAL + BANNED_ENGLISH:
        if re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', low):
            hits.append(w)
    if hits:
        warn(f'Wording ({label}): gặp từ nên tránh: {", ".join(sorted(set(hits)))} — thay bằng từ tiếng Việt/trang trọng hơn.')

APPROVALS = {'PROPOSED', 'APPROVED', 'REJECTED', 'NEEDS_INPUT', 'DEFERRED', 'SUPERSEDED'}
ZONES = {'classroom', 'e_learning', 'ai_mentor', 'internet'}
MILLER = {'KNOWS', 'KNOWS_HOW', 'SHOWS_HOW', 'DOES'}
TRACE_KEYS = ('job_task_ids', 'competency_ids', 'plo_ids', 'clo_ids',
              'lesson_outcome_ids', 'evidence_ids', 'rubric_ids', 'resource_ids')


def check_traceability(lesson, ready):
    """Kiểm cấu trúc traceability/activity/formative/UDL/resource của lesson.json.

    `ready=True` (cờ --ready) nâng các cảnh báo READY_FOR_PILOT thành FAIL: dùng khi
    chốt buổi để bàn giao pilot, không dùng cho vòng nháp.
    """
    hard = fail if ready else warn

    trace = lesson.get('traceability')
    if not isinstance(trace, dict):
        hard('traceability rỗng — buổi chưa nối được về JT/COMP/PLO/CLO/evidence/rubric/resource.')
        trace = {}
    else:
        if trace.get('approval_status') not in APPROVALS:
            fail(f'traceability.approval_status không hợp lệ (hợp lệ: {sorted(APPROVALS)}).')
        for key in TRACE_KEYS:
            if not isinstance(trace.get(key), list) or not trace.get(key):
                hard(f'traceability.{key} rỗng.')
        ok('traceability có mặt.')

    def check_refs(values, key, label):
        pool = trace.get(key) if isinstance(trace.get(key), list) else []
        if pool and isinstance(values, list):
            unknown = sorted(set(values) - set(pool))
            if unknown:
                fail(f'{label} tham chiếu {key} không khai báo: {", ".join(unknown)}')

    miller = lesson.get('miller_level')
    if miller and miller not in MILLER:
        fail(f'miller_level phải thuộc {sorted(MILLER)}.')
    elif not miller:
        warn('miller_level thiếu — chưa xác định mức Miller-adapted của buổi.')

    activity_map = lesson.get('activity_map') or []
    if not isinstance(activity_map, list):
        fail('activity_map phải là array.')
    elif activity_map:
        seen = set()
        for i, act in enumerate(activity_map):
            if not isinstance(act, dict):
                fail(f'activity_map[{i}] phải là object.')
                continue
            aid = act.get('activity_id')
            if not aid or aid in seen:
                fail(f'activity_map[{i}] cần activity_id duy nhất.')
            if aid:
                seen.add(aid)
                check_refs([aid], 'activity_ids', f'activity_map[{i}]')
            if act.get('zone') not in ZONES:
                fail(f'activity_map[{i}] zone không hợp lệ (hợp lệ: {sorted(ZONES)}).')
            if not act.get('lesson_outcome_ids'):
                fail(f'activity_map[{i}] cần lesson_outcome_ids.')
            check_refs(act.get('lesson_outcome_ids') or [], 'lesson_outcome_ids', f'activity_map[{i}]')
            check_refs(act.get('evidence_ids') or [], 'evidence_ids', f'activity_map[{i}]')
            d = act.get('duration_min')
            if d is not None and (not isinstance(d, (int, float)) or d < 0):
                fail(f'activity_map[{i}] duration_min phải >= 0.')
        ok(f'activity_map: {len(activity_map)} hoạt động.')
    else:
        hard('activity_map thiếu — chưa map hoạt động về outcome/evidence theo learning zone.')
    if ready and not trace.get('activity_ids'):
        fail('READY_FOR_PILOT cần traceability.activity_ids.')

    checks = lesson.get('formative_checks') or []
    if not isinstance(checks, list):
        fail('formative_checks phải là array.')
    elif checks:
        seen_checks = set()
        for i, chk in enumerate(checks):
            if not isinstance(chk, dict):
                fail(f'formative_checks[{i}] phải là object.')
                continue
            cid = chk.get('check_id')
            if not cid or cid in seen_checks:
                fail(f'formative_checks[{i}] cần check_id duy nhất.')
            if cid:
                seen_checks.add(cid)
            if not chk.get('target_outcome_ids'):
                fail(f'formative_checks[{i}] cần target_outcome_ids.')
            check_refs(chk.get('target_outcome_ids') or [], 'lesson_outcome_ids', f'formative_checks[{i}]')
            if not chk.get('feedback_action'):
                fail(f'formative_checks[{i}] cần feedback_action.')
        ok(f'formative_checks: {len(checks)} mục.')
    else:
        hard('formative_checks thiếu — buổi chưa có điểm kiểm tra hình thành và hành động phản hồi.')

    udl = lesson.get('udl_options')
    if udl is not None and (not isinstance(udl, dict)
                            or not any(udl.get(k) for k in ('representation', 'action_expression', 'engagement'))):
        warn('udl_options rỗng — bỏ field hoặc điền phương án thật sự dùng được.')

    for i, res in enumerate(lesson.get('resource_map') or []):
        if not isinstance(res, dict) or not res.get('resource_id'):
            fail(f'resource_map[{i}] cần resource_id.')
            continue
        check_refs([res['resource_id']], 'resource_ids', f'resource_map[{i}]')
        url = str(res.get('url') or '')
        if url and not (url.startswith('http://') or url.startswith('https://') or url.startswith('[CHỜ')):
            fail(f'resource_map[{i}] URL không hợp lệ và không phải placeholder [CHỜ...].')

    for i, row in enumerate(lesson.get('online_resources') or []):
        if not isinstance(row, list) or len(row) < 3:
            fail(f'online_resources[{i}] phải gồm tên, mục đích dùng và URL.')
            continue
        url = str(row[2] or '')
        if url and not (url.startswith('http://') or url.startswith('https://') or url.startswith('[CHỜ')):
            fail(f'online_resources[{i}] URL không hợp lệ và không phải placeholder [CHỜ...].')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson', nargs='?')
    ap.add_argument('course', nargs='?')
    ap.add_argument('--slide'); ap.add_argument('--video'); ap.add_argument('--seed')
    ap.add_argument('--fingerprint', metavar='COURSE_JSON')
    ap.add_argument('--ready', action='store_true',
                    help='nâng cảnh báo traceability/activity/formative thành FAIL (gate READY_FOR_PILOT)')
    a = ap.parse_args()

    if a.fingerprint:
        print(fingerprint(a.fingerprint)); return 0
    if not (a.lesson and a.course):
        ap.error('cần lesson.json và course.json (hoặc --fingerprint course.json)')

    lesson = json.load(open(a.lesson, encoding='utf-8'))
    course = json.load(open(a.course, encoding='utf-8'))

    # 1. Gate approved + schema
    if course.get('approved') is True:
        ok('course.json approved=true')
    else:
        fail('course.json chưa approved=true — syllabus chưa đóng dấu duyệt, không sản xuất học liệu.')
    if course.get('schema_version') != 2:
        warn(f'course.json schema_version={course.get("schema_version")!r} (kỳ vọng 2) — kiểm tra map field thủ công.')

    # 2. Fingerprint / cascade
    fp = fingerprint(a.course)
    lfp = lesson.get('course_fingerprint')
    if not lfp:
        warn(f'lesson.json thiếu course_fingerprint — thêm "{fp}" sau khi xác nhận nội dung khớp syllabus hiện tại.')
    elif lfp != fp:
        chg = course.get('changelog') or []
        last = '; '.join(f"v{c.get('version')} {c.get('date')}: {c.get('summary')}" for c in chg[-3:]) or '(course.json không có changelog)'
        warn(f'CASCADE: course.json đã đổi sau khi soạn buổi này (fingerprint {lfp} ≠ {fp}). Changelog gần nhất: {last}. Rà lại buổi rồi cập nhật fingerprint.')
    else:
        ok('fingerprint khớp — syllabus không đổi từ khi soạn buổi.')

    # 2b. Lesson seed audit (optional, backward-compatible)
    seed_file = a.seed or lesson.get('lesson_seed_file')
    if seed_file:
        seed_path = seed_file if os.path.isabs(seed_file) else os.path.join(os.path.dirname(os.path.abspath(a.lesson)), seed_file)
        if not os.path.exists(seed_path):
            warn(f'lesson_seed_file không tồn tại: {seed_file}')
        else:
            seed = json.load(open(seed_path, encoding='utf-8'))
            if seed.get('course_fingerprint') == fp:
                ok('lesson_seed.json fingerprint khớp course.json hiện tại.')
            else:
                warn(f'lesson_seed.json fingerprint {seed.get("course_fingerprint")} ≠ course.json {fp} — sinh lại seed trước khi rà lesson.')
            if seed.get('buoi') != lesson.get('buoi'):
                warn(f'lesson_seed.json buoi={seed.get("buoi")} khác lesson.json buoi={lesson.get("buoi")}.')
    else:
        warn('lesson.json chưa khai báo lesson_seed_file — khuyến nghị sinh/ghi seed để audit nguồn đầu vào buổi.')

    # 3. Timeline
    dur = lesson.get('duration_min', 0)
    tl = lesson.get('timeline') or []
    total = sum(parse_minutes(row[0]) for row in tl if row)
    if total == dur and dur > 0:
        ok(f'Tiến trình cộng đúng {dur} phút.')
    else:
        fail(f'Tiến trình cộng {total} phút ≠ duration_min {dur}.')

    # 4. Bài trong buổi + gate
    buoi = lesson.get('buoi')
    sl = [l for l in course.get('lessons', []) if l.get('session_idx') == buoi]
    if not sl:
        warn(f'Không tìm thấy bài nào trong course.json có session_idx={buoi} — kiểm tra trường covers/buoi.')
    gates = lesson.get('gate') or []
    if not gates:
        fail('lesson.json gate rỗng — gate buổi phải gộp từ gate các bài trong course.json.')
    else:
        n_gate = sum(1 for l in sl if l.get('gate'))
        if n_gate > len(gates):
            warn(f'Buổi phủ {n_gate} bài có gate nhưng lesson.json chỉ có {len(gates)} gate — kiểm tra gộp đủ chưa.')
        else:
            ok(f'Gate buổi: {len(gates)} mục (các bài có gate: {n_gate}).')

    # 5. Độ phủ objectives
    corpus_parts = [json.dumps(lesson, ensure_ascii=False)]
    for pth in (a.slide, a.video):
        if pth:
            corpus_parts.append(open(pth, encoding='utf-8').read())
    corpus_tokens = tokens(' '.join(corpus_parts))
    uncovered = []
    for l in sl:
        objs = l.get('objectives') or ''
        items = [x.strip() for x in re.split(r'\d+\)\s*|;', objs) if len(x.strip()) > 8]
        for it in items:
            tk = tokens(it)
            if tk and len(tk & corpus_tokens) / len(tk) < 0.35:
                uncovered.append(f"[{l.get('title','?')}] {it[:80]}")
    if uncovered:
        warn('Objectives có thể CHƯA được phủ trong học liệu buổi (kiểm tay):\n    - ' + '\n    - '.join(uncovered))
    else:
        ok('Mọi objective của các bài trong buổi đều xuất hiện trong học liệu (đối chiếu từ khóa).')

    # 5b. Traceability / activity map / formative / resource
    check_traceability(lesson, a.ready)

    # 6. KASH
    kash = lesson.get('kash') or []
    groups = norm(' '.join(str(r[0]) for r in kash if r))
    missing = [g for g in ['kiến thức', 'kỹ năng', 'thái độ', 'thói quen'] if g not in groups]
    if missing:
        warn('KASH thiếu nhóm: ' + ', '.join(missing))
    else:
        ok('KASH đủ 4 nhóm.')
    kash_txt = norm(json.dumps(kash, ensure_ascii=False) + json.dumps(lesson.get('exercises', []), ensure_ascii=False))
    vague = [v for v in VAGUE_VERBS if v in kash_txt]
    if vague:
        warn('KASH/bài tập dùng động từ không đo được: ' + ', '.join(vague) + ' — thay bằng động từ Bloom đo được.')

    # 7. Wording linter toàn lesson.json
    for pth_label, txt in walk_strings(lesson):
        lint_text(txt, pth_label)

    # 8. Slide outline
    if a.slide:
        smd = open(a.slide, encoding='utf-8').read()
        blocks = re.split(r'(?=^\*\*Slide\s)', smd, flags=re.M)
        slides = [b for b in blocks if b.startswith('**Slide')]
        if not slides:
            warn('Slide outline: không nhận diện được block "**Slide N —" — kiểm tra đúng template chưa.')
        else:
            miss = [re.match(r'\*\*(Slide[^*—-]*)', b).group(1).strip() for b in slides if 'Minh họa' not in b]
            if miss:
                fail('Slide thiếu dòng "Minh họa": ' + ', '.join(miss))
            else:
                ok(f'{len(slides)} slide đều có dòng Minh họa.')
            long_titles = []
            missing_job = []
            weak_visual = []
            visual_terms = [
                'ảnh kstudy', 'ảnh thật', 'ảnh chụp màn hình', 'screenshot', 'sơ đồ', 'biểu đồ',
                'timeline', 'ma trận', 'bảng so sánh', 'concept map', 'ảnh public',
                'ảnh tạo bằng trí tuệ nhân tạo', 'ai-generated', 'họa tiết', 'icon'
            ]
            for b in slides:
                heading = re.match(r'\*\*Slide\s+\d+\s+[—-]\s*([^*\n]+)', b)
                title = heading.group(1).strip() if heading else ''
                title_clean = re.sub(r'\*\*$', '', title).strip()
                if len(title_clean) > 60 or len(title_clean.split()) > 11:
                    long_titles.append(title_clean[:80])
                if 'Visual job' not in b:
                    missing_job.append(title_clean or 'không rõ tiêu đề')
                minh = re.search(r'Minh họa\s*:\s*(.+)', b, flags=re.I)
                if minh and not any(term in minh.group(1).lower() for term in visual_terms):
                    weak_visual.append(title_clean or 'không rõ tiêu đề')
            if long_titles:
                warn('Slide title dài, KSD khó dàn trang (nên ≤48 ký tự thường, ≤60 cover/section): ' + '; '.join(long_titles))
            if missing_job:
                warn('Slide thiếu "Visual job" (Proof/Thinking/Doing/Evidence/Context/Concept): ' + '; '.join(missing_job[:8]))
            if weak_visual:
                warn('Dòng Minh họa chưa nêu rõ loại visual cho KSD: ' + '; '.join(weak_visual[:8]))
        if 'Phong cách hình ảnh chung' not in smd:
            warn('Slide outline thiếu ghi chú "Phong cách hình ảnh chung" ở đầu file.')
        lint_text(smd, a.slide)

    # 9. Video outline
    if a.video:
        vmd = open(a.video, encoding='utf-8').read()
        vblocks = re.split(r'(?=^\*\*Video\s+\d+\.\d+)', vmd, flags=re.M)
        vids = [b for b in vblocks if re.match(r'\*\*Video\s+\d+\.\d+', b)]
        if not vids:
            warn('Video outline: không nhận diện được block "**Video X.Y" — kiểm tra đúng template chưa.')
        else:
            bad = [re.match(r'\*\*(Video\s+\d+\.\d+)', b).group(1) for b in vids
                   if 'Mục tiêu' not in b or 'Định dạng đề xuất' not in b]
            if bad:
                fail('Video thiếu "Mục tiêu" hoặc "Định dạng đề xuất": ' + ', '.join(bad))
            else:
                ok(f'{len(vids)} video đều có Mục tiêu + Định dạng đề xuất.')
            per_bai = {}
            for b in vids:
                x = re.match(r'\*\*Video\s+(\d+)\.', b).group(1)
                per_bai[x] = per_bai.get(x, 0) + 1
            off = [f'Bài {k}: {v} video' for k, v in per_bai.items() if not 3 <= v <= 6]
            if off:
                warn('Số video/bài ngoài khoảng 3–6: ' + ', '.join(off))
            if 'Cốt lõi' not in vmd or 'Mở rộng' not in vmd:
                warn('Video outline chưa phân nhãn Cốt lõi / Mở rộng.')
        lint_text(vmd, a.video)

    # In kết quả
    print('=' * 60)
    for m in PASSES: print('PASS  ' + m)
    for m in WARNS: print('WARN  ' + m)
    for m in FAILS: print('FAIL  ' + m)
    print('=' * 60)
    print(f'{len(PASSES)} PASS · {len(WARNS)} WARN · {len(FAILS)} FAIL')
    if FAILS:
        print('>> Sửa mọi FAIL trước khi trình user. WARN phải xử lý hoặc giải trình.')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
