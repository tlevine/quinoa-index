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
  yoga.teachers <- nrow(df)

  if (is.na(yoga.teachers)) {
    0
  } else {
    yoga.teachers
  }
})
