import $ from 'jquery'
import { chain, defaults, omit } from 'lodash'

import TmplListGroupItem from '../templates/list-group-item'
import { setContent, slugify } from '../util'

const STATUS_LABELS = {
  removed: 'Removed',
  modified: 'Modified',
  reinstated: 'Reinstated',
  restricted: 'Restricted',
  discontinued: 'Discontinued',
  'tool-removed': 'Tool Removed'
}

export default class {
  constructor (opts) {
    const statuses = chain(opts.datasets)
      .flatMap((dataset) => (dataset.dataset_source_status || '').split(','))
      .map((status) => slugify(status))
      .filter((status) => STATUS_LABELS[status])
      .countBy()
      .map((count, status) => {
        const selected = opts.params.status === status
        const params = selected ? omit(opts.params, 'status') : defaults({ status }, opts.params)
        return { title: STATUS_LABELS[status], url: '?' + $.param(params), count, selected }
      })
      .orderBy('title')
      .value()

    setContent(opts.el, statuses.map(TmplListGroupItem))
  }
}
