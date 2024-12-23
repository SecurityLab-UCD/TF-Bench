
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--fmap-Maybe

# poly_type
Parametric

# signature
```haskell
fmap :: (a -> b) -> Maybe a -> Maybe b
```   

# code
```haskell
fmap _ Nothing       = Nothing
fmap f (Just a)      = Just (f a)
```

# dependencies
## 0
```haskell
data Maybe a = Nothing | Just a
```
