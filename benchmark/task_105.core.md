
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--zipWith3

# poly_type
Parametric

# signature
```haskell
zipWith3 :: (a->b->c->d) -> [a]->[b]->[c]->[d]
```   

# code
```haskell
zipWith3 z = go
  where
    go (a:as) (b:bs) (c:cs) = z a b c : go as bs cs
    go _ _ _                = []
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```
