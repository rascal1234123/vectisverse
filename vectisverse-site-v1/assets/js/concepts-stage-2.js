
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;
  const items = document.querySelectorAll(".service,.card,.why-list li");
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if(e.isIntersecting){ e.target.classList.add("is-visible"); io.unobserve(e.target); }
    });
  },{threshold:.15});
  items.forEach((el,i)=>{
    el.style.opacity="0";
    el.style.transform="translateY(14px)";
    el.style.transition=`opacity .45s ease ${Math.min(i*45,280)}ms,transform .45s ease ${Math.min(i*45,280)}ms`;
    io.observe(el);
  });
  document.head.insertAdjacentHTML("beforeend","<style>.is-visible{opacity:1!important;transform:none!important}</style>");
})();
