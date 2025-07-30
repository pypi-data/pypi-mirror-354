#include "../include/garch_calculator.h"
#include <cmath>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <iostream>
#include <sstream>
#include <random>
#include <limits>
#include <boost/math/special_functions/gamma.hpp>
#include <boost/math/special_functions/digamma.hpp>
#include <boost/functional/hash.hpp>

namespace garch {

// === 工具函数实现 ===

int64_t GarchCalculator::getCurrentTimestamp() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::system_clock::now().time_since_epoch()
    ).count();
}

double GarchCalculator::calculateLogReturn(double current_price, double previous_price) {
    if (previous_price <= 0.0 || current_price <= 0.0) {
        return 0.0;
    }
    return std::log(current_price / previous_price);
}

double GarchCalculator::calculateGedDensity(double x, double sigma, double nu) {
    // 广义误差分布 (GED) 密度函数 - 匹配 arch 库实现
    // 使用缓存优化重复计算
    
    struct PairHash {
        size_t operator()(const std::pair<double, double>& p) const {
            size_t seed = 0;
            boost::hash_combine(seed, p.first);
            boost::hash_combine(seed, p.second);
            return seed;
        }
    };
    
    static thread_local std::unordered_map<std::pair<double, double>, std::pair<double, double>, PairHash> cache;
    
    auto key = std::make_pair(nu, sigma);
    auto it = cache.find(key);
    
    double lambda, log_normalizing_constant;
    
    if (it != cache.end()) {
        lambda = it->second.first;
        log_normalizing_constant = it->second.second;
    } else {
        // 计算 λ = sqrt[Γ(1/ν) / Γ(3/ν)] - 匹配 arch 库
        double log_gamma_1_nu = std::lgamma(1.0/nu);
        double log_gamma_3_nu = std::lgamma(3.0/nu);
        lambda = std::sqrt(std::exp(log_gamma_1_nu - log_gamma_3_nu));
        
        // 归一化常数对数: log[ν / (2^(1+1/ν) * Γ(1/ν) * λ)]
        log_normalizing_constant = std::log(nu) - (1.0 + 1.0/nu) * std::log(2.0) 
                                 - log_gamma_1_nu - std::log(lambda);
        
        // 缓存结果
        if (cache.size() < 1000) {
            cache[key] = std::make_pair(lambda, log_normalizing_constant);
        }
    }
    
    // 计算标准化值: z = x / (σ * λ)
    double z = x / (sigma * lambda);
    
    // 计算 |z|^ν - 优化常见 nu 值
    double abs_z_pow_nu;
    if (std::abs(nu - 2.0) < 1e-10) {
        // nu = 2.0 (正态分布)
        abs_z_pow_nu = z * z;
    } else if (std::abs(nu - 1.0) < 1e-10) {
        // nu = 1.0 (双指数分布)
        abs_z_pow_nu = std::abs(z);
    } else {
        abs_z_pow_nu = std::pow(std::abs(z), nu);
    }
    
    // 返回对数密度 (用于避免下溢)
    double log_density = log_normalizing_constant - std::log(sigma) - 0.5 * abs_z_pow_nu;
    return log_density;
}

// === GarchCalculator 实现 ===

GarchCalculator::GarchCalculator(size_t history_size, size_t min_samples)
    : price_history_(history_size)
    , parameters_()
    , current_variance_(parameters_.getUnconditionalVariance())
    , min_samples_(min_samples)
    , thread_safe_(false)
    , last_update_time_(0)
    , update_count_(0) {
    
    variance_history_.reserve(history_size);
}

bool GarchCalculator::addPricePoint(double price, int64_t timestamp) {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    if (price <= 0.0) {
        return false;
    }
    
    if (timestamp == 0) {
        timestamp = getCurrentTimestamp();
    }
    
    // 计算对数收益率
    double log_return = 0.0;
    if (!price_history_.empty()) {
        log_return = calculateLogReturn(price, price_history_.back().price);
    }
    
    // 添加数据点
    price_history_.push_back(PricePoint(timestamp, price, log_return));
    
    // 更新时间戳
    last_update_time_ = timestamp;
    update_count_++;
    
    return true;
}

bool GarchCalculator::addPricePoints(const std::vector<double>& prices, 
                                    const std::vector<int64_t>& timestamps) {
    if (prices.empty()) {
        return false;
    }
    
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    bool use_timestamps = !timestamps.empty() && timestamps.size() == prices.size();
    
    for (size_t i = 0; i < prices.size(); ++i) {
        int64_t ts = use_timestamps ? timestamps[i] : getCurrentTimestamp();
        
        if (prices[i] <= 0.0) {
            return false;
        }
        
        // 计算对数收益率
        double log_return = 0.0;
        if (!price_history_.empty()) {
            log_return = calculateLogReturn(prices[i], price_history_.back().price);
        }
        
        // 添加数据点
        price_history_.push_back(PricePoint(ts, prices[i], log_return));
        last_update_time_ = ts;
        update_count_++;
    }
    
    return true;
}

// === 新增：直接添加收益率数据的函数实现 ===

bool GarchCalculator::addReturn(double return_value, int64_t timestamp) {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    if (!std::isfinite(return_value)) {
        return false;
    }
    
    if (timestamp == 0) {
        timestamp = getCurrentTimestamp();
    }
    
    // 直接使用收益率，不需要价格计算
    // 设置一个虚拟价格序列以保持数据结构兼容性
    double dummy_price = price_history_.empty() ? 100.0 : 
                        price_history_.back().price * (1.0 + return_value);
    
    // 添加数据点，直接使用收益率
    price_history_.push_back(PricePoint(timestamp, dummy_price, return_value));
    
    // 更新时间戳
    last_update_time_ = timestamp;
    update_count_++;
    
    return true;
}

bool GarchCalculator::addReturns(const std::vector<double>& returns, 
                                 const std::vector<int64_t>& timestamps) {
    if (returns.empty()) {
        return false;
    }
    
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    bool use_timestamps = !timestamps.empty() && timestamps.size() == returns.size();
    
    for (size_t i = 0; i < returns.size(); ++i) {
        int64_t ts = use_timestamps ? timestamps[i] : getCurrentTimestamp();
        
        if (!std::isfinite(returns[i])) {
            return false;
        }
        
        // 直接使用收益率，生成虚拟价格以保持兼容性
        double dummy_price = price_history_.empty() ? 100.0 : 
                            price_history_.back().price * (1.0 + returns[i]);
        
        // 添加数据点，直接使用收益率
        price_history_.push_back(PricePoint(ts, dummy_price, returns[i]));
        last_update_time_ = ts;
        update_count_++;
    }
    
    return true;
}

bool GarchCalculator::updateModel() {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    if (price_history_.empty()) {
        return false;
    }
    
    // 获取最新的对数收益率
    double latest_return = price_history_.back().log_return;
    
    // 使用 GARCH(1,1) 方程更新方差
    // σ²_t = ω + α * ε²_(t-1) + β * σ²_(t-1)
    current_variance_ = parameters_.omega + 
                       parameters_.alpha * latest_return * latest_return + 
                       parameters_.beta * current_variance_;
    
    // 确保方差为正
    current_variance_ = std::max(current_variance_, 1e-8);
    
    // 记录方差历史
    variance_history_.push_back(current_variance_);
    
    // 限制历史长度
    if (variance_history_.size() > price_history_.capacity()) {
        variance_history_.erase(variance_history_.begin());
    }
    
    return true;
}

EstimationResult GarchCalculator::estimateParameters() {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    if (!hasEnoughData()) {
        return EstimationResult();
    }
    
    auto start_time = std::chrono::high_resolution_clock::now();
    EstimationResult result = optimizeParameters();
    auto end_time = std::chrono::high_resolution_clock::now();
    
    result.convergence_time_ms = std::chrono::duration<double, std::milli>(
        end_time - start_time
    ).count();
    
    if (result.converged) {
        parameters_ = result.parameters;
        // 重新计算当前方差
        current_variance_ = std::max(
            result.parameters.getUnconditionalVariance(),
            current_variance_ * 0.1
        );
    }
    
    return result;
}

EstimationResult GarchCalculator::optimizeParameters() {
    // 提取对数收益率
    std::vector<double> log_returns;
    log_returns.reserve(price_history_.size() - 1);
    
    for (size_t i = 1; i < price_history_.size(); ++i) {
        log_returns.push_back(price_history_[i].log_return);
    }
    
    if (log_returns.size() < 10) {
        return EstimationResult();
    }
    
    // 计算样本统计量
    double mean_return = std::accumulate(log_returns.begin(), log_returns.end(), 0.0) / log_returns.size();
    
    double sample_variance = 0.0;
    for (double ret : log_returns) {
        double diff = ret - mean_return;
        sample_variance += diff * diff;
    }
    sample_variance /= (log_returns.size() - 1);
    
    // 准备多个初始值候选 (匹配 arch 库的标准GARCH(1,1)初始值)
    std::vector<GarchParameters> initial_candidates;
    
    // 候选1: 标准GARCH(1,1) - 匹配arch库的默认偏好
    GarchParameters standard_garch;
    standard_garch.omega = sample_variance * 0.01;    // 小的omega (1%样本方差)
    standard_garch.alpha = 0.1;                       // 中等ARCH效应
    standard_garch.beta = 0.85;                       // 强GARCH效应 - 关键!
    standard_garch.nu = 1.5;                          // 适中的GED形状参数
    initial_candidates.push_back(standard_garch);
    
    // 候选2: 高持续性GARCH(1,1)
    GarchParameters high_persist_garch;
    high_persist_garch.omega = sample_variance * 0.005;
    high_persist_garch.alpha = 0.05;
    high_persist_garch.beta = 0.9;                    // 更高的持续性
    high_persist_garch.nu = 2.0;
    initial_candidates.push_back(high_persist_garch);
    
    // 候选3: 平衡型GARCH(1,1)
    GarchParameters balanced_garch;
    balanced_garch.omega = sample_variance * 0.02;
    balanced_garch.alpha = 0.15;
    balanced_garch.beta = 0.8;                        // 平衡的alpha和beta
    balanced_garch.nu = 1.8;
    initial_candidates.push_back(balanced_garch);
    
    // 候选4: 低持续性GARCH(1,1) 
    GarchParameters low_persist_garch;
    low_persist_garch.omega = sample_variance * 0.03;
    low_persist_garch.alpha = 0.2;
    low_persist_garch.beta = 0.7;                     // 较低但仍有意义的beta
    low_persist_garch.nu = 1.2;
    initial_candidates.push_back(low_persist_garch);
    
    // 候选5: 保守型GARCH(1,1) - 作为备选
    GarchParameters conservative_garch;
    conservative_garch.omega = sample_variance * 0.01;
    conservative_garch.alpha = 0.08;
    conservative_garch.beta = 0.88;                   // 高持续性，低冲击
    conservative_garch.nu = 1.6;
    initial_candidates.push_back(conservative_garch);
    
    // 对每个初始值使用BFGS优化
    double best_likelihood = -std::numeric_limits<double>::infinity();
    EstimationResult best_result;
    
    for (const auto& initial_params : initial_candidates) {
        // 确保参数有效
        if (!initial_params.isValid()) {
            continue;
        }
        
        // 确保能计算出有效的似然值
        double test_ll = calculateLogLikelihood(initial_params);
        if (!std::isfinite(test_ll) || test_ll < -1e6) {
            continue;
        }
        
        EstimationResult result = optimizeWithBFGS(initial_params);
        
        if (result.log_likelihood > best_likelihood) {
            best_likelihood = result.log_likelihood;
            best_result = result;
        }
    }
    
    // 如果所有BFGS尝试都失败，返回最佳初始参数
    if (best_likelihood == -std::numeric_limits<double>::infinity()) {
        for (const auto& initial_params : initial_candidates) {
            if (!initial_params.isValid()) continue;
            
            double test_ll = calculateLogLikelihood(initial_params);
            if (std::isfinite(test_ll) && test_ll > best_likelihood) {
                best_likelihood = test_ll;
                best_result.parameters = initial_params;
                best_result.log_likelihood = test_ll;
                best_result.iterations = 0;
                best_result.converged = false;
                
                // 计算信息准则
                int num_params = 4;
                best_result.aic = -2 * test_ll + 2 * num_params;
                best_result.bic = -2 * test_ll + num_params * std::log(price_history_.size() - 1);
            }
        }
    }
    
    return best_result;
}

GarchParameters GarchCalculator::constrainParameters(const GarchParameters& params) const {
    GarchParameters constrained = params;
    
    // 参数约束 - 匹配 arch 库的约束
    // omega > 0: 确保无条件方差为正，使用更宽松的范围
    constrained.omega = std::max(1e-8, std::min(1.0, constrained.omega));
    
    // alpha >= 0: ARCH效应非负，范围[0, 1)
    constrained.alpha = std::max(0.0, std::min(0.999, constrained.alpha));
    
    // beta >= 0: GARCH效应非负，范围[0, 1)
    constrained.beta = std::max(0.0, std::min(0.999, constrained.beta));
    
    // nu > 1.0: GED形状参数约束，合理范围
    constrained.nu = std::max(1.001, std::min(50.0, constrained.nu));
    
    // 平稳性约束: alpha + beta < 1 (arch 库的核心约束)
    if (constrained.alpha + constrained.beta >= 0.9999) {
        double sum = constrained.alpha + constrained.beta;
        double scale = 0.9999 / sum;
        constrained.alpha *= scale;
        constrained.beta *= scale;
    }
    
    return constrained;
}

VolatilityForecast GarchCalculator::forecastVolatility(int horizon) const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    VolatilityForecast forecast;
    forecast.timestamp = getCurrentTimestamp();
    forecast.forecast_horizon = horizon;
    
    if (!hasEnoughData() || horizon <= 0) {
        return forecast;
    }
    
    // 计算多步预测
    double persistence = parameters_.getPersistence();
    double unconditional_var = parameters_.getUnconditionalVariance();
    
    double forecast_var;
    if (std::abs(persistence - 1.0) < 1e-10) {
        // IGARCH 情况
        forecast_var = current_variance_ + horizon * parameters_.omega;
    } else {
        // 标准 GARCH 多步预测
        double persistence_power = std::pow(persistence, horizon);
        forecast_var = unconditional_var + 
                      persistence_power * (current_variance_ - unconditional_var);
    }
    
    // 边界检查
    forecast_var = std::max(forecast_var, 1e-8);
    forecast_var = std::min(forecast_var, 1e2);
    
    forecast.variance = forecast_var;
    forecast.volatility = std::sqrt(forecast_var);
    forecast.confidence_score = calculateConfidenceScore();
    
    return forecast;
}

double GarchCalculator::calculateLogLikelihood() const {
    return calculateLogLikelihood(parameters_);
}

double GarchCalculator::calculateGedLogLikelihood(const std::vector<double>& residuals,
                                                   const std::vector<double>& sigma_t,
                                                   double nu) const {
    if (residuals.size() != sigma_t.size() || residuals.empty()) {
        return -std::numeric_limits<double>::infinity();
    }
    
    // GED对数似然计算 - 严格匹配arch库的实现
    // arch库的GED参数化：pdf = ν/(2^(1+1/ν) * λ * Γ(1/ν) * σ) * exp(-0.5 * |ε/(λσ)|^ν)
    // 其中 λ = sqrt(Γ(1/ν)/Γ(3/ν))
    
    double log_gamma_1_nu = std::lgamma(1.0/nu);
    double log_gamma_3_nu = std::lgamma(3.0/nu);
    
    // λ = sqrt(Γ(1/ν)/Γ(3/ν)) - arch库的标准化因子
    double lambda = std::sqrt(std::exp(log_gamma_1_nu - log_gamma_3_nu));
    
    // 对数归一化常数：log[ν/(2^(1+1/ν) * λ * Γ(1/ν))]
    double log_constant = std::log(nu) - (1.0 + 1.0/nu) * std::log(2.0) 
                         - std::log(lambda) - log_gamma_1_nu;
    
    double log_likelihood = 0.0;
    
    for (size_t t = 0; t < residuals.size(); ++t) {
        if (sigma_t[t] <= 0.0) {
            return -std::numeric_limits<double>::infinity();
        }
        
        // 标准化残差：z = ε_t / (λ * σ_t)
        double z = residuals[t] / (lambda * sigma_t[t]);
        
        // 计算 |z|^ν
        double abs_z_pow_nu;
        if (std::abs(nu - 2.0) < 1e-12) {
            // nu = 2.0 (正态分布)
            abs_z_pow_nu = z * z;
        } else if (std::abs(nu - 1.0) < 1e-12) {
            // nu = 1.0 (拉普拉斯分布)
            abs_z_pow_nu = std::abs(z);
        } else {
            abs_z_pow_nu = std::pow(std::abs(z), nu);
        }
        
        // 对数似然贡献：log_constant - log(σ_t) - 0.5 * |z|^ν
        double ll_t = log_constant - std::log(sigma_t[t]) - 0.5 * abs_z_pow_nu;
        
        if (!std::isfinite(ll_t) || ll_t < -100.0) {  // 避免极端值
            return -std::numeric_limits<double>::infinity();
        }
        
        log_likelihood += ll_t;
    }
    
    return log_likelihood;
}

std::vector<double> GarchCalculator::calculateConditionalVariances(
    const std::vector<double>& residuals, 
    const GarchParameters& params) const {
    
    if (residuals.empty()) {
        return {};
    }
    
    std::vector<double> sigma2(residuals.size());
    
    // 初始条件方差 - 使用无条件方差 (匹配 arch 库)
    sigma2[0] = params.getUnconditionalVariance();
    
    // GARCH(1,1) 递归: σ²_t = ω + α * ε²_{t-1} + β * σ²_{t-1}
    for (size_t t = 1; t < residuals.size(); ++t) {
        sigma2[t] = params.omega + 
                   params.alpha * residuals[t-1] * residuals[t-1] + 
                   params.beta * sigma2[t-1];
        
        // 确保方差为正
        sigma2[t] = std::max(sigma2[t], 1e-8);
    }
    
    return sigma2;
}

double GarchCalculator::calculateLogLikelihood(const GarchParameters& params) const {
    if (!params.isValid()) {
        return -std::numeric_limits<double>::infinity();
    }
    
    // 提取对数收益率
    std::vector<double> residuals;
    for (size_t i = 1; i < price_history_.size(); ++i) {
        residuals.push_back(price_history_[i].log_return);
    }
    
    if (residuals.empty()) {
        return -std::numeric_limits<double>::infinity();
    }
    
    // 计算条件方差序列
    std::vector<double> sigma2 = calculateConditionalVariances(residuals, params);
    
    // 转换为标准差
    std::vector<double> sigma_t(sigma2.size());
    for (size_t i = 0; i < sigma2.size(); ++i) {
        sigma_t[i] = std::sqrt(sigma2[i]);
    }
    
    // 计算 GED 对数似然
    return calculateGedLogLikelihood(residuals, sigma_t, params.nu);
}

// === 访问器方法 ===

void GarchCalculator::setParameters(const GarchParameters& params) {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    parameters_ = params;
    current_variance_ = params.getUnconditionalVariance();
}

GarchParameters GarchCalculator::getParameters() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    return parameters_;
}

void GarchCalculator::resetParameters() {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    parameters_ = GarchParameters();
    current_variance_ = parameters_.getUnconditionalVariance();
}

double GarchCalculator::getCurrentVariance() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    return current_variance_;
}

double GarchCalculator::getCurrentVolatility() const {
    return std::sqrt(getCurrentVariance());
}

size_t GarchCalculator::getDataSize() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    return price_history_.size();
}

std::vector<double> GarchCalculator::getLogReturns() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    std::vector<double> returns;
    returns.reserve(price_history_.size() - 1);
    
    for (size_t i = 1; i < price_history_.size(); ++i) {
        returns.push_back(price_history_[i].log_return);
    }
    
    return returns;
}

std::vector<double> GarchCalculator::getVarianceSeries() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    return variance_history_;
}

bool GarchCalculator::hasEnoughData() const {
    return price_history_.size() >= min_samples_;
}

double GarchCalculator::calculateAIC() const {
    double ll = calculateLogLikelihood();
    return -2 * ll + 2 * 4;  // 4 参数
}

double GarchCalculator::calculateBIC() const {
    double ll = calculateLogLikelihood();
    int n = static_cast<int>(price_history_.size() - 1);
    return -2 * ll + 4 * std::log(n);
}

double GarchCalculator::calculateConfidenceScore() const {
    if (!hasEnoughData()) {
        return 0.0;
    }
    
    double sample_ratio = std::min(1.0, 
        static_cast<double>(price_history_.size()) / (min_samples_ * 2)
    );
    
    bool params_valid = parameters_.isValid();
    double confidence = params_valid ? 0.5 + 0.5 * sample_ratio : 0.2;
    
    return confidence;
}

void GarchCalculator::setHistorySize(size_t size) {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    boost::circular_buffer<PricePoint> new_buffer(size);
    
    // 复制现有数据
    for (const auto& point : price_history_) {
        new_buffer.push_back(point);
    }
    
    price_history_ = std::move(new_buffer);
}

void GarchCalculator::setMinSamples(size_t min_samples) {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    min_samples_ = min_samples;
}

std::string GarchCalculator::getConfigInfo() const {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    std::ostringstream oss;
    oss << "GARCH Calculator Configuration:\n";
    oss << "  History Size: " << price_history_.capacity() << "\n";
    oss << "  Min Samples: " << min_samples_ << "\n";
    oss << "  Current Data Points: " << price_history_.size() << "\n";
    oss << "  Thread Safe: " << (thread_safe_ ? "Yes" : "No") << "\n";
    oss << "  Parameters: ω=" << parameters_.omega 
        << ", α=" << parameters_.alpha 
        << ", β=" << parameters_.beta 
        << ", ν=" << parameters_.nu << "\n";
    oss << "  Current Variance: " << current_variance_ << "\n";
    oss << "  Update Count: " << update_count_;
    
    return oss.str();
}

void GarchCalculator::setThreadSafe(bool enable) {
    thread_safe_ = enable;
}

void GarchCalculator::clear() {
    if (thread_safe_) {
        std::lock_guard<std::mutex> lock(mutex_);
    }
    
    price_history_.clear();
    variance_history_.clear();
    current_variance_ = parameters_.getUnconditionalVariance();
    last_update_time_ = 0;
    update_count_ = 0;
}

// === 工具函数实现 ===

BasicStats calculateBasicStats(const std::vector<double>& data) {
    BasicStats stats;
    stats.count = data.size();
    
    if (data.empty()) {
        return stats;
    }
    
    // 计算均值
    stats.mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    
    // 计算方差和更高阶矩
    double sum_sq = 0.0;
    double sum_cube = 0.0;
    double sum_fourth = 0.0;
    
    for (double x : data) {
        double diff = x - stats.mean;
        double diff_sq = diff * diff;
        sum_sq += diff_sq;
        sum_cube += diff_sq * diff;
        sum_fourth += diff_sq * diff_sq;
    }
    
    stats.variance = sum_sq / (data.size() - 1);
    stats.std_dev = std::sqrt(stats.variance);
    
    // 偏度和峰度
    if (stats.std_dev > 0) {
        double n = static_cast<double>(data.size());
        stats.skewness = (sum_cube / n) / std::pow(stats.std_dev, 3);
        stats.kurtosis = (sum_fourth / n) / std::pow(stats.variance, 2) - 3.0;
    }
    
    return stats;
}

std::vector<double> calculateAutocorrelation(const std::vector<double>& data, int max_lag) {
    std::vector<double> autocorr(max_lag + 1, 0.0);
    
    if (data.size() <= static_cast<size_t>(max_lag)) {
        return autocorr;
    }
    
    // 计算均值
    double mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    
    // 计算方差
    double variance = 0.0;
    for (double x : data) {
        double diff = x - mean;
        variance += diff * diff;
    }
    variance /= data.size();
    
    if (variance == 0.0) {
        return autocorr;
    }
    
    // 计算自相关
    for (int lag = 0; lag <= max_lag; ++lag) {
        double covariance = 0.0;
        int count = static_cast<int>(data.size()) - lag;
        
        for (int i = 0; i < count; ++i) {
            covariance += (data[i] - mean) * (data[i + lag] - mean);
        }
        
        autocorr[lag] = covariance / (count * variance);
    }
    
    return autocorr;
}

double calculateLjungBoxStatistic(const std::vector<double>& residuals, int lag) {
    auto autocorr = calculateAutocorrelation(residuals, lag);
    
    double lb_stat = 0.0;
    int n = static_cast<int>(residuals.size());
    
    for (int k = 1; k <= lag; ++k) {
        double rho_k = autocorr[k];
        lb_stat += rho_k * rho_k / (n - k);
    }
    
    return n * (n + 2) * lb_stat;
}

double calculateVaR(double volatility, double confidence_level) {
    // 假设正态分布
    static const double z_95 = 1.645;  // 95% VaR
    static const double z_99 = 2.326;  // 99% VaR
    
    double z_score;
    if (std::abs(confidence_level - 0.05) < 1e-6) {
        z_score = z_95;
    } else if (std::abs(confidence_level - 0.01) < 1e-6) {
        z_score = z_99;
    } else {
        // 使用近似公式
        z_score = std::sqrt(-2 * std::log(confidence_level));
    }
    
    return z_score * volatility;
}

double calculateExpectedShortfall(double volatility, double confidence_level) {
    // 正态分布下的期望损失
    double z_alpha = std::sqrt(-2 * std::log(confidence_level));
    double phi_z = std::exp(-0.5 * z_alpha * z_alpha) / std::sqrt(2 * M_PI);
    
    return volatility * phi_z / confidence_level;
}

// === BFGS优化算法实现 ===

EstimationResult GarchCalculator::optimizeWithBFGS(const GarchParameters& initial_params) {
    const int max_iterations = 500;  // 大幅增加最大迭代次数
    const double tolerance = 1e-6;   // 放宽收敛条件
    const double grad_tolerance = 1e-4;  // 放宽梯度容忍度
    const double func_tolerance = 1e-8;  // 放宽函数容忍度
    
    // 将参数转换为向量形式
    std::vector<double> x = parametersToVector(initial_params);
    const int n = static_cast<int>(x.size());
    
    // 初始化BFGS Hessian近似为单位矩阵
    std::vector<std::vector<double>> H(n, std::vector<double>(n, 0.0));
    for (int i = 0; i < n; ++i) {
        H[i][i] = 1.0;
    }
    
    // 计算初始目标函数值和梯度
    GarchParameters current_params = vectorToParameters(x);
    current_params = constrainParameters(current_params);
    double f = calculateLogLikelihood(current_params);
    
    if (!std::isfinite(f) || f < -1e6) {
        EstimationResult result;
        result.parameters = current_params;
        result.log_likelihood = f;
        result.iterations = 0;
        result.converged = false;
        return result;
    }
    
    std::vector<double> grad(n);
    calculateAnalyticalGradient(current_params, grad);
    
    // 检查梯度有效性
    bool grad_valid = true;
    for (double g : grad) {
        if (!std::isfinite(g)) {
            grad_valid = false;
            break;
        }
    }
    
    if (!grad_valid) {
        EstimationResult result;
        result.parameters = current_params;
        result.log_likelihood = f;
        result.iterations = 0;
        result.converged = false;
        return result;
    }
    
    // 注意：我们要最大化似然函数，所以需要转换为最小化问题
    // 但是梯度方向要相应调整：最大化f等价于最小化-f
    f = -f;  // 目标函数变为负似然
    for (double& g : grad) {
        g = -g;  // 梯度也要变号
    }
    
    EstimationResult result;
    result.parameters = current_params;
    result.log_likelihood = -f;  // 记录原始的正似然值
    result.iterations = 0;
    result.converged = false;
    
    // 更新参数向量以反映约束后的参数
    x = parametersToVector(current_params);
    
    double prev_f = f;
    int stagnant_count = 0;
    const int max_stagnant = 25;  // 增加停滞容忍度
    
    for (int iter = 0; iter < max_iterations; ++iter) {
        // 检查梯度收敛条件
        double grad_norm = 0.0;
        for (double g : grad) {
            grad_norm += g * g;
        }
        grad_norm = std::sqrt(grad_norm);
        
        if (grad_norm < grad_tolerance) {
            result.converged = true;
            break;
        }
        
        // 检查函数值变化 - 使用相对变化
        if (iter > 0) {
            double relative_change = std::abs(f - prev_f) / (1.0 + std::abs(prev_f));
            if (relative_change < func_tolerance) {
                stagnant_count++;
                if (stagnant_count >= max_stagnant) {
                    result.converged = true;
                    break;
                }
            } else {
                stagnant_count = 0;
            }
        }
        
        // 计算搜索方向: d = -H * grad
        std::vector<double> direction(n, 0.0);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                direction[i] -= H[i][j] * grad[j];
            }
        }
        
        // 进行线搜索
        double step_size = lineSearch(current_params, grad, direction, 0.1);  // 更保守的初始步长
        
        if (step_size < 1e-12) {
            // 步长太小，可能已经收敛
            break;
        }
        
        // 更新参数
        std::vector<double> x_new(n);
        for (int i = 0; i < n; ++i) {
            x_new[i] = x[i] + step_size * direction[i];
        }
        
        // 投影到可行域
        x_new = projectToFeasibleRegion(x_new);
        
        // 计算新的函数值和梯度
        GarchParameters new_params = vectorToParameters(x_new);
        new_params = constrainParameters(new_params);  // 确保参数约束
        double f_new = -calculateLogLikelihood(new_params);  // 转换为最小化问题
        
        std::vector<double> grad_new(n);
        calculateAnalyticalGradient(new_params, grad_new);
        for (double& g : grad_new) {
            g = -g;  // 梯度变号
        }
        
        // 检查函数值改进（记住我们在最小化-f，所以f_new < f意味着似然改进）
        if (-f_new > result.log_likelihood) {
            result.log_likelihood = -f_new;
            result.parameters = new_params;
        }
        
        // BFGS更新
        std::vector<double> s(n), y(n);
        for (int i = 0; i < n; ++i) {
            s[i] = x_new[i] - x[i];
            y[i] = grad_new[i] - grad[i];
        }
        
        // 检查BFGS更新条件
        double sy = 0.0;
        for (int i = 0; i < n; ++i) {
            sy += s[i] * y[i];
        }
        
        if (sy > 1e-10) {  // 放宽BFGS更新条件
            updateBFGSHessian(H, s, y);
        } else {
            // 如果BFGS更新条件不满足，重置Hessian为单位矩阵
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    H[i][j] = (i == j) ? 1.0 : 0.0;
                }
            }
        }
        
        // 更新当前点
        prev_f = f;
        x = x_new;
        f = f_new;
        grad = grad_new;
        current_params = new_params;
        
        result.iterations = iter + 1;
    }
    
    // 计算信息准则
    int num_params = 4;
    result.aic = -2 * result.log_likelihood + 2 * num_params;
    result.bic = -2 * result.log_likelihood + num_params * std::log(price_history_.size() - 1);
    
    return result;
}

void GarchCalculator::calculateAnalyticalGradient(const GarchParameters& params,
                                                  std::vector<double>& gradient) const {
    gradient.resize(4);
    std::fill(gradient.begin(), gradient.end(), 0.0);
    
    // 提取残差
    std::vector<double> residuals;
    for (size_t i = 1; i < price_history_.size(); ++i) {
        residuals.push_back(price_history_[i].log_return);
    }
    
    if (residuals.empty()) {
        return;
    }
    
    // 计算条件方差及其导数
    std::vector<double> sigma2 = calculateConditionalVariances(residuals, params);
    std::vector<std::vector<double>> dsigma2_dtheta(4, std::vector<double>(residuals.size(), 0.0));
    
    // 计算方差导数 - 递推公式
    for (size_t t = 1; t < residuals.size(); ++t) {
        // d(σ²_t)/d(ω) = 1 + β * d(σ²_{t-1})/d(ω)
        dsigma2_dtheta[0][t] = 1.0 + params.beta * dsigma2_dtheta[0][t-1];
        
        // d(σ²_t)/d(α) = ε²_{t-1} + β * d(σ²_{t-1})/d(α)
        dsigma2_dtheta[1][t] = residuals[t-1] * residuals[t-1] + params.beta * dsigma2_dtheta[1][t-1];
        
        // d(σ²_t)/d(β) = σ²_{t-1} + β * d(σ²_{t-1})/d(β)
        dsigma2_dtheta[2][t] = sigma2[t-1] + params.beta * dsigma2_dtheta[2][t-1];
    }
    
    // 计算 GED 相关的导数
    double nu = params.nu;
    double log_gamma_1_nu = std::lgamma(1.0/nu);
    double log_gamma_3_nu = std::lgamma(3.0/nu);
    double psi_1_nu = boost::math::digamma(1.0/nu);  // ψ(1/ν)
    double psi_3_nu = boost::math::digamma(3.0/nu);  // ψ(3/ν)
    
    double c = std::exp(log_gamma_3_nu - log_gamma_1_nu);
    double sqrt_c = std::sqrt(c);
    
    // 似然函数对各参数的梯度
    for (size_t t = 0; t < residuals.size(); ++t) {
        double z_t = residuals[t] / std::sqrt(sigma2[t]);
        double abs_z_std = std::abs(z_t / sqrt_c);
        
        double abs_z_pow_nu_minus_2;
        if (std::abs(nu - 2.0) < 1e-10) {
            abs_z_pow_nu_minus_2 = 1.0;
        } else if (std::abs(nu - 1.0) < 1e-10) {
            abs_z_pow_nu_minus_2 = (abs_z_std > 1e-10) ? 1.0 / abs_z_std : 0.0;
        } else {
            abs_z_pow_nu_minus_2 = std::pow(abs_z_std, nu - 2.0);
        }
        
        double sign_z = (z_t >= 0) ? 1.0 : -1.0;
        double common_term = 0.5 * nu * abs_z_pow_nu_minus_2 * sign_z / (sqrt_c * sigma2[t]);
        
        // 对 ω, α, β 的梯度
        for (int i = 0; i < 3; ++i) {
            double dsigma2_dt = dsigma2_dtheta[i][t];
            gradient[i] += -0.5 / sigma2[t] * dsigma2_dt + 
                          common_term * residuals[t] * dsigma2_dt / std::sqrt(sigma2[t]);
        }
        
        // 对 ν 的梯度 (复杂，需要 digamma 函数)
        double dc_dnu = c * (psi_3_nu * 3.0/(nu*nu) - psi_1_nu * 1.0/(nu*nu));
        double abs_z_pow_nu = std::pow(abs_z_std, nu);
        double dlog_abs_z_dnu = (abs_z_std > 1e-10) ? std::log(abs_z_std) : 0.0;
        
        gradient[3] += 1.0/nu - 0.5 * dc_dnu / c + 
                      0.5 * dc_dnu / c - 0.5 * abs_z_pow_nu * dlog_abs_z_dnu;
    }
}

double GarchCalculator::lineSearch(const GarchParameters& current_params,
                                  const std::vector<double>& gradient,
                                  const std::vector<double>& direction,
                                  double initial_step) const {
    const double c1 = 1e-4;  // Armijo条件参数
    const double rho = 0.5;  // 步长缩减因子
    const int max_line_search = 20;
    
    std::vector<double> x = parametersToVector(current_params);
    double f0 = -calculateLogLikelihood(current_params);
    
    // 计算方向导数
    double dg0 = 0.0;
    for (size_t i = 0; i < gradient.size(); ++i) {
        dg0 += gradient[i] * direction[i];
    }
    
    // 如果方向导数为正，这不是下降方向
    if (dg0 >= 0) {
        return 1e-8;  // 返回很小的步长
    }
    
    double step = initial_step;
    double best_step = step;
    double best_f = f0;
    
    for (int i = 0; i < max_line_search; ++i) {
        // 计算新点
        std::vector<double> x_new(x.size());
        for (size_t j = 0; j < x.size(); ++j) {
            x_new[j] = x[j] + step * direction[j];
        }
        
        // 投影到可行域
        x_new = projectToFeasibleRegion(x_new);
        
        // 计算新的函数值
        GarchParameters new_params = vectorToParameters(x_new);
        double f_new = -calculateLogLikelihood(new_params);
        
        // 记录最佳步长
        if (std::isfinite(f_new) && f_new < best_f) {
            best_f = f_new;
            best_step = step;
        }
        
        // Armijo条件检查
        if (std::isfinite(f_new) && f_new <= f0 + c1 * step * dg0) {
            return step;
        }
        
        step *= rho;
        
        // 如果步长太小，退出
        if (step < 1e-12) {
            break;
        }
    }
    
    // 如果没有满足Armijo条件的步长，返回最佳步长
    return best_step > 1e-12 ? best_step : 1e-8;
}

void GarchCalculator::updateBFGSHessian(std::vector<std::vector<double>>& H,
                                        const std::vector<double>& s,
                                        const std::vector<double>& y) const {
    const int n = static_cast<int>(s.size());
    
    // 计算 rho = 1 / (y^T * s)
    double ys = 0.0;
    for (int i = 0; i < n; ++i) {
        ys += y[i] * s[i];
    }
    
    if (std::abs(ys) < 1e-10) {
        return; // 跳过更新
    }
    
    double rho = 1.0 / ys;
    
    // 计算 H_new = (I - rho * s * y^T) * H * (I - rho * y * s^T) + rho * s * s^T
    
    // 创建临时矩阵
    std::vector<std::vector<double>> temp1(n, std::vector<double>(n));
    std::vector<std::vector<double>> temp2(n, std::vector<double>(n));
    
    // temp1 = (I - rho * s * y^T)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            temp1[i][j] = (i == j ? 1.0 : 0.0) - rho * s[i] * y[j];
        }
    }
    
    // temp2 = temp1 * H
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            temp2[i][j] = 0.0;
            for (int k = 0; k < n; ++k) {
                temp2[i][j] += temp1[i][k] * H[k][j];
            }
        }
    }
    
    // H = temp2 * (I - rho * y * s^T)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            H[i][j] = 0.0;
            for (int k = 0; k < n; ++k) {
                double I_minus_rho_ys = (k == j ? 1.0 : 0.0) - rho * y[k] * s[j];
                H[i][j] += temp2[i][k] * I_minus_rho_ys;
            }
        }
    }
    
    // H += rho * s * s^T
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            H[i][j] += rho * s[i] * s[j];
        }
    }
}

std::vector<double> GarchCalculator::parametersToVector(const GarchParameters& params) const {
    // 使用参数缩放来改善数值稳定性
    return {
        params.omega * 1e6,    // omega缩放：1e-5 -> 10
        params.alpha,          // alpha不变：0.1 -> 0.1
        params.beta,           // beta不变：0.8 -> 0.8
        params.nu              // nu不变：2.0 -> 2.0
    };
}

GarchParameters GarchCalculator::vectorToParameters(const std::vector<double>& vec) const {
    if (vec.size() != 4) {
        return GarchParameters();
    }
    // 还原参数缩放
    return GarchParameters(
        vec[0] / 1e6,    // 还原omega缩放
        vec[1],          // alpha不变
        vec[2],          // beta不变
        vec[3]           // nu不变
    );
}

std::vector<double> GarchCalculator::projectToFeasibleRegion(const std::vector<double>& params) const {
    std::vector<double> projected = params;
    
    // omega约束: 对应实际omega范围 [1e-8, 1.0]，但这里是缩放后的
    projected[0] = std::max(0.01, std::min(1000000.0, projected[0]));  // 对应实际omega: [1e-8, 1.0]
    
    // alpha约束: [0.0, 0.999]
    projected[1] = std::max(0.0, std::min(0.999, projected[1]));
    
    // beta约束: [0.0, 0.999] - 现在允许真正的GARCH(1,1)
    projected[2] = std::max(0.0, std::min(0.999, projected[2]));
    
    // nu约束: [1.001, 50.0] - 扩展范围
    projected[3] = std::max(1.001, std::min(50.0, projected[3]));
    
    // 平稳性约束: alpha + beta < 1
    if (projected[1] + projected[2] >= 0.9999) {
        double sum = projected[1] + projected[2];
        double scale = 0.9999 / sum;
        projected[1] *= scale;
        projected[2] *= scale;
    }
    
          return projected;
  }

} // namespace garch