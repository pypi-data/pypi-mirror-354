from softassert

def test_case1():
    SoftAssert.soft_assert(1 == 2, "1 != 2").check()
    assert 1 == 1
    print("1=1")# This will pass
    SoftAssert.soft_assert("a" in "b", "'a' not in 'b'").check()


def test_case2():
    SoftAssert.soft_assert(True, "should be true")
    assert 1 == 1
    SoftAssert.check()
