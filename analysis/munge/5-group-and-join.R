aff.grouped <- ddply(aff, 'zip', function(df){
  pop <- sum(df$Total.population)
  
})
