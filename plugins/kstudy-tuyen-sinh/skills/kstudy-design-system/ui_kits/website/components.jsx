/* Kstudy website — section components. Exported to window at end. */
const { useState, useEffect, useRef } = React;

function Icon({ name, style }) {
  return <i data-lucide={name} style={style}></i>;
}

const NAV = [
  ['Khóa học', '#features'],
  ['Lộ trình', '#curriculum'],
  ['Giảng viên', '#mentors'],
  ['Học viên', '#stories'],
];

function NavBar({ onEnroll }) {
  const [open, setOpen] = useState(false);
  return (
    <header className="nav">
      <div className="container nav-inner">
        <a href="#top"><img className="nav-logo" src="../../assets/kstudy-logo-full.png" alt="Kstudy" /></a>
        <nav className="nav-links">
          {NAV.map(([l, h]) => <a key={l} href={h}>{l}</a>)}
        </nav>
        <div className="nav-right">
          <button className="btn btn-primary" onClick={onEnroll}>Đăng ký tư vấn</button>
          <button className="burger" onClick={() => setOpen(o => !o)} aria-label="Menu">
            <Icon name={open ? 'x' : 'menu'} />
          </button>
        </div>
      </div>
      {open && (
        <div className="container" style={{ paddingBottom: 18, display: 'flex', flexDirection: 'column', gap: 14 }}>
          {NAV.map(([l, h]) => <a key={l} href={h} onClick={() => setOpen(false)}
            style={{ fontFamily: 'var(--font-sans)', fontWeight: 500, color: 'var(--slate-700)', padding: '6px 0' }}>{l}</a>)}
          <button className="btn btn-primary" style={{ alignSelf: 'flex-start' }} onClick={() => { setOpen(false); onEnroll(); }}>Đăng ký tư vấn</button>
        </div>
      )}
    </header>
  );
}

function Hero({ onEnroll }) {
  return (
    <section className="hero" id="top">
      <div className="hero-grid"></div>
      <div className="orb" style={{ width: 14, height: 14, background: 'var(--yellow-500)', left: '46%', top: 120 }}></div>
      <div className="container hero-inner">
        <div>
          <span className="chip chip-glass"><span className="dot"></span> Lộ trình 2026</span>
          <h1>Đào tạo <span className="hl">AI &amp; Automation</span><br />Marketing thực chiến</h1>
          <p className="lead">Học bằng case study thật. Làm chủ công cụ AI, dựng quy trình tự động và tăng trưởng có thể chứng minh trên CV của bạn.</p>
          <div className="hero-cta">
            <button className="btn btn-yellow btn-lg" onClick={onEnroll}><Icon name="calendar-check" /> Đăng ký tư vấn</button>
            <a className="btn btn-ghost-d btn-lg" href="#curriculum">Xem lộ trình <Icon name="arrow-right" /></a>
          </div>
          <div className="hero-stats">
            <div className="hero-stat"><div className="fig">1.200+</div><div className="cap">học viên tốt nghiệp</div></div>
            <div className="hero-stat"><div className="fig">8</div><div className="cap">tuần thực chiến</div></div>
            <div className="hero-stat"><div className="fig">+200%</div><div className="cap">reach trung bình</div></div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="orb" style={{ position: 'absolute', width: 360, height: 360, background: 'var(--grad-brand)', borderRadius: '50%' }}></div>
          <div className="orb" style={{ position: 'absolute', width: 460, height: 460, border: '2px solid rgba(255,255,255,.14)', borderRadius: '50%' }}></div>
          <img src="../../assets/kstudy-icon-white.png" alt="" style={{ width: 150, position: 'relative', zIndex: 2, opacity: .96 }} />
        </div>
      </div>
    </section>
  );
}

const FEATURES = [
  ['brain-circuit', 'ibadge-blue', 'Tư duy AI-first', 'Biết khi nào — và khi nào không — nên dùng AI trong quy trình marketing.'],
  ['workflow', 'ibadge-grad', 'Dựng Automation', 'Kết nối tool, dữ liệu và nội dung thành quy trình chạy tự động 24/7.'],
  ['trending-up', 'ibadge-yellow', 'Tăng trưởng đo được', 'Đặt mục tiêu, đo chỉ số và tối ưu chiến dịch dựa trên dữ liệu thật.'],
];

function Features() {
  return (
    <section className="section" id="features">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">Kết quả khoá học</span>
          <h2 className="h1">Bạn sẽ làm chủ được gì?</h2>
        </div>
        <div className="grid-3">
          {FEATURES.map(([ic, cls, h, p]) => (
            <div className="fcard" key={h}>
              <div className={'ibadge ' + cls}><Icon name={ic} /></div>
              <h3>{h}</h3>
              <p className="body">{p}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const WEEKS = [
  ['01', 'Tuần 1–2', 'Nền tảng AI', 'Hiểu mô hình, prompt & bộ công cụ cốt lõi.'],
  ['02', 'Tuần 3–4', 'Nội dung & kênh', 'Sản xuất nội dung đa kênh với AI.'],
  ['03', 'Tuần 5–6', 'Automation', 'Dựng quy trình tự động end-to-end.'],
  ['04', 'Tuần 7–8', 'Dự án tốt nghiệp', 'Chạy chiến dịch thật & lên portfolio.'],
];

function Curriculum() {
  return (
    <section className="section" id="curriculum" style={{ background: 'var(--surface-2)' }}>
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">Lộ trình 8 tuần</span>
          <h2 className="h1">Từ nền tảng đến thực chiến</h2>
        </div>
        <div className="curr">
          {WEEKS.map(([no, wk, h, p]) => (
            <div className="ccard" key={no}>
              <span className="no">{no}</span>
              <span className="wk">{wk}</span>
              <h3>{h}</h3>
              <p className="body">{p}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function StatsBand() {
  return (
    <section className="band">
      <div className="orb" style={{ width: 520, height: 520, background: 'var(--grad-brand)', left: '50%', top: '50%', transform: 'translate(-50%,-50%)', filter: 'blur(70px)', opacity: .4 }}></div>
      <div className="container band-inner">
        {[['1.200+', 'học viên đã tốt nghiệp'], ['8', 'tuần lộ trình thực chiến'], ['+200%', 'reach trung bình sau khoá']].map(([f, c]) => (
          <div className="band-stat" key={c}><div className="fig">{f}</div><div className="cap">{c}</div></div>
        ))}
      </div>
    </section>
  );
}

const STORIES = [
  ['Sau 8 tuần ở Kstudy, mình tự dựng được quy trình content chạy tự động — và đi phỏng vấn với một portfolio thật.', 'NM', 'Nguyễn Minh Anh', 'Học viên K12 · Content Lead'],
  ['Khoá học rất thực chiến. Mình áp dụng automation ngay vào công việc và tiết kiệm được hàng giờ mỗi ngày.', 'TH', 'Trần Thu Hương', 'Học viên K10 · Marketer'],
  ['Giảng viên là người đang làm nghề nên mọi case study đều sát thực tế. Đáng giá từng đồng.', 'LD', 'Lê Đức', 'Học viên K11 · Founder'],
];

function Testimonials() {
  return (
    <section className="section" id="stories">
      <div className="container">
        <div className="section-head center">
          <span className="eyebrow">Học viên nói gì</span>
          <h2 className="h1">Kết quả thật, người thật</h2>
        </div>
        <div className="tgrid">
          {STORIES.map(([q, in_, nm, rl]) => (
            <div className="tcard" key={nm}>
              <p className="quote">“{q}”</p>
              <div className="who">
                <div className="av" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'var(--font-display)', fontWeight: 700, color: 'var(--blue-600)', fontSize: 18 }}>{in_}</div>
                <div><div className="nm">{nm}</div><div className="rl">{rl}</div></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTASection({ onEnroll }) {
  return (
    <section className="section" id="mentors">
      <div className="container">
        <div className="cta">
          <div className="orb" style={{ width: 520, height: 520, right: -160, bottom: -200, background: 'var(--grad-brand)', opacity: .5, filter: 'blur(30px)' }}></div>
          <span className="chip chip-glass" style={{ position: 'relative' }}><span className="dot"></span> Tư vấn miễn phí</span>
          <h2>Sẵn sàng bắt đầu hành trình <span className="hl">AI</span> của bạn?</h2>
          <p className="lead">Đăng ký tư vấn miễn phí — nhận lộ trình học cá nhân hoá cho mục tiêu của bạn.</p>
          <div className="cta-btns">
            <button className="btn btn-yellow btn-lg" onClick={onEnroll}><Icon name="calendar-check" /> Đăng ký tư vấn</button>
            <a className="btn btn-ghost-d btn-lg" href="#features">Tìm hiểu thêm</a>
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  const cols = [
    ['Khoá học', ['AI Marketing', 'Automation', 'Content & Social', 'Growth']],
    ['Học viện', ['Về Kstudy', 'Giảng viên', 'Blog', 'Tuyển dụng']],
    ['Hỗ trợ', ['Liên hệ', 'Câu hỏi thường gặp', 'Điều khoản', 'Bảo mật']],
  ];
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-top">
          <div>
            <img className="footer-logo" src="../../assets/kstudy-logo-white.png" alt="Kstudy" />
            <p className="body" style={{ color: 'var(--fg-on-dark-2)', maxWidth: 280 }}>Học viện đào tạo AI &amp; Automation Marketing — học bằng case study thực chiến.</p>
          </div>
          {cols.map(([h, items]) => (
            <div key={h}><h4>{h}</h4><ul>{items.map(i => <li key={i}><a href="#">{i}</a></li>)}</ul></div>
          ))}
        </div>
        <div className="footer-bottom">
          <span>© 2026 Học viện Kstudy · www.kstudy.edu.vn</span>
          <div className="socials">
            {[['globe', 'Website'], ['mail', 'Email'], ['phone', 'Hotline'], ['send', 'Zalo']].map(([s, lbl]) => <a key={s} href="#" aria-label={lbl}><Icon name={s} /></a>)}
          </div>
        </div>
      </div>
    </footer>
  );
}

function EnrollModal({ open, onClose }) {
  const [done, setDone] = useState(false);
  if (!open) return null;
  return (
    <div className="modal-bg" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="x" onClick={onClose}><Icon name="x" /></button>
        <span className="eyebrow">Tư vấn miễn phí</span>
        <h3>Đăng ký tư vấn</h3>
        <p className="body" style={{ margin: '6px 0 0' }}>Để lại thông tin, đội ngũ Kstudy sẽ liên hệ trong 24h.</p>
        <form onSubmit={e => { e.preventDefault(); setDone(true); setTimeout(onClose, 1400); }}>
          <label className="field"><span>Họ và tên</span><input required placeholder="Nguyễn Văn A" /></label>
          <label className="field"><span>Số điện thoại</span><input required placeholder="09xx xxx xxx" /></label>
          <label className="field"><span>Email</span><input type="email" required placeholder="ban@email.com" /></label>
          <button className="btn btn-primary btn-lg" style={{ width: '100%', justifyContent: 'center', marginTop: 24 }} type="submit">
            {done ? 'Đã gửi ✓' : 'Gửi đăng ký'}
          </button>
        </form>
      </div>
    </div>
  );
}

Object.assign(window, { NavBar, Hero, Features, Curriculum, StatsBand, Testimonials, CTASection, Footer, EnrollModal, Icon });
