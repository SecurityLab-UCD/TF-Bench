import pytest
from src.hs_parser import HASKELL_LANGUAGE
from src.hs_parser.ast_util import AST, ASTLoc
from hypothesis import given
import hypothesis.strategies as st
from funcy_chain import Chain


def test_function_extract():
    fn_add = """
add :: Int -> Int -> Int
add 0 y = y
add x 0 = x
add x y = x + y
"""

    fn_scanl = """
scanl :: (Char -> Char -> Char) -> Char -> ByteString -> ByteString
scanl f z = B.scanl (\a b -> c2w (f (w2c a) (w2c b))) (c2w z)
"""

    comments = """
-- | 'scanl' is similar to 'foldl', but returns a list of successive
-- reduced values from the left:
--
-- > scanl f z [x1, x2, ...] == [z, z `f` x1, (z `f` x1) `f` x2, ...]
--
-- Note that
--
-- > last (scanl f z xs) == foldl f z xs.
"""
    hs_functions = [fn_add, fn_scanl, comments]
    hs_lines = Chain(hs_functions).mapcat(lambda s: s.splitlines()).value

    @given(st.permutations(hs_lines))
    def haskell_lines_in_any_order(lines):
        code = "\n".join(lines)
        ast = AST(code, HASKELL_LANGUAGE)
        fs = Chain(ast.get_functions()).map(ast.func2src).value
        fs.sort()

        assert fs[0] == fn_add.strip("\n")
        assert fs[1] == fn_scanl.strip("\n")

    haskell_lines_in_any_order()


if __name__ == "__main__":
    test_function_extract()
