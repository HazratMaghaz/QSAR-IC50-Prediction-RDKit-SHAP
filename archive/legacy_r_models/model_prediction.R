library(dplyr)
library(caTools)
library(caret)
library(randomForest)
library(mlbench)

# Load necessary libraries
library(randomForest)

# Function for calculating R-squared
R2 <- function(y, equation, ...) {
  1 - (sum((y - predict(equation))^2)/sum((y - mean(y))^2))
}

# Function to calculate custom RM2 metrics
rm2 <- function(y, x, ...) {
  if ((R2(y, (lm(y ~ x)))) > R2(y, (lm(y ~ -1 + x)))) {
    return(R2(y, (lm(y ~ x))) * (1 - (sqrt(R2(y, (lm(y ~ x))) - R2(y,
                                                                   (lm(y ~ -1 + x)))))))
  } else {
    return(R2(y, (lm(y ~ x))))
  }
}

rm2.reverse <- function(y, x, ...) {
  return(R2(x, (lm(x ~ y))) * (1 - (sqrt(R2(x, (lm(x ~ y))) - R2(x, (lm(x ~ -1 + y)))))))
}

average.rm2 <- function(y, x, ...) {
  if ((R2(y, (lm(y ~ x)))) > R2(y, (lm(y ~ -1 + x)))) {
    return(((R2(y, (lm(y ~ x))) * (1 - (sqrt(R2(y, (lm(y ~ x))) - R2(y,
                                                                     (lm(y ~ -1 + x)))))) + R2(x, (lm(x ~ y))) * (1 - (sqrt(R2(x,
                                                                                                                               (lm(x ~ y))) - R2(x, (lm(x ~ -1 + y))))))))/2)
  } else {
    return(((R2(y, (lm(y ~ x)))) + (R2(x, (lm(x ~ y))) * (1 - (sqrt(R2(x,
                                                                       (lm(x ~ y))) - R2(x, (lm(x ~ -1 + y))))))))/2)
  }
}

delta.rm2 <- function(y, x, ...) {
  if ((R2(y, (lm(y ~ x)))) > R2(y, (lm(y ~ -1 + x)))) {
    return(abs((R2(y, (lm(y ~ x))) * (1 - (sqrt(R2(y, (lm(y ~ x))) -
                                                  R2(y, (lm(y ~ -1 + x)))))) - R2(x, (lm(x ~ y))) * (1 - (sqrt(R2(x,
                                                                                                                  (lm(x ~ y))) - R2(x, (lm(x ~ -1 + y)))))))))
  } else {
    return(abs((R2(y, (lm(y ~ x)))) - (R2(x, (lm(x ~ y))) * (1 - (sqrt(R2(x,
                                                                          (lm(x ~ y))) - R2(x, (lm(x ~ -1 + y)))))))))
  }
}

# Function for calculating mean and standard deviation
mean_and_sd <- function(x) {
  c(round(rowMeans(x, na.rm = TRUE), digits = 2), round(genefilter::rowSds(x,
                                                                           na.rm = TRUE), digits = 2))
}

# Load the saved model
loaded_model <- readRDS("my_random_forest_model.rds")

# reading data
unseen_data <- read.csv("unseen_npass_opt_data.csv")

# Extract the columns you need for prediction
data_unseen <- unseen_data[, 3:ncol(unseen_data)]

# Make predictions
predictions <- predict(loaded_model, data = data_unseen)

# Combine predictions with the relevant columns from unseen_data
df <- data.frame(Compound_Name = unseen_data$comp_name, 
                 mol = unseen_data$mol, 
                 pIC50 = predictions)

# saving dataframe to csv
write.csv(df, "npass_predict_file.csv", row.names = FALSE)

