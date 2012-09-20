quinoa <- join(
  join(aff.grouped, yoga.grouped, by = 'zip'),
  join(ccof.grouped, nop.grouped, by = 'zip'),
  by = 'zip'
)
quinoa$yoga.teachers[is.na(quinoa$yoga.teachers)] <- 0
