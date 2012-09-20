library('ProjectTemplate')
load.project()

for (dataset in project.info$data)
{
  message(paste('Showing top 5 rows of', dataset))
  print(head(get(dataset)))
}

yoga.top.1 <- quinoa[order(quinoa$yoga.teachers.per.capita, decreasing = T),][1:100,]
print(yoga.top.1[1:5,])

yoga.top.2 <- subset(quinoa[order(quinoa$yoga.teachers.per.capita, decreasing = T),],yoga.teachers > 1)[1:10,]
print(yoga.top.2[1:5,])
