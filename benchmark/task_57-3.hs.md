
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldMap-(,)

# poly_type
Ad-hoc

# signature
```haskell
foldMap :: Monoid m => (a0 -> m) -> (a, a0) -> m
```   

# code
```haskell
foldMap f (_, y) = f y
```

# dependencies
