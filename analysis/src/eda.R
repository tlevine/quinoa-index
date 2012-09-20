library('ProjectTemplate')
load.project()

for (dataset in project.info$data)
{
  message(paste('Showing top 5 rows of', dataset))
  print(head(get(dataset)))
}

yoga.top.100 <- quinoa[order(quinoa$yoga.teachers.per.capita, decreasing = T),][1:100,]
print(yoga.top.100[1:5,])
