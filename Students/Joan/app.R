library("dplyr")
library("plotly")
library("readr")
library("rsconnect")
library("printr")
library("DT")
library("rstudioapi")
library("reshape")
library("lubridate")
library("shiny")
library("shinydashboard")
library("highcharter")
library("vctrs")
library("simtimer")

df <- read.csv("master.csv",as.is = TRUE)
df$Date.Time <- strptime(df$Date.Time,format = "%d/%m/%Y %H:%M:%S") 
df <- df[-which(is.na(df$Date.Time)),]
df$year <- year(df$Date.Time)
df$month <- month(df$Date.Time)
df$day <- day(df$Date.Time)
df$hour <- hour(df$Date.Time)
# df$hour <- hour(df$Date.Time)
df$Date.Time <- date(df$Date.Time)
df$Duration <- strptime(df$Duration,format="%H:%M:%S", tz = "CET")
df$Duration <- hour(df$Duration)*60 + minute(df$Duration)
df$Duration[which(df$Duration > 120)] <- NA

userlist <- split(df,df$User)

fdf_day <- function(df){
  df_day <- df %>%  
    group_by(year,month,day) %>%  
    summarise(Intensity = round(mean(Intensity,na.rm = T),digits = 2),
              Duration = round(mean(Duration,na.rm = T),digits = 2),
              nattacks = n(),
              Date.Time = Date.Time[1])
  return(df_day)
}
fdf_month <- function(df){
  
  df_month <- df %>%  
    group_by(year,month) %>%  
    summarise(Intensity = round(mean(Intensity, na.rm = T),digits = 2),
              Duration = round(mean(Duration, na.rm = T),digits = 2),
              nattacks = n(),
              Date.Time = Date.Time[1])
  return(df_month)
}
fhourly <- function(df){  
  hourly <- df %>%  group_by(hour) %>%  summarise(Intensity = round(mean(Intensity,na.rm = T),digits = 2),
                                                  Duration = round(mean(Duration,na.rm = T),digits = 2),
                                                  nattacks = n())
  return(hourly)
}
fdaily <- function(df){
  daily <- df %>%  group_by(day) %>%  summarise(Intensity = round(mean(Intensity,na.rm = T),digits = 2),
                                                Duration = round(mean(Duration,na.rm = T),digits = 2),
                                                nattacks = n())
  return(daily)
}
# USER INTERFACE
ui <- dashboardPage(skin = "red",
                    dashboardHeader(title = "Nobism Project"),
                    dashboardSidebar(
                      sidebarMenu(
                        menuItem("Graphs",tabName = "graphs", icon = icon("bar-chart")),
                        menuItem("Trends",tabName = "trends", icon = icon("chart-line")),
                        numericInput(inputId = "userid",label = "UserID",value = 1),
                        
                        selectInput(inputId = "Granularity", label = "Select a granularity",
                                    choices=c("Day","Month"),selected = "Month"),
                        
                        selectInput(inputId = "Variable", label = "Select a variable", selected = "Intensity",
                                    choices = c("Intensity","Duration","nattacks")),
                        
                        dateRangeInput(inputId = "Dates", label = "Select date ranges",
                                       start = min(df$Date.Time),end = max(df$Date.Time),
                                       min = min(df$Date.Time),max = max(df$Date.Time))
                      )
                    ),
                    dashboardBody(
                      tabItems(
                        tabItem(tabName = "graphs",
                                tabsetPanel(
                                  tabPanel(title = "Time Graphs",
                                           box(highchartOutput("plot"),width = 12)))),
                        tabItem(tabName = "trends",
                                tabsetPanel(
                                  tabPanel(title = "Trends",
                                           selectInput(inputId = "trendgran", label = NULL,
                                                       choices = c("day","hour"),selected = "day",width = 100),
                                           box(plotlyOutput("plot1"),width = 12))))
    )
  )
)



# SERVER
server <- function(input, output) {
  
  userselect <- reactive({
    validate(
      need(input$userid %in% unique(df$User), "Please enter a valid USERID")
    )
      df <- df %>% dplyr::filter(User == input$userid)
  })
  
  get.granularity <- reactive({
    switch(input$Granularity,
           "Day" = 
             if (input$userid == 1) {
               fdf_day(df)
             } else {
               fdf_day(userselect())
             },
           "Month" =
             if (input$userid == 1) {
                fdf_month(df)
             } else {
                fdf_month(userselect())
             })
  })
  
  filteredData <- reactive({
    get.granularity() %>% 
      dplyr::select(Variable = input$Variable, Date.Time) %>% 
      dplyr::filter(Date.Time <= input$Dates[2] & Date.Time >= input$Dates[1])
  })
  
  output$Dates <- renderPrint ({ 
    input$Dates 
  })
  
  output$plot <- renderHighchart({
      data_plot <- filteredData()
    
    highchart(type = "stock",theme = hc_theme_economist()) %>% 
      hc_add_series(name = input$Variable,data_plot, "line", hcaes(x = Date.Time,y = Variable)) %>%
      #hc_add_series(name = input$Variable,data_plot, "column", hcaes(x = Date.Time,y = Variable)) %>% 
      hc_title(text = paste(input$Variable," over time every ",input$Granularity)) %>% 
      hc_xAxis(title = list(text = input$Granularity)) %>%
      hc_yAxis(title = list(text = input$Variable),min = 0, tickInterval = 1, opposite = FALSE)
  })
  
  output$plot1 <- renderPlotly({
      data_plot <- userselect()
    
    if (input$Variable == "nattacks") {
      trendf <- data_plot %>% dplyr::select(variable = "Intensity",time = input$trendgran)
      colnames(trendf) <- c("variable","time")
      datatrend <- trendf %>% group_by(time) %>%  summarise(variable = n())
      plotly::plot_ly(datatrend,x = ~time,y = ~variable, type = "scatter", mode = 'lines') %>%
        layout(xaxis = list(title = input$trendgran),
               yaxis = list(title = input$Variable, ticks = "outside",tick0 = 0))
    }else{
      trendf <- data_plot %>% dplyr::select(variable = input$Variable,time = input$trendgran)
      colnames(trendf) <- c("variable","time")
      datatrend <- trendf %>% group_by(time) %>%  summarise(variable = mean(variable,na.rm = T))
      plotly::plot_ly(datatrend,x = ~time,y = ~variable, type = "scatter", mode = 'lines') %>%
        layout(xaxis = list(title = input$trendgran),
               yaxis = list(title = input$Variable, ticks = "outside",tick0 = 0))
    }
  })
}

# RUNNING APP
shinyApp(ui, server)
