"""
Tasks whose dependencies cannot be directly added using `hoogle.py`
"""

# pylint: disable=line-too-long
MANUAL_TASKS = [
    {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--lines",
        "signature": "lines :: String -> [String]",
        "code": "lines \"\"                =  []\nlines s                 =  cons (case break (== '\\n') s of\n                                    (l, s') -> (l, case s' of\n                                                    []      -> []\n                                                    _:s''   -> lines s''))\n  where\n    cons ~(h, t)        =  h : t",
        "poly_type": "Monomorphic",
        "dependencies": [
            "break :: (a -> Bool) -> [a] -> ([a],[a])",
        ],
    },
    {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--words",
        "signature": "words :: String -> [String]",
        "code": "words s                 =  case dropWhile isSpace s of\n                                \"\" -> []\n                                s' -> w : words s''\n                                      where (w, s'') =\n                                             break isSpace s'",
        "poly_type": "Monomorphic",
        "dependencies": [
            "dropWhile :: (a -> Bool) -> [a] -> [a]",
            "isSpace :: Char -> Bool",
            "break :: (a -> Bool) -> [a] -> ([a],[a])",
        ],
    },
]
