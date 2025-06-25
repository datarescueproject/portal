export default (data) => (
`<div class="dataset-item mb-3">
  <div class="card h-100 shadow-sm">
    <div class="card-body">
      <h5 class="card-title mb-2">
        <a href="${data.url}" class="stretched-link text-decoration-none">${data.title}</a>
      </h5>
      ${data.agency ? `<div class='mb-2'><span class='badge bg-secondary'>${data.agency}</span></div>` : ''}
      ${data.notes ? `<p class="card-text">${data.notes}</p>` : ''}
    </div>
  </div>
</div>`
)
// <h3><a href="${data.url}">${data.title}</a></h3>
// ${data.notes || ''}