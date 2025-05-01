
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--concat

# poly_type
Parametric

# signature
```haskell
concat :: [[a]] -> [a]
```   

# code
```haskell
concat = foldr (++) []
```

# dependencies
## 0
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```
## 1
```haskell
(++) :: [a] -> [a] -> [a]
```