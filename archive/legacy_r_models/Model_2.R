library(dplyr)
library(caTools)
library(caret)
library(randomForest)
library(mlbench)

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

data = read.csv("Substructure_final_dataset_for_model.csv")
set.seed(0)
x <- na.omit(data)
para <- dplyr::sample_n(x, size = 2936, replace = TRUE)

in_train_para <- sample(nrow(para), size = as.integer(nrow(para) * 0.7),
                        replace = FALSE)
Train_data <- para[in_train_para, ]
Test_data <- Train_data[-in_train_para, ]
set.seed(0)
model_train <- ranger::ranger(pIC50 ~ ., data = Train_data, write.forest = TRUE,
                              save.memory = TRUE)

saveRDS(model_train, file = "my_random_forest_model.rds")

# Calculate metrics on test data
prediction <- predict(model_train, Test_data)
prediction <- prediction$predictions
value <- data.frame(obs = Test_data$pIC50, pred = prediction)

result <- caret::defaultSummary(value)
result_rm2 <- rm2(value$obs, value$pred)
names(result_rm2) <- "rm2"
results_reverse <- rm2.reverse(value$obs, value$pred)
names(results_reverse) <- "reverse.rm2"
result_average_rm2 <- average.rm2(value$obs, value$pred)
names(result_average_rm2) <- "average.rm2"
result_delta <- delta.rm2(value$obs, value$pred)
names(result_delta) <- "delta.rm"

# Combine all metrics into a single result data frame
result <- data.frame(caret::defaultSummary(value))  # Base metrics
colnames(result)[colnames(result) == "rmse"] <- "RMSE_Mean"
colnames(result)[colnames(result) == "Rsquared"] <- "Rsquared_Mean"
colnames(result)[colnames(result) == "MAE"] <- "MAE"
result$rm2 <- rm2(value$obs, value$pred)
result$reverse.rm2 <- rm2.reverse(value$obs, value$pred)
result$average.rm2 <- average.rm2(value$obs, value$pred)
result$delta.rm2 <- delta.rm2(value$obs, value$pred)

set.seed(0)
confusionMatrix(prediction, Test_data$pIC50)
# Cross-validation
#cv_results <- caret::train(pIC50 ~ ., data = x, method = "ranger", 
                         #  trControl = trainControl(method = "cv", number = 10))
#cv_summary <- caret::summary(cv_results)

# Testing
#test_results <- training_function(x)
