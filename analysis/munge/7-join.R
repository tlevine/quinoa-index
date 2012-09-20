quinoa <- join(aff.grouped, yoga.grouped, by = 'zip')
quinoa$yoga.teachers[is.na(quinoa$yoga.teachers)] <- 0
