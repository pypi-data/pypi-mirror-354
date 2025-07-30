#!/usr/bin/env python3
"""
最简单的GARCH示例程序
使用yfinance获取股票数据，用garch_lib进行GARCH建模
现在直接使用收益率数据，与arch库保持一致
"""

import numpy as np
import yfinance as yf
import garch_lib as gc

def main():
    # 1. 下载股票数据 (苹果股票，1年数据)
    print("📊 下载AAPL股票数据...")
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1y")
    
    # 2. 计算对数收益率 (与arch库保持一致)
    print("📈 计算对数收益率...")
    prices = data['Close'].values
    returns = np.log(prices[1:] / prices[:-1])
    
    # 3. 去除均值 (中心化处理，与arch库保持一致)
    returns = returns - returns.mean()
    
    # 4. 创建GARCH计算器并直接添加收益率数据
    print("⚡ 运行GARCH模型...")
    calc = gc.GarchCalculator(history_size=len(returns) + 10)
    
    # 直接使用收益率，不再需要价格转换
    calc.add_returns(returns.tolist())
    
    # 5. 估计GARCH参数
    result = calc.estimate_parameters()
    params = result.parameters
    
    # 6. 输出结果
    print(f"\n✅ GARCH(1,1)模型结果:")
    print(f"   数据点数: {len(returns)}")
    print(f"   收敛状态: {'✅' if result.converged else '❌'}")
    print(f"   ω (omega): {params.omega:.6f}")
    print(f"   α (alpha): {params.alpha:.6f}")  
    print(f"   β (beta):  {params.beta:.6f}")
    print(f"   ν (nu):    {params.nu:.6f}")
    print(f"   持续性 (α+β): {params.alpha + params.beta:.6f}")
    print(f"   当前波动率: {calc.get_current_volatility():.6f}")
    
    # 7. 预测未来1天的波动率
    forecast = calc.forecast_volatility(1)
    print(f"   明天预测波动率: {forecast.volatility:.6f}")
    
    # 8. 显示与arch库的兼容性
    print(f"\n📋 数据兼容性:")
    print(f"   输入格式: 直接使用收益率 (与arch库一致)")
    print(f"   数据预处理: 中心化处理")
    print(f"   模型类型: GARCH(1,1)-GED")

if __name__ == "__main__":
    main() 