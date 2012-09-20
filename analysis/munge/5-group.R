library(isotone)

aff.grouped <- ddply(aff, 'zip', function(df){
  pop <- sum(df$Total.population)
  median.age <- weighted.median(df$Median.age..years, df$Total.population)
  portion.female <- weighted.mean(df$portion.female, df$Total.population, na.rm = T)

  if (pop > 0) {
    c(
      pop = sum(df$Total.population),
      median.age = median.age,
      portion.female = portion.female
    )
  } else {
    c(pop = 0, median.age = NA, portion.female = 0.5)
  }
})

yoga.grouped <- ddply(yoga, 'zip', function(df){
  c(yoga.teachers = nrow(df))
})

nop.grouped <- ddply(nop, 'zip', function(df){
  c(nop.operators = nrow(df))
})

ccof.grouped <- ddply(ccof, 'zip', function(df){
  c(ccof.operators = nrow(df))
})
