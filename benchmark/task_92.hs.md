
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--cycle

# poly_type
Parametric

# signature
```haskell
cycle :: [a] -> [a]
```   

# code
```haskell
cycle [] = error
cycle xs = xs' where xs' = xs ++ xs'
```

# dependencies
## 0
```haskell
(++) :: [a] -> [a] -> [a]
```
