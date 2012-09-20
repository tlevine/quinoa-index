get.zip.code <- function(messy.zip) {
  sub('[^0-9]*([0-9]{5}).*', '\\1', messy.zip)
}

# Get the zip code
aff$zip <- get.zip.code(aff$GCT_STUB.display.label.1)
yoga$zip <- get.zip.code(yoga$Zip)
#nop$zip <- get.zip.code(
#ccof <- get.zip.code(
