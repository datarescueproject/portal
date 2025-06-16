export default (data) => (
`<dataset>
  <div class="card mb-3">
    <div class="card-body">
      <h4 class="card-title">
        <a href="${data.url}">${data.title}</a>
      </h4>
      <div class="card-text">
        ${data.notes || ''}
      </div>
    </div>
  </div>
</dataset>`

)
// <h3><a href="${data.url}">${data.title}</a></h3>
// ${data.notes || ''}