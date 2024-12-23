
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(++)

# poly_type
Parametric

# signature
```haskell
(++) :: [a] -> [a] -> [a]
```   

# code
```haskell
(++) (x:xs) ys = x : xs ++ ys
(++) []     ys = ys
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```
