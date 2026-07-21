const header=document.querySelector('.site-header');
const button=document.querySelector('.menu');
const nav=document.querySelector('#primary-nav');

if(header&&button&&nav){
  button.addEventListener('click',()=>{
    const open=header.classList.toggle('open');
    button.setAttribute('aria-expanded',String(open));
    button.textContent=open?'×':'☰';
  });

  nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
    header.classList.remove('open');
    button.setAttribute('aria-expanded','false');
    button.textContent='☰';
  }));
}
