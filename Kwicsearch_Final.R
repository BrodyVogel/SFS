#Counts all occurrences of words from a dictionary in a corpus and collects relevent excerpts. Runtime ~10 minutes 
#for 5,000 files, which varies based on dictionary, size of files, #acronyms, etc. 

library(readtext)
library(quanteda)
library(dplyr)
library(stringr)
library(tm)

DATA_DIR <- "/Users/brodyvogel/Box Sync/Krogh2018/UNSpeeches/" 

#Read the dictionary
## Some notes on the specifics of the Dictionary file:
####   ) Every phrase shoulld be in quotation marks
####   ) Stem terms need a leading underscore, "_", so they can be identified
####   ) Acronyms need leading and/or trailing whitespaces inside the quotes (" IMF", " WTO") so as not to match
####     chunks of words. The trailing whitespace is only necessary in cases like " UPR ", in which " UPR" would
####     hit on things like "uproar".
####   ) At the end, there needs to be an "_END" stem that tells the loops to stop
####   ) Don't forget to replace the test dictionary with whatever one you plan on using
lines <- scan('/Users/brodyvogel/Desktop/Work Study/Dictionary2.txt', character(), quote = '"')

# The pattern matching in the call to kwic() is different from that used in the counting loops. In the counting
# loops, the grep() calls factor in spacing. In kwic(), the pattern matching is on tokens, so, for example, 
# kwic(text, phrase(" IMF "), valuetype = 'glob') won't match "The IMF has..." because it's tokenized " IMF " 
# into ("", IMF, ""). That all goes to say, if you have acronyms that you need to protect - as outlined in the 
# dictionary notes - add them to this list without any spaces, so kwic() can find them. 
# The other little bit - *nationalization, *libearal - is for words that can take prefixes. grep() won't catch them. Be 
# conservative, here, though: Each addition of this type of word slows the runtime, because the wildcard '*',
# which will shortly be added to the end of each word, will cause kwic() to constantly look both forwards and 
# backwards in the string its parsing. 
# I guess you could just treat all the acronyms the same (pad both sides with whitespace in the dictionary
# and add them all to this list), but I have a feeling that'd slow things down considerably. 

prob_acronyms <- c("IMF", "IDA", "BIT", "ICC", "TRIPS", "ICTY", "ICTR", "UPR", "WTO", "*nationalization", "*liberal")

#Gets the stems
stems <- lines[grep("_", lines)]

#Gets the words that are not stems
notStems <- removeWords(lines, stems)[removeWords(lines, stems) != ""]

#Prepares the words that are not stems to match word stems in the kwic() glob search. It really just adds a 
#'*' so as to catch other cases of the words.
notStems1 <- c()
for (x in notStems) {
  
  add <- paste(x, "*", sep = "")
  notStems1 <- c(notStems1, add)

}

#Creates the dataframe that will hold the word counts
counts <- setNames(data.frame(matrix(ncol = length(stems) + 1, nrow = 0)), c('Doc', sub("_", "", stems)))

#This reads in the document names 
docs <- list.files(DATA_DIR, full.names = TRUE, recursive=TRUE, pattern="*.txt")

#This counts the occurrences of each term. Fills in the dataframe.
place_holder <- 1
for (doc in docs){
  
  txt <- readChar(doc, file.info(doc)$size)
  txt <- str_replace_all(txt, '[\r\n]', ' ')
  txt <- str_replace_all(txt, '\t', ' ')
  txt <- gsub("\\s+", " ", txt)
  
  counts[place_holder, 1] <- basename(doc)
  
  counter <- 2
  num_words <- 0
  
  for (word in lines) {
    #Again, basically count the words until you hit a stem, in which case move to the next column
    if (grepl("_", word) == TRUE & match(word, lines) == 1){
      
      next
    }
    else if (grepl("_", word) == TRUE & match(word, lines) != 1){
      
      counts[place_holder, counter] <- num_words
      counter <- counter + 1
      num_words <- 0
    } 
    else {
      #If it's not a stem, count it
      num_words <- num_words + str_count(txt, fixed(word, ignore_case = TRUE))
    }
  }
  place_holder <- place_holder + 1
}

#Throw out the "END" column again
counts <- counts[-c(length(stems)+1)]

str_split_fixed(counts$doc, "_", 3)

#Makes the counts and forthcoming corpus names uniform
counts$Doc <- str_replace(counts$Doc, "_[0-9]*_", "_")
counts$Doc <- str_replace(counts$Doc, ".txt", "")

ungd <- readtext(paste0(DATA_DIR, "Converted sessions/*"), 
                       docvarsfrom = "filenames", 
                       dvsep="_", 
                       docvarnames = c("Country", "Session", "Year"))

#changing row.names to have only country_year, rather than folder pathway from `readtext`.
row.names(ungd) <- str_replace(str_replace(sapply(str_split(ungd$doc_id, "/"),`[`,2), ".txt", ""), "_\\d{2}", "")

ungd_corpus <- corpus(ungd, text_field = "text")

#I changed this to have more natural-language-looking tokens, which didn't seem to affect the runtime.
#Change back if you want - I don't think it'll cause any problems. 
tok <- tokens(ungd_corpus, what = "word")

#Build the regex for the kwic search
carrier <- c(prob_acronyms)

for (x in notStems1) {
  carrier <- c(carrier, phrase(x))
}

#kwic search
IMFdata <- data.frame(kwic(tok, carrier, window = 50, valuetype = "glob"))


#Creates the excerpt and keys columns
counts$Keys <- c(1)
counts$Excerpt <- c(1)

ro <- 1

#As you suggested, it mostly just keeps track of the indexes for the first and last occurrence of a buzzword. 
#Then, at the end, it adds the speech indexed by those two positions. 
for (speech in counts$Doc) {
  if (speech %in% IMFdata$docname) {
    start <- min(IMFdata[IMFdata$docname == speech, 2])
    if (start > 50) {
      start <- start - 50
    }
    else {
      start <- 1
    }
    finish <- max(IMFdata[IMFdata$docname == speech, 3])
    if (finish < length(as.character(tok[speech])) - 50) {
      finish <- finish + 50
    }
    else {
      finish <- length(as.character(tok[speech]))
    }
    excerpt <- paste(as.character(tok[speech])[start:finish], collapse = " ")
    counts[ro, "Excerpt"] <- excerpt
    counts[ro, "Keys"] <- paste(unique(c(IMFdata[IMFdata$docname == speech, 5])), collapse = " , ")
  }
  else {
    excerpt <- ""
    counts[ro, "Excerpt"] <- excerpt
    # if you want each keyword, including repetitions, take out the unique(c()) call
    counts[ro, "Keys"] <- paste(unique(c(IMFdata[IMFdata$docname == speech, 5])), collapse = " , ")
}
  
  ro <- ro + 1
  print(ro)
}

# This isn't perfect. There were still 2 cases where grep() matched a word and kwic() didn't that I had to fix 
# manually (both unrelated to the topic). Just somthing to watch out for. Fiddling with the dictionary / prob_acronyms 
# could catch all of these, but it might make the runtime a little unsavory.


#pipe it to a .csv 
write.csv(counts, "/Users/brodyvogel/Desktop/Excerpts.csv")
