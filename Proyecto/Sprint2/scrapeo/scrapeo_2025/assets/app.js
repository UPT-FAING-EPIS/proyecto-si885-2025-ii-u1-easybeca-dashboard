/* Observatorio de Becas – App JS */
(function () {
  const els = {
    tabs: document.querySelectorAll('.tab'),
    panels: document.querySelectorAll('.tab-panel'),
    becaChips: document.querySelectorAll('.chip[data-beca-code]'),
    // Beca 18
    beca18Stats: document.getElementById('beca18-stats'),
    beca18TableBody: document.querySelector('#beca18-universidades tbody'),
    beca18Promedios: document.getElementById('beca18-promedios'),
    beca18Error: document.getElementById('beca18-error'),
    beca18Detalle: document.getElementById('beca18-detalle'),
    searchBeca18: document.getElementById('search-beca18'),
    filterTipoBeca18: document.getElementById('filter-tipo-beca18'),
    // Beca Tec
    becaTecInfo: document.getElementById('beca-tec-info'),
    becaTecStats: document.getElementById('beca-tec-stats'),
    becaTecTableBody: document.querySelector('#beca-tec-instituciones tbody'),
    becaTecError: document.getElementById('beca-tec-error'),
    searchBecaTec: document.getElementById('search-beca-tec'),
    filterTipoBecaTec: document.getElementById('filter-tipo-beca-tec'),
    // Beca Perú
    becaPeruInfo: document.getElementById('beca-peru-info'),
    becaPeruStats: document.getElementById('beca-peru-stats'),
    becaPeruTableBody: document.querySelector('#beca-peru-instituciones tbody'),
    becaPeruError: document.getElementById('beca-peru-error'),
    searchBecaPeru: document.getElementById('search-beca-peru'),
    filterTipoBecaPeru: document.getElementById('filter-tipo-beca-peru'),
    // Instituciones
    institucionesStats: document.getElementById('instituciones-stats'),
    institucionesTableBody: document.querySelector('#tabla-instituciones tbody'),
    institucionesError: document.getElementById('instituciones-error'),
    institucionesInfoBeca: document.getElementById('instituciones-info-beca'),
    searchInstituciones: document.getElementById('search-instituciones'),
    filterBeca: document.getElementById('filter-beca'),
    // Becas integrales
    becasStats: document.getElementById('becas-stats'),
    becasTableBody: document.querySelector('#tabla-becas tbody'),
    becasError: document.getElementById('becas-error'),
    searchBecas: document.getElementById('search-becas'),
    filterCategoria: document.getElementById('filter-categoria'),
    // Estadísticas
    statsGlobales: document.getElementById('estadisticas-globales'),
    statsBecaBody: document.querySelector('#tabla-estadisticas-beca tbody'),
    statsError: document.getElementById('estadisticas-error'),
  };

  // Simple state
  const state = {
    beca18: null,
    instituciones: null,
    integrales: null,
  };

  // Tabs behavior
  els.tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-tab');
      els.tabs.forEach(b => b.classList.remove('active'));
      els.panels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(target).classList.add('active');
    });
  });

  // Quick filters for Instituciones by beca code
  els.becaChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const code = chip.getAttribute('data-beca-code');
      // Visual active state
      els.becaChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      // Apply filter to select and render
      els.filterBeca.value = code;
      els.filterBeca.dispatchEvent(new Event('change'));
    });
  });

  async function fetchJSON(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Error ${res.status} al cargar ${path}`);
    return res.json();
  }

  function format(val) {
    return val == null || val === '' ? '—' : String(val);
  }

  // Helpers para métricas por beca basadas en 'becas_instituciones_completo.json'
  function computeMetricsByBeca(code) {
    const datos = state.instituciones?.datos || [];
    const filtered = datos.filter(r => r.codigo_beca === code);
    const uniq = (arr) => Array.from(new Set(arr.filter(Boolean)));
    return {
      total_registros: filtered.length,
      instituciones_unicas: uniq(filtered.map(r => r.nombre_institucion)).length,
      programas_unicos: uniq(filtered.map(r => r.programa)).length,
      regiones_unicas: uniq(filtered.map(r => r.region)).length,
      fecha_generacion: state.instituciones?.metadatos?.fecha_generacion || '—',
      _filtered: filtered,
    };
  }

  // Render Beca Tec
  function renderBecaTec() {
    const be = state.integrales?.becas?.beca_tec;
    if (be && els.becaTecInfo) {
      const mods = (be.modalidades_especificas || []).join(', ');
      els.becaTecInfo.innerHTML = `
        <h4>Beca Tec – Información general</h4>
        <div class="grid">
          <div class="info-item"><div class="label">Cantidad de becas</div><div class="value">${format(be.cantidad_becas)}</div></div>
          <div class="info-item"><div class="label">Modalidades</div><div class="value">${format(mods)}</div></div>
          <div class="info-item"><div class="label">Tipo de estudio</div><div class="value">${format(be.tipo_estudio)}</div></div>
          <div class="info-item"><div class="label">Cobertura</div><div class="value">${format(be.cobertura)}</div></div>
          <div class="info-item"><div class="label">Estado</div><div class="value">${format(be.estado)}</div></div>
          <div class="info-item"><div class="label">URL oficial</div><div class="value">${be.url_oficial ? `<a href="${be.url_oficial}" target="_blank">${be.url_oficial}</a>` : '—'}</div></div>
        </div>`;
    }

    const metrics = computeMetricsByBeca('beca_tec');
    els.becaTecStats.innerHTML = `
      <div class="stat"><div class="label">Fecha generación</div><div class="value">${format(metrics.fecha_generacion)}</div></div>
      <div class="stat"><div class="label">Instituciones participantes</div><div class="value">${format(metrics.instituciones_unicas)}</div></div>
      <div class="stat"><div class="label">Programas</div><div class="value">${format(metrics.programas_unicos)}</div></div>
      <div class="stat"><div class="label">Regiones</div><div class="value">${format(metrics.regiones_unicas)}</div></div>
    `;

    const term = (els.searchBecaTec?.value || '').trim().toLowerCase();
    const tipo = els.filterTipoBecaTec?.value || '';
    const rows = metrics._filtered
      .filter(r => !tipo || (r.tipo_instituciones || '').toLowerCase() === tipo.toLowerCase())
      .filter(r => {
        if (!term) return true;
        const hay = [r.nombre_institucion, r.region, r.ubicacion, r.programa].map(v => (v || '').toLowerCase());
        return hay.some(v => v.includes(term));
      })
      .map(r => `
        <tr>
          <td>${format(r.nombre_institucion)}</td>
          <td>${format(r.region)}</td>
          <td>${format(r.ubicacion)}</td>
          <td>${format(r.programa)}</td>
          <td>${format(r.modalidad_programa)}</td>
        </tr>
      `)
      .join('');
    els.becaTecTableBody.innerHTML = rows || '<tr><td colspan="5">Sin resultados</td></tr>';
  }

  // Render Beca Perú
  function renderBecaPeru() {
    const bp = state.integrales?.becas?.beca_peru;
    if (bp && els.becaPeruInfo) {
      const cron = bp.cronograma_segundo_momento_2025 || {};
      els.becaPeruInfo.innerHTML = `
        <h4>Beca Perú 2025 – Información general</h4>
        <div class="grid">
          <div class="info-item"><div class="label">Total de becas</div><div class="value">${format(bp.cantidad_becas)}</div></div>
          <div class="info-item"><div class="label">Edad límite</div><div class="value">${format(bp.edad_limite)}</div></div>
          <div class="info-item"><div class="label">Financiamiento</div><div class="value">${format(bp.financiamiento)}</div></div>
          <div class="info-item"><div class="label">Estado</div><div class="value">${format(bp.estado)}</div></div>
          <div class="info-item"><div class="label">URL oficial</div><div class="value">${bp.url_oficial ? `<a href="${bp.url_oficial}" target="_blank">${bp.url_oficial}</a>` : '—'}</div></div>
        </div>
        <div class="list" style="margin-top:10px;">
          <div class="title" style="margin-bottom:6px;">Cronograma Segundo Momento 2025</div>
          <div class="desc">Postulación: ${format(cron.postulacion)}</div>
          <div class="desc">Subsanación: ${format(cron.subsanacion)}</div>
          <div class="desc">Publicación de seleccionados: ${format(cron.publicacion_seleccionados)}</div>
          <div class="desc">Aceptación de la beca: ${format(cron.aceptacion_beca)}</div>
          <div class="desc">Publicación de becarios: ${format(cron.publicacion_becarios)}</div>
        </div>`;
    }

    const metrics = computeMetricsByBeca('beca_peru');
    els.becaPeruStats.innerHTML = `
      <div class="stat"><div class="label">Fecha generación</div><div class="value">${format(metrics.fecha_generacion)}</div></div>
      <div class="stat"><div class="label">Instituciones participantes</div><div class="value">${format(metrics.instituciones_unicas)}</div></div>
      <div class="stat"><div class="label">Programas</div><div class="value">${format(metrics.programas_unicos)}</div></div>
      <div class="stat"><div class="label">Regiones</div><div class="value">${format(metrics.regiones_unicas)}</div></div>
    `;

    const term = (els.searchBecaPeru?.value || '').trim().toLowerCase();
    const tipo = els.filterTipoBecaPeru?.value || '';
    const rows = metrics._filtered
      .filter(r => !tipo || (r.tipo_instituciones || '').toLowerCase() === tipo.toLowerCase())
      .filter(r => {
        if (!term) return true;
        const hay = [r.nombre_institucion, r.region, r.ubicacion, r.programa].map(v => (v || '').toLowerCase());
        return hay.some(v => v.includes(term));
      })
      .map(r => `
        <tr>
          <td>${format(r.nombre_institucion)}</td>
          <td>${format(r.region)}</td>
          <td>${format(r.ubicacion)}</td>
          <td>${format(r.programa)}</td>
          <td>${format(r.modalidad_programa)}</td>
        </tr>
      `)
      .join('');
    els.becaPeruTableBody.innerHTML = rows || '<tr><td colspan="5">Sin resultados</td></tr>';
  }

  // Render Beca 18
  function renderBeca18() {
    const data = state.beca18;
    if (!data) return;

    // Stats
    els.beca18Stats.innerHTML = `
      <div class="stat"><div class="label">Fecha extracción</div><div class="value">${format(data.fecha_extraccion)}</div></div>
      <div class="stat"><div class="label">Universidades elegibles</div><div class="value">${format(data.total_universidades)}</div></div>
      <div class="stat"><div class="label">Modalidades</div><div class="value">${format(data.total_modalidades)}</div></div>
    `;

    // Table universidades
    const term = els.searchBeca18.value.trim().toLowerCase();
    const tipo = els.filterTipoBeca18.value;
    const rows = (data.universidades_elegibles || [])
      .filter(u => !tipo || (u.tipo === tipo))
      .filter(u => {
        if (!term) return true;
        const hay = [u.nombre, u.tipo, u.ubicacion, u.estado].map(v => (v || '').toLowerCase());
        return hay.some(v => v.includes(term));
      })
      .map(u => `
        <tr data-name="${u.nombre}">
          <td>${format(u.nombre)}</td>
          <td>${format(u.tipo)}</td>
          <td>${format(u.quintil)}</td>
          <td>${format(u.ubicacion)}</td>
          <td>${format(u.estado)}</td>
        </tr>
      `)
      .join('');
    els.beca18TableBody.innerHTML = rows || '<tr><td colspan="5">Sin resultados</td></tr>';

    // Promedios
    const proms = data.promedios_minimos_por_modalidad || {};
    const items = Object.entries(proms)
      .map(([modalidad, info]) => {
        const desc = info.descripcion || info.descripcion_modalidad || '';
        const prom = info.promedio_minimo || info.nota_aproximada || '';
        const req = info.requisitos_adicionales || '';
        return `
          <li>
            <div class="title">${modalidad} — ${format(prom)}</div>
            <div class="desc">${format(desc)}</div>
            ${req ? `<div class="desc"><strong>Requisitos:</strong> ${format(req)}</div>` : ''}
          </li>`;
      })
      .join('');
    els.beca18Promedios.innerHTML = items || '<li>Sin información de promedios</li>';
  }

  // Panel de detalle para una universidad en Beca 18
  function renderBeca18Detalle(u) {
    if (!u || !els.beca18Detalle) return;
    const fuente = u.fuente_url && /^https?:\/\//.test(u.fuente_url)
      ? `<a href="${u.fuente_url}" target="_blank">${format(u.fuente || 'Fuente')}</a>`
      : format(u.fuente || u.fuente_url);

    const mods = (u.modalidades || []).map(m => `
      <li>
        <div class="title">${format(m.modalidad)}</div>
        <div class="desc">Nota mínima: ${format(m.nota_minima)}</div>
        ${m.requisitos_adicionales ? `<div class="desc">Requisitos: ${format(m.requisitos_adicionales)}</div>` : ''}
        ${m.descripcion ? `<div class="desc">${format(m.descripcion)}</div>` : ''}
      </li>
    `).join('');

    els.beca18Detalle.innerHTML = `
      <h4>${format(u.nombre)}</h4>
      <div class="grid" style="margin-top:8px;">
        <div class="info-item"><div class="label">Tipo</div><div class="value">${format(u.tipo)}</div></div>
        <div class="info-item"><div class="label">Quintil</div><div class="value">${format(u.quintil)}</div></div>
        <div class="info-item"><div class="label">Ubicación</div><div class="value">${format(u.ubicacion)}</div></div>
        <div class="info-item"><div class="label">Estado</div><div class="value">${format(u.estado)}</div></div>
        <div class="info-item"><div class="label">Convocatoria</div><div class="value">${format(u.convocatoria)}</div></div>
        <div class="info-item"><div class="label">Elegible Beca 18</div><div class="value">${u.elegible_beca18 ? 'Sí' : 'No'}</div></div>
        <div class="info-item"><div class="label">Fuente</div><div class="value">${fuente}</div></div>
      </div>
      <div style="margin-top:10px;">
        <div class="title" style="color: var(--muted); font-size:12px; margin-bottom:6px;">Modalidades y requisitos</div>
        <ul class="list">${mods || '<li><div class="desc">Sin modalidades registradas</div></li>'}</ul>
      </div>
    `;
    els.beca18Detalle.classList.remove('hidden');
    try { els.beca18Detalle.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch {}
  }

  // Render Instituciones por Beca
  function renderInstituciones() {
    const data = state.instituciones;
    if (!data) return;

    const stats = data.estadisticas || {};
    els.institucionesStats.innerHTML = `
      <div class="stat"><div class="label">Total registros</div><div class="value">${format(stats.total_registros)}</div></div>
      <div class="stat"><div class="label">Becas procesadas</div><div class="value">${format(stats.total_becas)}</div></div>
    `;

    const term = els.searchInstituciones.value.trim().toLowerCase();
    const beca = els.filterBeca.value;

    // Mostrar resumen informativo si la beca filtrada es Beca Perú
    if (beca === 'beca_peru' && state.integrales?.becas?.beca_peru) {
      const bp = state.integrales.becas.beca_peru;
      const cron = bp.cronograma_segundo_momento_2025 || {};
      els.institucionesInfoBeca.innerHTML = `
        <h4>Beca Perú 2025 – Información general</h4>
        <div class="grid">
          <div class="info-item">
            <div class="label">Total de becas</div>
            <div class="value">${format(bp.cantidad_becas)}</div>
          </div>
          <div class="info-item">
            <div class="label">Edad límite</div>
            <div class="value">${format(bp.edad_limite)}</div>
          </div>
          <div class="info-item">
            <div class="label">Financiamiento</div>
            <div class="value">${format(bp.financiamiento)}</div>
          </div>
          <div class="info-item">
            <div class="label">Estado</div>
            <div class="value">${format(bp.estado)}</div>
          </div>
        </div>
        <div class="list" style="margin-top:10px;">
          <div class="title" style="margin-bottom:6px;">Cronograma Segundo Momento 2025</div>
          <div class="desc">Postulación: ${format(cron.postulacion)}</div>
          <div class="desc">Subsanación: ${format(cron.subsanacion)}</div>
          <div class="desc">Publicación de seleccionados: ${format(cron.publicacion_seleccionados)}</div>
          <div class="desc">Aceptación de la beca: ${format(cron.aceptacion_beca)}</div>
          <div class="desc">Publicación de becarios: ${format(cron.publicacion_becarios)}</div>
        </div>
      `;
      els.institucionesInfoBeca.classList.remove('hidden');
    } else {
      els.institucionesInfoBeca.classList.add('hidden');
      els.institucionesInfoBeca.innerHTML = '';
    }
    const rows = (data.datos || [])
      .filter(r => !beca || r.codigo_beca === beca)
      .filter(r => {
        if (!term) return true;
        const hay = [r.nombre_institucion, r.region, r.ubicacion, r.programa].map(v => (v || '').toLowerCase());
        return hay.some(v => v.includes(term));
      })
      .map(r => `
        <tr>
          <td>${format(r.codigo_beca)}</td>
          <td>${format(r.nombre_institucion)}</td>
          <td>${format(r.region)}</td>
          <td>${format(r.ubicacion)}</td>
          <td>${format(r.programa)}</td>
          <td>${format(r.modalidad_programa)}</td>
        </tr>
      `)
      .join('');
    els.institucionesTableBody.innerHTML = rows || '<tr><td colspan="6">Sin resultados</td></tr>';
  }

  // Render Becas Integrales
  function renderBecasIntegrales() {
    const data = state.integrales;
    if (!data) return;

    const stats = data.estadisticas || {};
    els.becasStats.innerHTML = `
      <div class="stat"><div class="label">Fecha extracción</div><div class="value">${format(data.fecha_extraccion)}</div></div>
      <div class="stat"><div class="label">Total categorías</div><div class="value">${format(Object.keys(data.categorias || {}).length)}</div></div>
    `;

    const term = els.searchBecas.value.trim().toLowerCase();
    const cat = els.filterCategoria.value;
    // data.becas es un diccionario de becas (codigo -> info)
    const registros = Object.entries(data.becas || {})
      .map(([codigo, info]) => ({ codigo, ...info }))
      .filter(b => !cat || (b.categoria || '').toLowerCase() === cat)
      .filter(b => {
        if (!term) return true;
        const hay = [b.nombre, b.institucion, b.tipo_estudio, b.modalidad].map(v => (v || '').toLowerCase());
        return hay.some(v => v.includes(term));
      });

    els.becasTableBody.innerHTML = registros.map(b => `
      <tr>
        <td>${format(b.codigo)}</td>
        <td>${format(b.nombre)}</td>
        <td>${format(b.institucion)}</td>
        <td>${format(b.categoria)}</td>
        <td>${format(b.tipo_estudio)}</td>
        <td>${format(b.modalidad)}</td>
        <td>${format(b.cobertura)}</td>
        <td>${b.url_oficial ? `<a href="${b.url_oficial}" target="_blank">link</a>` : '—'}</td>
        <td>${format(b.estado)}</td>
      </tr>
    `).join('') || '<tr><td colspan="9">Sin resultados</td></tr>';
  }

  // Render Estadísticas globales
  function renderEstadisticasGlobales() {
    const ins = state.instituciones?.estadisticas;
    if (!ins) return;
    els.statsGlobales.innerHTML = `
      <div class="card"><div class="title">Total registros</div><div class="value">${format(ins.total_registros)}</div></div>
      <div class="card"><div class="title">Total becas</div><div class="value">${format(ins.total_becas)}</div></div>
    `;

    const rows = Object.entries(ins.resumen_por_beca || {})
      .map(([codigo, s]) => `
        <tr>
          <td>${format(s.nombre_beca || codigo)}</td>
          <td>${format(s.total_registros)}</td>
          <td>${format(s.instituciones_unicas)}</td>
          <td>${format(s.regiones_unicas)}</td>
        </tr>
      `)
      .join('');
    els.statsBecaBody.innerHTML = rows || '<tr><td colspan="4">Sin datos</td></tr>';
  }

  // Bind filters
  els.searchBeca18.addEventListener('input', renderBeca18);
  els.filterTipoBeca18.addEventListener('change', renderBeca18);
  if (els.searchBecaTec) els.searchBecaTec.addEventListener('input', renderBecaTec);
  if (els.filterTipoBecaTec) els.filterTipoBecaTec.addEventListener('change', renderBecaTec);
  if (els.searchBecaPeru) els.searchBecaPeru.addEventListener('input', renderBecaPeru);
  if (els.filterTipoBecaPeru) els.filterTipoBecaPeru.addEventListener('change', renderBecaPeru);
  els.searchInstituciones.addEventListener('input', renderInstituciones);
  els.filterBeca.addEventListener('change', renderInstituciones);
  els.searchBecas.addEventListener('input', renderBecasIntegrales);
  els.filterCategoria.addEventListener('change', renderBecasIntegrales);

  // Click en filas de universidades (Beca 18)
  if (els.beca18TableBody) {
    els.beca18TableBody.addEventListener('click', (e) => {
      const tr = e.target.closest('tr');
      if (!tr) return;
      const name = tr.getAttribute('data-name') || (tr.cells && tr.cells[0] ? tr.cells[0].textContent.trim() : '');
      const uni = (state.beca18?.universidades_elegibles || []).find(u => (u.nombre || '').trim() === name);
      if (uni) renderBeca18Detalle(uni);
    });
  }

  // Init: load and auto-refresh JSONs
  async function loadAllData() {
    try {
      const ts = Date.now(); // cache-busting
      const [beca18, instituciones, integrales] = await Promise.all([
        fetchJSON(`beca18_datos.json?v=${ts}`),
        fetchJSON(`becas_instituciones_completo.json?v=${ts}`),
        fetchJSON(`becas_integrales_completo.json?v=${ts}`),
      ]);

      state.beca18 = beca18;
      state.instituciones = instituciones;
      state.integrales = integrales;

      renderBeca18();
      renderBecaTec();
      renderBecaPeru();
      renderInstituciones();
      renderBecasIntegrales();
      renderEstadisticasGlobales();
    } catch (err) {
      console.error(err);
      const msg = `No se pudieron cargar los datos: ${err.message}`;
      [els.beca18Error, els.institucionesError, els.becasError, els.statsError].forEach(el => {
        if (!el) return;
        el.textContent = msg;
        el.classList.remove('hidden');
      });
    }
  }

  function startAutoRefresh(intervalMs = 60000) { // 60s
    setInterval(loadAllData, intervalMs);
  }

  async function init() {
    await loadAllData();
    startAutoRefresh(60000);
  }

  init();
})();