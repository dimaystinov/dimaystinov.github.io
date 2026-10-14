(() => {
  const lang = document.documentElement.lang === 'en' ? 'en' : 'ru';
  const form = document.querySelector('.filters');
  const year = document.querySelector('#year');
  const place = document.querySelector('#place');
  const search = document.querySelector('#search');
  const groups = [...document.querySelectorAll('.year-group')];
  const count = document.querySelector('#count');
  function filter() {
    const query = search.value.trim().toLocaleLowerCase(lang);
    let total = 0;
    groups.forEach(group => {
      let visible = 0;
      group.querySelectorAll('tbody tr').forEach(row => {
        const match = (year.value === 'all' || group.dataset.year === year.value)
          && (place.value === 'all' || row.dataset.place === place.value)
          && row.textContent.toLocaleLowerCase(lang).includes(query);
        row.hidden = !match;
        if (match) visible++;
      });
      group.hidden = visible === 0;
      total += visible;
    });
    count.textContent = lang === 'en' ? `Results shown: ${total}` : `Показано записей: ${total}`;
    document.querySelector('#empty').hidden = total !== 0;
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', filter);
  form.addEventListener('change', filter);
  form.addEventListener('reset', () => setTimeout(filter, 0));
  filter();
})();
document.querySelectorAll('.year-detail').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('#full-register').open = true;
    document.querySelector('#year').value = link.dataset.year;
    document.querySelector('#place').value = 'all';
    document.querySelector('#search').value = '';
    document.querySelector('#year').dispatchEvent(new Event('change', {bubbles:true}));
  });
});

document.querySelectorAll(".language-switch").forEach(link => {
  link.addEventListener("click", () => { link.href = link.getAttribute("href").split("#")[0] + location.hash; });
});
