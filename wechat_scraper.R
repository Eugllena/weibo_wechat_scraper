library(rvest)
library(dplyr)
library(stringr)

# Search by Sogou Wechat Search Engine, type in the key words and download all the pages manully.

records <- data_frame()
fd <- "Path to the pages you download."
urls <- list.files(fd)     # Every url is a path to one page. 
for(url in urls){                                                 
  ht <- read_html(url)
  links <- ht %>%
    html_nodes(xpath = "//h3/a") %>%
    html_attr("href")
  for(j in seq_along(links)){
    html <- try(read_html(links[j]))
    if(inherits(html, "try-error")) html <- read_html(links[j], options = "HUGE")    # Some pages are too complex.
    id <- paste0("year-month-", as.character((i - 1) * 10 + j))    # Every wechat page given an unique id in the form year-month-number.
    
    # Extract meta-data

    title <- html %>%
      html_nodes(xpath = "//title") %>%
      html_text()

    ## Check if the page have been remove or some unkowned error.

    if(title == "此文章被第三方评估为不实信息") next
    if(title == "") {title <- html %>%
                     html_nodes(xpath = "//div[@class='global_error_msg warn']") %>%
                     html_text()
	             if(title == "该内容已被发布者删除") next else break	  
		    }

    ## Check page end.

    author <- html %>%
      html_nodes(xpath = "//div[@class='rich_media_meta_list']/em[2]") %>%
      html_text()
    poster <- html %>%
      html_nodes("#post-user") %>%
      html_text()
    date <- html %>%
      html_nodes("#post-date") %>%
      html_text()
    if(!length(date)) date <- html %>%
	                html_nodes("#publish_time") %>%
		        html_text()
    if(!length(author)) author <- NA_character_
    r <- data_frame(id, title, author, poster, date)
    records <- bind_rows(records, r)

    # Extract meta-data end.

    # Extract content.

    div_text <- html %>%
      html_nodes("#js_content") %>%
      html_children() %>%
      html_text() %>%
      .[. != ""]
    path <- "Path of the file to write the content."
    write(div_text, file = path)
  }
}
