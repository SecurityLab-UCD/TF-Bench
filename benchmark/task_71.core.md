
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--until

# poly_type
Parametric

# signature
```haskell
until :: (a -> Bool) -> (a -> a) -> a -> a
```   

# code
```haskell
until p f = go
  where
    go x | p x          = x
         | otherwise    = go (f x)
```

# dependencies
