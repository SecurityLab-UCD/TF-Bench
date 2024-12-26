
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Generics.hs--liftA2-Maybe

# poly_type
Parametric

# signature
```haskell
liftA2 :: (a1 -> a2 -> a3) -> Maybe a1 -> Maybe a2 -> Maybe a3
```   

# code
```haskell
liftA2 f (Just x) (Just y) = Just (f x y)
liftA2 _ _ _ = Nothing
```

# dependencies
## 0
```haskell
data Maybe a = Nothing | Just a
```
