library(ggmap)
library(plotrix)
cities2020 <- read.csv('cities2020_utf8.csv')
firstrow <- colnames(cities2020)
colnames(cities2020) <- c('City1','City2','City3','City4','City5','City6','City7','City8','City9','City10','City11','City12','City13','City14','City15','City16')
cities2020 <- rbind(firstrow, cities2020)
unique2020 <- read.csv('citieslist.csv')
colnames(unique2020) <- c('City')
unique2020 <- rbind(c('San Francisco, CA'), unique2020)
freq <- as.data.frame(table(unique2020))
freq$Freq <- rescale(freq$Freq, c(1,1000))
for (i in length(unique2020)) {
  count = 0
  print(unique2020[i])
  for (col in colnames(cities2020)) {
    count = count + sum(cities2020$col == unique2020[i])
  }
  print(count)
  freq$Freq[i] <- count
}

