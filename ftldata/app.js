'use strict';
(async () => {
  const grid = document.querySelector('#project-grid');
  const status = document.querySelector('#project-status');
  const make = (tag, cls, text) => { const el = document.createElement(tag); el.className = cls; el.textContent = text; return el; };
  try {
    const response = await fetch('./projects.json');
    if (!response.ok) throw new Error('load');
    const projects = await response.json();
    if (!Array.isArray(projects) || projects.some(p => !p.id || !p.name || !p.category)) throw new Error('data');
    const symbols = {learning:'↗', robotics:'◎', infrastructure:'⌘'};
    for (const project of projects) {
      const card = make('article', 'project-card', ''); card.dataset.category = project.category; card.id = project.id;
      const top = make('div', 'card-top', '');
      top.append(make('span', 'project-symbol', symbols[project.category]), make('span', 'status', project.status || 'Планируется'));
      card.append(top, make('p', 'tag', project.tag), make('h3', '', project.name), make('p', 'project-description', project.description));
      const button = make('button', 'project-action', 'Обсудить проект ↗'); button.type = 'button';
      button.addEventListener('click', () => { location.href='https://ftldata.duckdns.org/#brief'; });
      const details = make('details', 'project-details', ''); details.open = true;
      const summary = make('summary', '', 'О проекте'); details.append(summary);
      const body = make('div', 'details-body', '');
      for (const text of project.details || []) body.append(make('p', '', text));
      for (const service of project.services || []) {
        const section = make('section', 'service-detail', '');
        section.append(make('h4', '', service.name), make('p', '', service.description));
        const link = make('a', 'service-open', 'Открыть ' + service.name + ' ↗');
        link.href = service.url; link.target = '_blank'; link.rel = 'noopener noreferrer';
        section.append(link); body.append(section);
      }
      for (const clip of [...(project.video ? [project.video] : []), ...(project.videos || [])]) {
        const figure = make('figure', 'project-video' + (clip.portrait ? ' project-video-portrait' : ''), '');
        const caption = make('figcaption', '', clip.title);
        const video = make('video', '', '');
        video.controls = true; video.playsInline = true; video.preload = 'metadata';
        video.poster = clip.poster; video.setAttribute('aria-label', clip.title);
        const source = document.createElement('source'); source.src = clip.src; source.type = 'video/mp4';
        const fallback = make('a', '', 'Открыть видео'); fallback.href = clip.src;
        video.append(source, fallback); figure.append(caption, video); body.append(figure);
      }
      if (!project.services?.length) body.append(button);
      details.append(body); card.append(details);
      grid.append(card);
    }
    for (const button of document.querySelectorAll('[data-filter]')) button.addEventListener('click', () => {
      for (const other of document.querySelectorAll('[data-filter]')) other.setAttribute('aria-pressed', String(other === button));
      let count = 0;
      for (const card of grid.children) { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; if (!card.hidden) count++; }
      status.textContent = `Показано проектов: ${count}`;
    });

  } catch (error) { status.textContent = 'Не удалось загрузить проекты. Обновите страницу.'; }
})();
