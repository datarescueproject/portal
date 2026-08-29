/**
 * Usage:
 * <div data-component="datasets-list">
 *   <h3 class="datasets-count" data-hook="datasets-count"></h3>
 *   <input type="text" data-hook="search-query" placeholder="Search..." class="form-control">
 *   <div data-hook="datasets-items"></div>
 * </div>
 *
 * Optionally, add filters to the component element such as
 *   data-organization="sample-department"
 *   data-category="education"
 */
import {pick, defaults, filter} from 'lodash'

import TmplDatasetItem from '../templates/dataset-item'
import {queryByHook, setContent, createDatasetFilters} from '../util'

export default class {
  constructor (opts) {
    const elements = {
      datasetsItems: queryByHook('datasets-items', opts.el),
      datasetsCount: queryByHook('datasets-count', opts.el),
      searchQuery: queryByHook('search-query', opts.el),
      pagination: queryByHook('datasets-pagination', opts.el),
      paginationNav: queryByHook('datasets-pagination-nav', opts.el),
      empty: queryByHook('datasets-empty', opts.el)
    }

    // Filter datasets and render in items container
    const paramFilters = pick(opts.params, ['organization', 'category', 'status'])
    const attributeFilters = pick(opts.el.data(), ['organization', 'category', 'status'])
    const filters = createDatasetFilters(defaults(paramFilters, attributeFilters))
    const filteredDatasets = filter(opts.datasets, filters)
    const pageSize = Number(opts.el.data('page-size')) || 20
    let currentPage = 1
    let visibleDatasets = filteredDatasets

    const render = () => {
      const totalPages = Math.max(1, Math.ceil(visibleDatasets.length / pageSize))
      currentPage = Math.min(currentPage, totalPages)
      const start = (currentPage - 1) * pageSize
      const datasetsMarkup = visibleDatasets.slice(start, start + pageSize).map(TmplDatasetItem)
      setContent(elements.datasetsItems, datasetsMarkup)

      const datasetSuffix = visibleDatasets.length === 1 ? '' : 's'
      setContent(elements.datasetsCount, visibleDatasets.length + ' dataset' + datasetSuffix)
      if (elements.empty.length) elements.empty.prop('hidden', visibleDatasets.length !== 0)

      elements.paginationNav.toggleClass('d-none', totalPages <= 1)
      const paginationMarkup = []
      paginationMarkup.push(this._paginationItem('Previous', currentPage - 1, currentPage === 1))
      const pages = new Set([1, totalPages])
      for (let page = currentPage - 2; page <= currentPage + 2; page++) {
        if (page > 0 && page <= totalPages) pages.add(page)
      }
      let previousPage
      for (const page of Array.from(pages).sort((a, b) => a - b)) {
        if (previousPage && page - previousPage > 1) {
          paginationMarkup.push('<li class="page-item disabled"><span class="page-link">&hellip;</span></li>')
        }
        paginationMarkup.push(this._paginationItem(page, page, false, page === currentPage))
        previousPage = page
      }
      paginationMarkup.push(this._paginationItem('Next', currentPage + 1, currentPage === totalPages))
      setContent(elements.pagination, paginationMarkup)
    }

    elements.pagination.on('click', '[data-page]', (e) => {
      const page = Number(e.currentTarget.dataset.page)
      if (!e.currentTarget.disabled && page !== currentPage) {
        currentPage = page
        render()
        opts.el[0].scrollIntoView({behavior: 'smooth', block: 'start'})
      }
    })

    // Search datasets listener
    const searchFunction = this._createSearchFunction(filteredDatasets)
    elements.searchQuery.on('input', (e) => {
      const query = e.currentTarget.value
      visibleDatasets = searchFunction(query)
      currentPage = 1
      render()
    })

    render()
  }

  _paginationItem (label, page, disabled, active = false) {
    return `<li class="page-item${disabled ? ' disabled' : ''}${active ? ' active' : ''}">
      <button class="page-link" type="button" data-page="${page}"${disabled ? ' disabled' : ''}${active ? ' aria-current="page"' : ''}>${label}</button>
    </li>`
  }

  // Returns a function that can be used to search an array of datasets
  // The function returns the filtered array of datasets
  _createSearchFunction (datasets) {
    const keys = ['title', 'notes', 'description', 'organization', 'agency']
    return function (query) {
      const lowerCaseQuery = query.toLowerCase()
      return filter(datasets, function (dataset) {
        return keys.reduce(function (previousValue, key) {
          return previousValue || (dataset[key] && dataset[key].toLowerCase().indexOf(lowerCaseQuery) !== -1)
        }, false)
      })
    }
  }
}
