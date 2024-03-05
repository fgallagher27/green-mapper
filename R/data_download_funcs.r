#### Description

# This script creates a shapefile map of London's public transport system.
# It uses the TFL API and various other sources to construct the map.
# To run this script a tfl_api.yml file should be set up in the root directory
# with TFL as the top level, and app_id and app_key as sub levels

#### Set up ----

library(config)
library(here)
library(jsonlite)
library(httr)

api_key_path <- here("tfl_api.yml")
api_info <- config::get(file = api_key_path)
api_key <- api_info$app_key
api_id <- api_info$app_id


#### Function ----
bike <- "https://api.tfl.gov.uk/BikePoint"
tube <- "https://api.tfl.gov.uk/Line/Mode/tube"

url <- modify_url(
    route,
    query = list(app_id = api_id, app_key = api_key)
)

request <- GET(url)
request
request$status_code


route <- jsonlite::fromJSON(content(request, "text"))

#' Accesses a TFL database and converts the output into a shapefile
#'
#' @param url a string containing the url request to execute
#' @param credentials list containing api access id and key
#' @param save boolean toggle for saving the file, `FALSE` as default
#' @param shp_name string of filepath to save to when `save=TRUE`
#'
#' @examples
#' create_shp()
create_shp <- function(url, credentials, save = FALSE, shp_name = "") {
    url_mod <- modify_url(
        url,
        query = list(app_id = credentials[[1]], app_key = credentials[[2]])
    )

    request <- GET(url_mod)
    status <- request$status_code
    content <- jsonlite::fromJSON(content(request, "text"))

    shp <- data.frame(
        id = seq_along(seq_len(length(content$lat))),
        name = content$commonName,
        lat = content$lat,
        lon = content$lon
    )|>
        sf::st_as_sf(coords = c("lon", "lat"))

    if (status == 200) {
        sf::st_write(shp, shp_name)
    } else {
        message("Bad status: ", status)
    }

    return(shp)
}
