(()=>{
  'use strict';
  const cards=Array.from(document.querySelectorAll('.creator-card'));
  const search=document.getElementById('search');
  const category=document.getElementById('category');
  const stage=document.getElementById('stage');
  const grade=document.getElementById('grade');
  const count=document.getElementById('visible-count');
  const empty=document.getElementById('empty');
  if(!search||!category||!stage)return;
  const url=new URL(window.location.href);
  const initial=url.searchParams.get('q');
  if(initial)search.value=initial;
  function filter(){
    const q=search.value.trim().toLocaleLowerCase();
    let n=0;
    for(const card of cards){
      const good=(!q||card.dataset.search.toLocaleLowerCase().includes(q))&&(!category.value||card.dataset.category===category.value)&&(!stage.value||card.dataset.stage===stage.value)&&(!grade.value||card.dataset.grade===grade.value);
      card.hidden=!good;
      if(good)n++;
    }
    count.textContent=String(n);
    empty.classList.toggle('show',n===0);
  }
  search.addEventListener('input',filter);
  category.addEventListener('change',filter);
  stage.addEventListener('change',filter);
  grade.addEventListener('change',filter);
  filter();
})();
