CASES=`grep 'TestCase(' -R . --include=*.py | wc -l`
TESTS=`grep 'def test_' -R . --include=*.py | wc -l`
ASSERTS=`grep 'self.assert' -R . --include=*.py | wc -l`
echo -e $CASES test cases;
echo -e $TESTS individual tests;
echo -e asserting $ASSERTS things;

