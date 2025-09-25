#!/usr/bin/env Rscript

library(pdftools)
library(tabulapdf)

extract_tables_from_pdf <- function(pdf_path, output_csv = NULL) {
  if (!file.exists(pdf_path)) {
    cat("Error: PDF file '", pdf_path, "' not found\n", sep = "")
    return(invisible(NULL))
  }
  
  pdf_info <- pdf_info(pdf_path)
  total_pages <- pdf_info$pages
  pages_to_process <- min(5, total_pages)
  
  cat("Processing", pages_to_process, "pages...\n")
  
  all_tables <- list()
  row_counter <- 0
  
  for (page_num in 1:pages_to_process) {
    tryCatch({
      tables <- extract_tables(pdf_path, pages = page_num, method = "lattice")
      
      if (length(tables) > 0) {
        cat("Found", length(tables), "table(s) on page", page_num, "\n")
        
        for (table_num in seq_along(tables)) {
          table_data <- tables[[table_num]]
          
          if (is.matrix(table_data) && nrow(table_data) > 0) {
            for (row_idx in 1:nrow(table_data)) {
              row_counter <- row_counter + 1
              row_data <- c(page_num, table_num, table_data[row_idx, ])
              all_tables[[row_counter]] <- row_data
            }
          }
        }
      }
    }, error = function(e) {
      cat("Warning: Could not extract tables from page", page_num, ":", e$message, "\n")
      
      tryCatch({
        tables <- extract_tables(pdf_path, pages = page_num, method = "stream")
        
        if (length(tables) > 0) {
          cat("Found", length(tables), "table(s) on page", page_num, "(using stream method)\n")
          
          for (table_num in seq_along(tables)) {
            table_data <- tables[[table_num]]
            
            if (is.matrix(table_data) && nrow(table_data) > 0) {
              for (row_idx in 1:nrow(table_data)) {
                row_counter <- row_counter + 1
                row_data <- c(page_num, table_num, table_data[row_idx, ])
                all_tables[[row_counter]] <- row_data
              }
            }
          }
        }
      }, error = function(e2) {
        cat("Warning: Both extraction methods failed for page", page_num, "\n")
      })
    })
  }
  
  if (length(all_tables) == 0) {
    cat("No tables found in the PDF\n")
    return(invisible(NULL))
  }
  
  if (is.null(output_csv)) {
    output_csv <- paste0(tools::file_path_sans_ext(basename(pdf_path)), "_extracted_tables_0_5.csv")
  }
  
  max_cols <- max(sapply(all_tables, length)) - 2
  headers <- c("Page", "Table", paste0("Column", 1:max_cols))
  
  padded_tables <- lapply(all_tables, function(row) {
    if (length(row) < length(headers)) {
      row <- c(row, rep("", length(headers) - length(row)))
    }
    return(row[1:length(headers)])
  })
  
  df <- do.call(rbind, padded_tables)
  colnames(df) <- headers
  df <- as.data.frame(df, stringsAsFactors = FALSE)
  
  write.csv(df, output_csv, row.names = FALSE, fileEncoding = "UTF-8")
  
  cat("Extracted", nrow(df), "rows from tables\n")
  cat("Data saved to:", output_csv, "\n")
  
  return(invisible(df))
}

main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) < 1) {
    cat("Usage: Rscript main.R <pdf_file> [output_csv]\n")
    cat("Example: Rscript main.R document.pdf extracted_data.csv\n")
    return(invisible(NULL))
  }
  
  pdf_file <- args[1]
  output_csv <- if (length(args) > 1) args[2] else NULL
  
  extract_tables_from_pdf(pdf_file, output_csv)
}

if (!interactive()) {
  main()
}