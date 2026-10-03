(function(){
 var lb=document.getElementById('lb'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('p');
 function show(src,cap){lbImg.src=src;lbImg.alt=cap;lbCap.textContent=cap;if(typeof lb.showModal==='function'){lb.showModal();}else{lb.setAttribute('open','');}}
 document.querySelectorAll('.open,.zoom').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.src,b.dataset.cap);});});
 lb.querySelector('.close').addEventListener('click',function(){lb.close();});
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lbImg){lb.close();}});
 lb.addEventListener('close',function(){lbImg.src='';});
 var burger=document.querySelector('.burger'),menu=document.getElementById('menu');
 burger.addEventListener('click',function(){var o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o?'true':'false');});
 menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){menu.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
 var links=menu.querySelectorAll('a');
 var secs=Array.prototype.map.call(links,function(a){return document.querySelector(a.getAttribute('href'));});
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);});}});},{rootMargin:'-40% 0px -50% 0px'});secs.forEach(function(s){if(s)io.observe(s);});}
 document.querySelectorAll('.slider').forEach(function(sl){
  var ul=sl.querySelector('.slides'),slides=ul.querySelectorAll('.slide'),dots=sl.querySelectorAll('.dots button'),prev=sl.querySelector('.prev'),next=sl.querySelector('.next'),n=slides.length,i=0;
  function go(k){i=Math.max(0,Math.min(n-1,k));ul.scrollTo({left:slides[i].offsetLeft-ul.offsetLeft,behavior:'smooth'});}
  function paint(){dots.forEach(function(d,k){d.classList.toggle('on',k===i);});prev.disabled=(i===0);next.disabled=(i===n-1);}
  prev.addEventListener('click',function(){go(i-1);});next.addEventListener('click',function(){go(i+1);});
  dots.forEach(function(d,k){d.addEventListener('click',function(){go(k);});});
  ul.addEventListener('scroll',function(){var w=ul.clientWidth;var k=Math.round(ul.scrollLeft/w);if(k!==i){i=k;paint();}});
  sl.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);}if(e.key==='ArrowRight'){go(i+1);}});
  sl.tabIndex=0;paint();
 });
})();