
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--zipWith

# poly_type
Parametric

# signature
```haskell
zipWith :: (a->b->c) -> [a]->[b]->[c]
```   

# code
```haskell
zipWith f = go
  where
    go [] _ = []
    go _ [] = []
    go (x:xs) (y:ys) = f x y : go xs ys
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```