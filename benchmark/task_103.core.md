
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--zip3

# poly_type
Parametric

# signature
```haskell
zip3 :: [a] -> [b] -> [c] -> [(a,b,c)]
```   

# code
```haskell
zip3 (a:as) (b:bs) (c:cs) = (a,b,c) : zip3 as bs cs
zip3 _      _      _      = []
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```