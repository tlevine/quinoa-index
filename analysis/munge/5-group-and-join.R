library(isotone)
aff.grouped <- ddply(aff, 'zip', function(df){
  c(
    pop = sum(df$Total.population),
    median.age = weighted.median(df$Median.age..years, df$Total.population),
    portion.female = weighted.mean(df$portion.female, df$Total.population)
  )
})
