aff.grouped <- ddply(aff, 'zip', function(df){
  c(
    pop = sum(df$Total.population),
    pseudo.median.age = median(df$Median.age..years),
    portion.female = weighted.mean(df$portion.female, df$Total.population)
  )
})
