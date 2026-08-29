const escapeHTML = (value) => String(value || '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#039;')

const statusBadges = (statusValue) => {
  const statuses = String(statusValue || '')
    .split(',')
    .map((status) => status.trim())
    .filter(Boolean)

  if (!statuses.length) return ''

  const badges = statuses.map((status) => {
    const statusClass = status.toLowerCase().replace(/\s+/g, '-')
    return `<span class="status-badge status-${statusClass}">${escapeHTML(status)}</span>`
  }).join('')

  return `<div class="status-badge-list">${badges}</div>`
}

export default (data) => {
  const categories = Array.isArray(data.category) ? data.category : (data.category ? [data.category] : [])
  const notes = data.notes || data.description
  return `<article class="dataset-card">
    <div class="dataset-card__meta">
      ${statusBadges(data.dataset_source_status)}
      <span class="dataset-card__office" title="${escapeHTML(data.organization)}">${escapeHTML(data.organization)}</span>
    </div>
    <h2><a href="${escapeHTML(data.url)}">${escapeHTML(data.title)}</a></h2>
    ${notes ? `<div class="dataset-card__summary"><p>${escapeHTML(notes)}</p></div>` : ''}
    ${categories.length ? `<div class="tag-row">${categories.map((category) => `<span class="category-tag">${escapeHTML(category)}</span>`).join('')}</div>` : ''}
  </article>`
}
