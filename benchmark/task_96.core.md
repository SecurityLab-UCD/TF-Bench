
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--dropWhile

# poly_type
Parametric

# signature
```haskell
dropWhile :: (a -> Bool) -> [a] -> [a]
```   

# code
```haskell
dropWhile _ []          =  []
dropWhile p xs@(x:xs')
            | p x       =  dropWhile p xs'
            | otherwise =  xs
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```

