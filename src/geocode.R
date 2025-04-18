library(geocodebr)
library(sf)
library(tidyverse)

df <- readxl::read_excel("../datasets/butecos_2025_cleaned.xlsx")

campos <- geocodebr::definir_campos(
  logradouro = "Rua",
  numero = "Numero",
  localidade = "Bairro",
  municipio = "Cidade",
  estado = "UF"
)

df <- geocodebr::geocode(
  enderecos = df,
  campos_endereco = campos,
  resultado_completo = FALSE,
  resolver_empates = FALSE,
  resultado_sf = FALSE,
  verboso = FALSE,
  cache = TRUE,
  n_cores = 1
)

writexl::write_xlsx(df, "butecos_2025_geolocated.xlsx")

