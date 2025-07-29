from stata_mcp import *

if __name__ == "__main__":
    # 1. 基本测试 - 最简单的变量列表
    print("Test 1 - Basic variable list:")
    print(StataCommandGenerator.summarize(["mpg", "weight"]))
    print("\nExpected: summarize mpg weight\n")

    # 2. 无变量列表 - 默认所有变量
    print("Test 2 - No variable list:")
    print(StataCommandGenerator.summarize())
    print("\nExpected: summarize\n")

    # 3. if条件测试
    print("Test 3 - With if condition:")
    print(StataCommandGenerator.summarize(["price"], if_condition="foreign == 1"))
    print("\nExpected: summarize price if foreign == 1\n")

    # 4. in范围测试
    print("Test 4 - With in range:")
    print(StataCommandGenerator.summarize(["price"], in_range="1/100"))
    print("\nExpected: summarize price in 1/100\n")

    # 5. 权重测试
    print("Test 5 - With weights:")
    print(StataCommandGenerator.summarize(["price"], weight="aweights=pop"))
    print("\nExpected: summarize price [aweights=pop]\n")

    # 6. 详细选项测试
    print("Test 6 - With detail option:")
    print(StataCommandGenerator.summarize(["price", "mpg"], detail=True))
    print("\nExpected: summarize price mpg, detail\n")

    # 7. 仅均值选项测试
    print("Test 7 - With meanonly option:")
    print(StataCommandGenerator.summarize(["price"], meanonly=True))
    print("\nExpected: summarize price, meanonly\n")

    # 8. 格式选项测试
    print("Test 8 - With format option:")
    print(StataCommandGenerator.summarize(["price"], fmt=True))
    print("\nExpected: summarize price, format\n")

    # 9. 分隔线选项测试
    print("Test 9 - With separator option:")
    print(StataCommandGenerator.summarize(["price", "mpg"], separator=5))
    print("\nExpected: summarize price mpg, separator(5)\n")

    # 10. 显示选项测试
    print("Test 10 - With display options:")
    print(StataCommandGenerator.summarize(["price"], vsquish=True, noemptycells=True))
    print("\nExpected: summarize price, vsquish noemptycells\n")

    # 11. 复杂组合测试
    print("Test 11 - Complex combination:")
    print(StataCommandGenerator.summarize(
        ["price", "mpg"],
        if_condition="foreign == 1",
        detail=True,
        separator=10,
        vsquish=True,
        fvwrap=3
    ))
    print("\nExpected: summarize price mpg if foreign == 1, detail separator(10) vsquish fvwrap(3)\n")

    # 12. 错误测试 - detail和meanonly冲突
    print("Test 12 - Error: detail and meanonly conflict")
    try:
        print(StataCommandGenerator.summarize(["price"], detail=True, meanonly=True))
    except ValueError as e:
        print(f"Caught error as expected: {e}")
    print("\nExpected: ValueError about conflict between detail and meanonly\n")

    # 13. 错误测试 - 无效权重类型
    print("Test 13 - Error: invalid weight type")
    try:
        print(StataCommandGenerator.summarize(["price"], weight="invalid=pop"))
    except ValueError as e:
        print(f"Caught error as expected: {e}")
    print("\nExpected: ValueError about invalid weight type\n")

    # 14. 错误测试 - iweights与detail冲突
    print("Test 14 - Error: iweights with detail")
    try:
        print(StataCommandGenerator.summarize(["price"], weight="iweights=pop", detail=True))
    except ValueError as e:
        print(f"Caught error as expected: {e}")
    print("\nExpected: ValueError about iweights not allowed with detail\n")

    # 15. 错误测试 - 无效显示选项
    print("Test 15 - Error: invalid display option")
    try:
        print(StataCommandGenerator.summarize(["price"], invalid_option=True))
    except ValueError as e:
        print(f"Caught error as expected: {e}")
    print("\nExpected: ValueError about invalid display option\n")
