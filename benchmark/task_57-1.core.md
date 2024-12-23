
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldMap-Maybe

# poly_type
Ad-hoc

# signature
```haskell
foldMap :: Monoid m => (a -> m) -> Maybe a -> m
```   

# code
```haskell
foldMap = maybe mempty
```

# dependencies
## 0
```haskell
maybe :: b -> (a -> b) -> Maybe a -> b
```
## 1
```haskell
mempty :: Monoid m => m
```
