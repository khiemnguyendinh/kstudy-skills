/* Kstudy website — app shell. Assembles sections + interactivity. */
const { useState, useEffect } = React;

function App() {
  const [enroll, setEnroll] = useState(false);
  const [toast, setToast] = useState(false);
  const openEnroll = () => setEnroll(true);

  // (re)draw Lucide icons after every render
  useEffect(() => { if (window.lucide) window.lucide.createIcons(); });

  return (
    <>
      <NavBar onEnroll={openEnroll} />
      <Hero onEnroll={openEnroll} />
      <Features />
      <Curriculum />
      <StatsBand />
      <Testimonials />
      <CTASection onEnroll={openEnroll} />
      <Footer />
      <EnrollModal open={enroll} onClose={() => { setEnroll(false); }} />
      {toast && (
        <div className="toast"><Icon name="check-circle" /> Cảm ơn bạn! Kstudy sẽ liên hệ sớm.</div>
      )}
    </>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
