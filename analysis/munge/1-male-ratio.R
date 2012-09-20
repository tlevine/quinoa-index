aff$portion.female <- (function(){
  # Dunno what the difference is, so let's take a mean.
  males.per.female <- mean(aff$Males.per.100.females, aff$Males.per.100.females.1)/100

  # Then turn it into a proportion
  portion.male <- males.per.female / (males.per.female + 1)

  # Return portion female for funzies.
  1 - portion.male
})()
