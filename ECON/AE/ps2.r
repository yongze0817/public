install.packages("readxl")
install.packages("grf")
library(readxl)
library(grf)

data <- read_excel("Your_own_directory/Forest.xlsx")

Y <- as.matrix(data$outcome)        # Outcome variable
W <- as.matrix(data$treatment)      # Treatment variable
X <- as.matrix(data[, paste0("X", 1:10)])  # Control variables X1 to X10

causal_forest_model <- causal_forest(X, Y, W, num.trees = 4000)

# Estimate CATE with confidence intervals
cate_predictions <- predict(causal_forest_model, estimate.variance = TRUE)
cate <- cate_predictions$predictions
cate_variance <- cate_predictions$variance.estimates

# 95% confidence intervals
cate_ci_lower <- cate - 1.96 * sqrt(cate_variance)
cate_ci_upper <- cate + 1.96 * sqrt(cate_variance)

# Plot CATE with confidence interval
plot(cate, type = "l", col = "blue", ylab = "CATE", xlab = "Observation Index")
lines(cate_ci_lower, col = "red", lty = 2) # Lower bound of CI
lines(cate_ci_upper, col = "red", lty = 2) # Upper bound of CI
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

