install.packages("readxl")
install.packages("grf")
library(readxl)
library(grf)

data <- read_excel("C:/Users/rmaat/Downloads/Forest.xlsx")

Y <- as.matrix(data$Y)        # Outcome variable
D <- as.matrix(data$D)      # Treatment variable
W <- as.matrix(data[, paste0("W", 1:10)])  # Control variables X1 to X10

W.test <- matrix(0, 101, 10)
W.test[, 1] <- seq(0, 2, length.out = 101)

#CH
tau.forest <- causal_forest(W, Y, D, num.trees = 4000)
tau.hat <- predict(tau.forest, W.test, estimate.variance = TRUE)
sigma.hat <- sqrt(tau.hat$variance.estimates)
plot(W.test[, 1], tau.hat$predictions, ylim =
       range(tau.hat$predictions + 1.96 * sigma.hat,
             tau.hat$predictions - 1.96 * sigma.hat, 0, 2),
     xlab = "W1", ylab = "CATE", type = "l")
lines(W.test[, 1], tau.hat$predictions + 1.96 * sigma.hat, col = 1,
      lty = 2)
lines(W.test[, 1], tau.hat$predictions - 1.96 * sigma.hat, col = 1,
      lty = 2)

ate <- average_treatment_effect(tau.forest,target.sample = "all",method="AIPW")
ate_estimate <- ate[1]                  # ATE estimate
ate_ci_lower <- ate[1] - 1.96 * ate[2]  # Lower bound of 95% CI
ate_ci_upper <- ate[1] + 1.96 * ate[2]  # Upper bound of 95% CI

cat("ATE Estimate:", ate_estimate, "\n")
cat("95% Confidence Interval for ATE:", ate_ci_lower, "to", ate_ci_upper, "\n")

p_value <- 2 * (1 - pnorm(abs((2-ate_estimate) / ate[2]))
cat("P-value(2):", p_value, "\n")
cat("Reject H0 at 5% significance level:", p_value < 0.05, "\n")

p_value <- 2 * (1 - pnorm(abs((1-ate_estimate) / ate[2])))
cat("P-value(1):", p_value, "\n")
cat("Reject H0 at 5% significance level:", p_value < 0.05, "\n")

p_value <- 2 * (1 - pnorm(abs(ate_estimate / ate[2])))
cat("P-value(0):", p_value, "\n")









#GPT
# Estimate CATE with confidence intervals
causal_forest_model <- causal_forest(W, Y, D, num.trees = 4000)
cate_predictions <- predict(causal_forest_model, estimate.variance = TRUE)
cate <- cate_predictions$predictions
cate_variance <- cate_predictions$variance.estimates

# 95% confidence intervals
cate_ci_lower <- cate - 1.96 * sqrt(cate_variance)
cate_ci_upper <- cate + 1.96 * sqrt(cate_variance)

# Plot CATE with confidence interval
plot(W.test[, 1], cate, ylim =
       range(cate_ci_upper,
             cate_ci_lower, 0, 2),
     type = "l", col = "blue", ylab = "CATE", xlab = "w1")
lines(W.test[, 1],cate_ci_lower, col = "red", lty = 2) # Lower bound of CI
lines(W.test[, 1],cate_ci_upper, col = "red", lty = 2) # Upper bound of CI
legend("topright", legend = c("CATE", "95% Confidence Interval"),
       col = c("blue", "red"), lty = c(1, 2))



ate <- average_treatment_effect(causal_forest_model, target.sample = "all")
ate_estimate <- ate[1]                  # ATE estimate
ate_ci_lower <- ate[1] - 1.96 * ate[2]  # Lower bound of 95% CI
ate_ci_upper <- ate[1] + 1.96 * ate[2]  # Upper bound of 95% CI

cat("ATE Estimate:", ate_estimate, "\n")
cat("95% Confidence Interval for ATE:", ate_ci_lower, "to", ate_ci_upper, "\n")

p_value <- 2 * (1 - pnorm(abs(ate_estimate / ate[2])))

cat("P-value:", p_value, "\n")
cat("Reject H0 at 5% significance level:", p_value < 0.05, "\n")
cat("Reject H0 at 1% significance level:", p_value < 0.01, "\n")

