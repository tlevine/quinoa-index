quinoa <- join(
  join(aff.grouped, yoga.grouped, by = 'zip'),
  join(ccof.grouped, nop.grouped, by = 'zip'),
  by = 'zip'
)

for (var in c('yoga.teachers', 'ccof.operators', 'nop.operators')) {
  quinoa[,var][is.na(quinoa[,var])] <- 0
}
