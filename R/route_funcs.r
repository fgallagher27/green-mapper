#### Description

# This script contains the function to caclulate different
# routes between two points, and calculate the associated
# time, distance and CO2

#### Set up ----

library(tidyverse)
library(config)
library(here)
library(jsonlite)
library(httr)


#### Function definitions ----

route_recommendations <- function(id, start_point, end_point){
    # load in preferences
    id_weightings <- preferences |> filter(id == 'id')
    routes_df <- get_routes_metrics(start_point, end_point)
    rank_df <- convert_metric_to_rank(routes_df)
    weighted_rank_df <- apply_weights(rank_df, id_weightings)
    return(weighted_rank_df)
}

get_routes_metrics <- function(start_point, end_point) {
    routes <- calc_routes(start_point, end_point)
    time <- calc_time(routes)
    dist <- calc_dist(routes)
    co2 <- calc_co2(routes)

    dfs <- c(routes, time, dist, co2)
    out_df <- purrr::reduce(dfs, left_join)

    return(out_df)
}


#' Retrieves possible routes using TFL API journey planner. The routes
#' are then converted from text format to a shapefile containing the
#' line strings of the various legs of each route from start point to
#' end point along recognised transport links.
#'
#' @param start_point a postcode or coordinate point as a string
#' @param end_point a postcode or coordinate point as a string
#' @param credentials list containing api access id and key
#'
#' @examples
#' calc_routes()
calc_routes <- function(start_point, end_point, credentials) {

    # 1. retrieve routes from TFL API journey planner
    route_url <- paste0(
        "https://api.tfl.gov.uk/Journey/JourneyResults/",
        start_point,
        "/to/",
        end_point
    )
    url <- modify_url(
        route_url,
        query = list(app_id = credentials[[0]], app_key = credentials[[2]])
    )

    request <- GET(url)
    route_info <- jsonlite::fromJSON(content(request, "text"))

    # 2. extract route information and convert to shapefile
    return(routes)
}

calc_time <- function(routes_df) {

}

calc_dist <- function(routes_df) {
    
}

calc_co2 <- function(routes_df) {
    
}


convert_metric_to_rank <- function(routes) {
    # rank each route on each metric  1:n
}


apply_weights <- function(rank_df, weighting) {
    temp <- rank_df * weighting
    temp <- temp |>
        mutate('route_rank' = sum()) |>
        arrange('route_rank', desc=TRUE)
    return(temp)
}

update_weights <- function(id, weighting) {
    
}