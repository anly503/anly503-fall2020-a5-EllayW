library(plotly)
library(dplyr)
library(tidyr)
library(htmlwidgets)

df <- read.csv('plot-data.csv')
df2 <- df%>%
  select(date, appliance, house,consumption) %>%
  group_by(date,appliance,house) %>%
  summarise(consumption = sum(consumption))
df2$consumption <- df2$consumption/1000000
df2 <- df2[df2$house == 4,]
df2$house = NULL


## change data type
df2$appliance <- factor(df2$appliance)
df2$date <- factor(df2$date)
df3 <- df2 %>% 
  group_by(date,appliance) %>%
  summarise(consumption = sum(consumption)) %>% 
  ungroup()

shared_data <- df3 %>% 
  highlight_key(~appliance)

## @knitr fig
fig <-shared_data  %>%
  plot_ly(., x = ~date, 
          y = ~consumption, type = 'scatter',mode = 'line',
          color = ~appliance, fill = 'tozeroy',
          text = ~consumption,
          hoverinfo = 'text',
          transforms = list(
            list(
              type = 'filter',
              target = ~appliance,
              operation = '=',
              value = unique(df2$appliance)[1]
            )
          ))


fig <- fig %>% layout(
  title = "Daily Consumption(M) by Appliances")


### attempt 2 -- failed
## DO NOT RUN
#####################################################
fig2 <- shared_data %>% plot_ly() %>%
  add_pie(., 
          labels = ~appliance, 
          values = ~consumption, 
          textinfo = 'label+percent') %>%
  layout(title = 'Pie Chart of Consumption(M) by Appliances')


fig2 <- fig2 %>% layout(title = 'Pie Chart of Consumption(M) by Appliances',
                      xaxis = list(showgrid = FALSE, 
                                   zeroline = FALSE, 
                                   showticklabels = FALSE),
                      yaxis = list(showgrid = FALSE, 
                                   zeroline = FALSE, 
                                   showticklabels = FALSE))

#subplot(fig,fig2,nrow=2)
###########################################

saveWidget(fig, file="plotly.html")

## run the output

fig