library('ProjectTemplate')
# load.project()

for (dataset in project.info$data)
{
  message(paste('Showing top 5 rows of', dataset))
# print(head(get(dataset)))
}

divide.by.zero <- function(a,b){
  a.per.b <- a / b
  a.per.b[is.nan(a.per.b)] <- 0
  a.per.b
}

yoga.top.1 <- quinoa[order(quinoa$yoga.teachers / quinoa$pop, decreasing = T),][1:100,]
print(yoga.top.1[1:5,])

yoga.top.2 <- subset(quinoa[order(quinoa$yoga.teachers / quinoa$pop, decreasing = T),],yoga.teachers > 1)[1:10,]
print(yoga.top.2[1:5,])

ccof.top <- quinoa[order(quinoa$ccof.operators, decreasing = T),][1:100,]
nop.top <- quinoa[order(quinoa$nop.operators, decreasing = T),][1:100,]

gender.imbalance <- quinoa[order(abs(quinoa$portion.female - 0.5), decreasing = T),][1:1000,]
gender.imbalance.plot <- ggplot(quinoa) +
  aes(y=(pop*(1-portion.female)), x=(pop*portion.female)) +
  geom_abline(slope=1, intercept = 0) +
  # Dunno what's wrong with this
# opts(
#   plot.title = 'Zip code gender balance'
#   plot.title = 'Out-lying gender imbalances tend towards males with high populations and vice-versa',
#   axis.title.x = 'Females within a particular zip code',
#   axis.title.y = 'Males within a particular zip code'
# ) +
  geom_point()
print(gender.imbalance.plot)
